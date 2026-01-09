"""
Gerenciador de fases do jogo, responsável por criar e gerenciar as bolas em cada fase.
"""
import pygame
import random
from typing import List, Counter, Tuple
from mygame.core.asset_manager import AssetManager
from mygame.fx.particle_system import ParticleSystem
from mygame.core.game_mode import GameMode, BallBehavior
from mygame.utils.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS,
    BASE_BALL_COUNT, BALL_COUNT_INCREASE_PER_PHASE,
    BASE_FREE_BALL_SPEED, SPEED_INCREASE_PER_PHASE,
    BASE_GRAVITY, GRAVITY_INCREASE_PER_PHASE,
    COLORS_PASTEL, MULTIPLAYER_PHASE_LIMIT,
    SAFE_POSITION_MAX_ATTEMPTS, COLLISION_MARGIN_MULTIPLIER
)
from mygame.utils.geometry import (
    calculate_bounds_for_singleplayer, calculate_bounds_for_multiplayer,
    calculate_distance_squared, is_position_in_bounds
)
from mygame.utils.helpers import is_multiplayer_mode
from mygame.entities.ball_factory import BallFactory
from mygame.entities.ball_base import Ball
from mygame.entities.ball_free import FreeBall
from mygame.entities.ball_jump import JumpBall
from mygame.entities.stationary_ball import StationaryBall
from mygame.utils.types import Bounds
from mygame.utils.validators import (
    validate_game_mode, validate_ball_behavior,
    validate_phase_number, validate_score
)
from mygame.utils.exceptions import InvalidGameModeError, InvalidBallBehaviorError
from mygame.utils.logger import log_info, log_warning, log_error, log_debug

# Mapeamento de comportamentos de bola para classes
BALL_BEHAVIORS = {
    BallBehavior.STATIONARY.value: StationaryBall,
    BallBehavior.FREE_MOVEMENT.value: FreeBall,
    BallBehavior.JUMPING.value: JumpBall
}


class PhaseManager:
    """Gerencia as fases do jogo, criação de bolas e lógica de progressão."""
    
    def __init__(self, assets: AssetManager, particles: ParticleSystem):
        self.assets = assets
        self.particles = particles
        self.balls: List[Ball] = []
        self.opponent_balls: List[Ball] = []
        self.game_mode = GameMode.SINGLEPLAYER.value
        self.ball_behavior = BallBehavior.STATIONARY.value
        self.current_phase = 1
        self.player_one_score = 0
        self.player_two_score = 0
        self.ai_last_action_time = 0
        self.ai_think_interval = 1200
        
        # Cache de cálculos
        self._cached_phase_params: dict[int, tuple[int, float, float, dict]] = {}
        self._cached_singleplayer_bounds: Bounds | None = None
        self._cached_multiplayer_bounds: tuple[Bounds, Bounds] | None = None

    def _get_safe_position(
        self, bounds: Bounds, existing_balls: List[Ball]
    ) -> tuple[int, int]:
        """
        Encontra uma posição segura para uma nova bola, evitando sobreposição.
        Otimizado para reduzir complexidade: calcula collision_margin uma vez e usa early return.
        
        Args:
            bounds: Limites da área (x_min, x_max, y_min, y_max)
            existing_balls: Lista de bolas existentes
            
        Returns:
            Tupla (x, y) com posição segura
        """
        # Early return: se não há bolas existentes, retorna posição aleatória
        if not existing_balls:
            return (
                random.randint(bounds[0] + BALL_RADIUS, bounds[1] - BALL_RADIUS),
                random.randint(bounds[2] + BALL_RADIUS, bounds[3] - BALL_RADIUS)
            )
        
        # Calcula collision_margin uma vez (otimização)
        collision_margin = COLLISION_MARGIN_MULTIPLIER * BALL_RADIUS
        collision_margin_sq = collision_margin * collision_margin
        
        for _ in range(SAFE_POSITION_MAX_ATTEMPTS):
            x = random.randint(bounds[0] + BALL_RADIUS, bounds[1] - BALL_RADIUS)
            y = random.randint(bounds[2] + BALL_RADIUS, bounds[3] - BALL_RADIUS)
            pos = (x, y)
            
            # Verifica colisão usando função otimizada
            if not self._is_position_overlapping(pos, existing_balls, collision_margin_sq):
                return pos
        
        # Fallback: retorna posição aleatória mesmo se houver sobreposição
        log_warning(
            "Could not find safe position after max attempts, using random",
            attempts=SAFE_POSITION_MAX_ATTEMPTS,
            existing_balls_count=len(existing_balls)
        )
        return (
            random.randint(bounds[0] + BALL_RADIUS, bounds[1] - BALL_RADIUS),
            random.randint(bounds[2] + BALL_RADIUS, bounds[3] - BALL_RADIUS)
        )
    
    def _is_position_overlapping(
        self, pos: tuple[int, int], existing_balls: List[Ball], collision_margin_sq: float
    ) -> bool:
        """
        Verifica se uma posição está sobrepondo alguma bola existente.
        
        Args:
            pos: Posição (x, y) a verificar
            existing_balls: Lista de bolas existentes
            collision_margin_sq: Distância mínima ao quadrado
            
        Returns:
            True se há sobreposição
        """
        x, y = pos
        for ball in existing_balls:
            dist_sq = calculate_distance_squared((x, y), (ball.x, ball.y))
            if dist_sq < collision_margin_sq:
                return True
        return False

    def _calculate_phase_parameters(self) -> Tuple[int, float, float, dict]:
        """
        Calcula os parâmetros da fase atual (número de bolas, velocidade, gravidade).
        Usa cache para evitar recálculos desnecessários.
        
        Returns:
            Tupla (num_balls, speed, gravity, params_dict)
        """
        # Verifica cache
        if self.current_phase in self._cached_phase_params:
            return self._cached_phase_params[self.current_phase]
        
        # Calcula parâmetros
        num_balls = (
            (BASE_BALL_COUNT + (self.current_phase - 1) * BALL_COUNT_INCREASE_PER_PHASE) // 2 * 2
        )
        speed = BASE_FREE_BALL_SPEED + (self.current_phase - 1) * SPEED_INCREASE_PER_PHASE
        gravity = BASE_GRAVITY + (self.current_phase - 1) * GRAVITY_INCREASE_PER_PHASE
        
        params = {
            "speed": speed,
            "gravity": gravity,
            "pop_sound": self.assets.sounds.get('pop')
        }
        
        result = (num_balls, speed, gravity, params)
        
        # Armazena no cache
        self._cached_phase_params[self.current_phase] = result
        
        return result
    
    def _invalidate_cache(self) -> None:
        """Invalida o cache quando necessário (ex: mudança de fase)."""
        self._cached_phase_params.clear()

    def _create_balls_for_singleplayer(
        self, ball_class: type, colors: List[Tuple[int, int, int]], params: dict
    ) -> None:
        """
        Cria bolas para o modo singleplayer.
        
        Args:
            ball_class: Classe da bola a ser criada
            colors: Lista de cores disponíveis
            params: Parâmetros de criação (speed, gravity, etc)
        """
        # Usa cache de bounds
        if self._cached_singleplayer_bounds is None:
            self._cached_singleplayer_bounds = calculate_bounds_for_singleplayer()
        bounds = self._cached_singleplayer_bounds
        
        num_balls, _, _, _ = self._calculate_phase_parameters()
        player_one_balls = []
        
        for i in range(num_balls):
            position = self._get_safe_position(bounds, player_one_balls)
            ball = BallFactory.create_ball(
                self.ball_behavior,
                colors[i % 2],
                colors,
                bounds,
                position,
                **params
            )
            player_one_balls.append(ball)
        
        self.balls = player_one_balls

    def _create_balls_for_multiplayer(
        self, ball_class: type, colors: List[Tuple[int, int, int]], params: dict
    ) -> None:
        """
        Cria bolas para o modo multiplayer (PvP ou PvE).
        
        Args:
            ball_class: Classe da bola a ser criada
            colors: Lista de cores disponíveis
            params: Parâmetros de criação (speed, gravity, etc)
        """
        num_balls, _, _, _ = self._calculate_phase_parameters()
        
        # Usa cache de bounds
        if self._cached_multiplayer_bounds is None:
            self._cached_multiplayer_bounds = calculate_bounds_for_multiplayer()
        player_one_bounds, player_two_bounds = self._cached_multiplayer_bounds
        
        player_one_balls = []
        player_two_balls = []
        
        for i in range(num_balls // 2):
            # Cria bolinhas para Jogador 1
            pos1 = self._get_safe_position(player_one_bounds, player_one_balls)
            ball1 = BallFactory.create_ball(
                self.ball_behavior,
                colors[i % 2],
                colors,
                player_one_bounds,
                pos1,
                **params
            )
            player_one_balls.append(ball1)
            
            # Cria bolinhas para Jogador 2
            pos2 = self._get_safe_position(player_two_bounds, player_two_balls)
            ball2 = BallFactory.create_ball(
                self.ball_behavior,
                colors[i % 2],
                colors,
                player_two_bounds,
                pos2,
                **params
            )
            player_two_balls.append(ball2)
        
        self.balls = player_one_balls
        self.opponent_balls = player_two_balls

    def load_current_phase(self) -> None:
        """
        Carrega a fase atual com todas as bolas necessárias.
        
        Raises:
            InvalidBallBehaviorError: Se o comportamento da bola for inválido
            ValueError: Se a fase for inválida
        """
        # Fail fast: valida pré-condições
        validate_phase_number(self.current_phase)
        
        if self.ball_behavior not in BALL_BEHAVIORS:
            raise InvalidBallBehaviorError(self.ball_behavior)
        
        log_info(
            "Loading phase",
            phase=self.current_phase,
            game_mode=self.game_mode,
            ball_behavior=self.ball_behavior
        )
        
        self.balls.clear()
        self.opponent_balls.clear()
        
        ball_class = BALL_BEHAVIORS[self.ball_behavior]
        colors = random.sample(COLORS_PASTEL, 2)
        num_balls, speed, gravity, params = self._calculate_phase_parameters()
        
        log_debug(
            "Phase parameters calculated",
            phase=self.current_phase,
            num_balls=num_balls,
            speed=speed,
            gravity=gravity
        )
        
        if is_multiplayer_mode(self.game_mode):
            self._create_balls_for_multiplayer(ball_class, colors, params)
            log_info(
                "Multiplayer phase loaded",
                phase=self.current_phase,
                player_one_balls=len(self.balls),
                player_two_balls=len(self.opponent_balls)
            )
        else:
            self._create_balls_for_singleplayer(ball_class, colors, params)
            log_info(
                "Singleplayer phase loaded",
                phase=self.current_phase,
                balls_count=len(self.balls)
            )

    def start_new_progression(self, game_mode: str, ball_behavior: str) -> None:
        """
        Inicia uma nova progressão de fases.
        
        Args:
            game_mode: Modo de jogo (validado)
            ball_behavior: Comportamento da bola (validado)
            
        Raises:
            InvalidGameModeError: Se o modo de jogo for inválido
            InvalidBallBehaviorError: Se o comportamento for inválido
        """
        # Fail fast: valida entradas antes de prosseguir
        self.game_mode = validate_game_mode(game_mode)
        self.ball_behavior = validate_ball_behavior(ball_behavior)
        self.current_phase = 1
        self.player_one_score = 0
        self.player_two_score = 0
        log_info(
            "Starting new progression",
            game_mode=self.game_mode,
            ball_behavior=self.ball_behavior
        )
        self.load_current_phase()

    def load_next_phase(self) -> None:
        """Carrega a próxima fase."""
        log_info("Loading next phase", current_phase=self.current_phase)
        self.current_phase += 1
        # Cache será atualizado automaticamente quando necessário
        self.load_current_phase()

    def _run_ai_logic(self) -> None:
        """Executa a lógica de IA para o modo Player vs Bot."""
        if not self.opponent_balls or self.game_mode != GameMode.PLAYER_VS_BOT.value:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.ai_last_action_time > self.ai_think_interval:
            color_counts = Counter(ball.color for ball in self.opponent_balls)
            if len(color_counts) > 1:
                majority_color = color_counts.most_common(1)[0][0]
                minority_balls = [
                    ball for ball in self.opponent_balls
                    if ball.color != majority_color
                ]
                if minority_balls:
                    selected_ball = random.choice(minority_balls)
                    old_color = selected_ball.switch_color()
                    self.particles.emit(selected_ball.x, selected_ball.y, old_color)
                    log_debug(
                        "AI action executed",
                        phase=self.current_phase,
                        majority_color=majority_color,
                        minority_count=len(minority_balls)
                    )
            self.ai_last_action_time = current_time

    def update(self) -> None:
        """Atualiza todas as bolas e executa lógica de IA."""
        for ball in self.balls:
            ball.update()
        for ball in self.opponent_balls:
            ball.update()
        self._run_ai_logic()

    def draw(self, screen: pygame.Surface) -> None:
        """Desenha todas as bolas na tela."""
        for ball in self.balls:
            ball.draw(screen)
        for ball in self.opponent_balls:
            ball.draw(screen)

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """
        Processa um clique na posição especificada.
        
        Args:
            pos: Tupla (x, y) da posição do clique
        """
        target_list = self.balls
        screen_midpoint = SCREEN_HEIGHT // 2
        
        if self.game_mode == GameMode.PLAYER_VS_PLAYER.value and pos[1] > screen_midpoint:
            target_list = self.opponent_balls
        elif self.game_mode == GameMode.PLAYER_VS_BOT.value and pos[1] > screen_midpoint:
            return  # Bot controla sua área
        
        for ball in target_list:
            if ball.is_clicked(pos):
                old_color = ball.switch_color()
                self.particles.emit(ball.x, ball.y, old_color)
                log_debug(
                    "Ball clicked",
                    phase=self.current_phase,
                    position=pos,
                    old_color=old_color,
                    new_color=ball.color
                )
                break

    def is_phase_complete(self) -> Tuple[bool, str]:
        """
        Verifica se a fase atual está completa.
        
        Returns:
            Tupla (is_complete, winner_name)
        """
        if not self.balls:
            return False, ""
        
        first_color = self.balls[0].color
        player_one_wins = all(ball.color == first_color for ball in self.balls)
        
        if self.game_mode in [GameMode.PLAYER_VS_PLAYER.value, GameMode.PLAYER_VS_BOT.value]:
            if not self.opponent_balls:
                return player_one_wins, "Jogador 1" if player_one_wins else ""
            
            first_opponent_color = self.opponent_balls[0].color
            player_two_wins = all(
                ball.color == first_opponent_color for ball in self.opponent_balls
            )
            if player_two_wins:
                winner = "Jogador 2" if self.game_mode == GameMode.PLAYER_VS_PLAYER.value else "Bot"
                return True, winner
        
        if player_one_wins:
            return True, "Jogador 1"
        return False, ""

    def update_score(self, winner_side: str) -> None:
        """
        Atualiza o placar com base no vencedor da fase.
        
        Args:
            winner_side: Nome do vencedor ("Jogador 1", "Jogador 2", "Bot")
        """
        if winner_side == "Jogador 1":
            self.player_one_score = validate_score(self.player_one_score + 1)
        else:  # "Jogador 2" ou "Bot"
            self.player_two_score = validate_score(self.player_two_score + 1)

    def get_final_winner(self) -> str:
        """
        Retorna o vencedor final baseado no placar.
        
        Returns:
            Nome do vencedor ou "Empate"
        """
        if self.player_one_score > self.player_two_score:
            return "Jogador 1"
        if self.player_two_score > self.player_one_score:
            return "Jogador 2" if self.game_mode == GameMode.PLAYER_VS_PLAYER.value else "Bot"
        return "Empate"

    def is_progression_complete(self) -> bool:
        """
        Verifica se o limite de fases do multiplayer foi atingido.
        
        Returns:
            True se a progressão está completa
        """
        if self.game_mode in [GameMode.PLAYER_VS_PLAYER.value, GameMode.PLAYER_VS_BOT.value]:
            return self.current_phase >= MULTIPLAYER_PHASE_LIMIT
        return False  # Singleplayer nunca termina por fase
