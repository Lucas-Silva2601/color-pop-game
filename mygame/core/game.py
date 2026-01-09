import pygame
import sys
import json
from typing import Dict, Optional
from mygame.core.asset_manager import AssetManager
from mygame.core.phase_manager import PhaseManager
from mygame.fx.particle_system import ParticleSystem
from mygame.ui.menu_screen import MenuScreen
from mygame.ui.hud import HUD
from mygame.ui.button import Button
from mygame.core.game_state import GameState
from mygame.core.game_mode import GameMode
from mygame.ui.menu_names import MenuName
from mygame.utils.validators import validate_game_mode, validate_ball_behavior
from mygame.utils.exceptions import InvalidGameModeError, InvalidBallBehaviorError, SaveDataError
from mygame.utils.logger import log_info, log_warning, log_error, set_context
from mygame.utils.helpers import is_multiplayer_mode
from mygame.utils.config import (
    SAVE_FILE, SINGLEPLAYER_TIME_LIMIT_SECONDS, FPS,
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAY, WHITE,
    PLAYER_AREA_COLOR, OPPONENT_AREA_COLOR, DIVIDER_LINE_WIDTH
)
from mygame.utils.types import Color
from mygame.core.interfaces import IAssetManager, IParticleSystem
from mygame.utils.performance import PerformanceMonitor
from typing import Optional

class Game:
    def __init__(
        self,
        screen: pygame.Surface,
        asset_manager: Optional[IAssetManager] = None,
        particle_system: Optional[IParticleSystem] = None,
        phase_manager: Optional[PhaseManager] = None
    ):
        """
        Inicializa o jogo com dependências injetadas.
        
        Args:
            screen: Superfície do pygame
            asset_manager: Gerenciador de assets (opcional, cria novo se None)
            particle_system: Sistema de partículas (opcional, cria novo se None)
            phase_manager: Gerenciador de fases (opcional, cria novo se None)
        """
        log_info("Initializing Game")
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        
        # Injeção de dependências (com fallback para compatibilidade)
        if asset_manager is None:
            asset_manager = AssetManager()
        if particle_system is None:
            particle_system = ParticleSystem()
        if phase_manager is None:
            phase_manager = PhaseManager(asset_manager, particle_system)
        
        self.assets = asset_manager
        self.particles = particle_system
        self.phase_manager = phase_manager
        self.hud = HUD(self.assets)
        from mygame.utils.config import LIGHT_GRAY, DARK_BLUE
        self.back_button = Button(
            rect=pygame.Rect(10, 10, 70, 35), text="Voltar",
            font=self.assets.fonts['back_button'], callback=self.go_to_main_menu, 
            bg_color=LIGHT_GRAY, text_color=DARK_BLUE, hover_sound=self.assets.sounds.get('ui_hover'), 
            click_sound=self.assets.sounds.get('ui_click')
        )
        
        self.screens: Dict[str, MenuScreen] = {}
        self.current_screen: Optional[MenuScreen] = None
        self.winner_message = ""
        self.winner_side = ""

        self.game_start_time = 0
        self.records = self.load_records()
        self.current_mode_key = ""
        self.assets.play_music()
        
        # Monitor de performance
        self.performance_monitor = PerformanceMonitor(track_fps=True)
        
        log_info("Game initialized successfully", records_count=len(self.records))

    def load_records(self) -> dict[str, int]:
        """
        Carrega os recordes salvos do arquivo.
        
        Returns:
            Dicionário com os recordes
            
        Raises:
            SaveDataError: Se houver erro ao carregar (mas retorna {} como fallback)
        """
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                records = data.get("records", {})
                log_info("Records loaded", file_path=SAVE_FILE, records_count=len(records))
                return records
        except FileNotFoundError:
            # Arquivo não existe ainda, retorna vazio
            log_info("Save file not found, starting with empty records", file_path=SAVE_FILE)
            return {}
        except json.JSONDecodeError as e:
            # Arquivo corrompido, loga erro mas continua com fallback
            log_warning(
                "Save file corrupted, using empty records",
                file_path=SAVE_FILE,
                error=str(e)
            )
            return {}
        except Exception as e:
            log_error(
                "Unexpected error loading save file",
                exception=e,
                file_path=SAVE_FILE
            )
            raise SaveDataError(f"Erro inesperado ao carregar save: {e}", SAVE_FILE) from e

    def save_records(self) -> None:
        """
        Salva os recordes no arquivo.
        
        Raises:
            SaveDataError: Se houver erro ao salvar
        """
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump({"records": self.records}, f, indent=2)
            log_info("Records saved", file_path=SAVE_FILE, records_count=len(self.records))
        except Exception as e:
            log_error(
                "Error saving records",
                exception=e,
                file_path=SAVE_FILE,
                records_count=len(self.records)
            )
            raise SaveDataError(f"Erro ao salvar recordes: {e}", SAVE_FILE) from e

    def go_to_main_menu(self) -> None:
        """Retorna ao menu principal."""
        log_info("Returning to main menu", previous_state=self.game_state.value)
        self.game_state = GameState.MENU
        self.current_screen = self.screens[MenuName.MAIN_MENU.value]
        set_context(game_state="menu")

    def start_game_mode(self, game_mode: str, ball_behavior: str) -> None:
        """
        Inicia um modo de jogo específico.
        
        Args:
            game_mode: Modo de jogo (validado)
            ball_behavior: Comportamento da bola (validado)
            
        Raises:
            InvalidGameModeError: Se o modo de jogo for inválido
            InvalidBallBehaviorError: Se o comportamento for inválido
        """
        # Fail fast: valida entradas
        validated_mode = validate_game_mode(game_mode)
        validated_behavior = validate_ball_behavior(ball_behavior)
        
        self.current_mode_key = f"{validated_mode}_{validated_behavior}"
        log_info(
            "Starting game mode",
            game_mode=validated_mode,
            ball_behavior=validated_behavior,
            mode_key=self.current_mode_key
        )
        
        self.phase_manager.start_new_progression(validated_mode, validated_behavior)
        
        if validated_mode == GameMode.SINGLEPLAYER.value:
            self.game_start_time = pygame.time.get_ticks()
            self.hud.reset_timer(SINGLEPLAYER_TIME_LIMIT_SECONDS)
            log_info(
                "Singleplayer mode started",
                time_limit=SINGLEPLAYER_TIME_LIMIT_SECONDS
            )
        
        self.game_state = GameState.PLAYING
        set_context(
            game_state="playing",
            game_mode=validated_mode,
            ball_behavior=validated_behavior
        )

    def run(self) -> None:
        """Loop principal do jogo."""
        running = True
        while running:
            # Atualiza monitor de performance
            self.performance_monitor.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == GameState.PLAYING:
                            self.go_to_main_menu()
                        else:
                            running = False
                elif self.game_state == GameState.MENU and self.current_screen:
                    self.current_screen.handle_events(event)
                elif self.game_state == GameState.PLAYING:
                    self.back_button.handle_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.phase_manager.handle_click(event.pos)
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
            # Loga performance se FPS baixo (apenas em DEBUG)
            self.performance_monitor.log_performance(min_fps=30.0)

    def handle_events(self) -> None:
        """Processa eventos do pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == GameState.MENU and self.current_screen:
                self.current_screen.handle_events(event)
            elif self.game_state == GameState.PLAYING:
                self.back_button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.phase_manager.handle_click(event.pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.go_to_main_menu()
            elif self.game_state in [GameState.END_SCREEN, GameState.SPLIT_VICTORY]:
                if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    self.go_to_main_menu()

    def update(self) -> None:
        """Atualiza o estado do jogo."""
        if self.game_state == GameState.MENU and self.current_screen:
            for btn in self.current_screen.buttons:
                btn.update()
            self.current_screen.background.update()
        elif self.game_state == GameState.PLAYING:
            self.phase_manager.update()
            self.back_button.update()
            self.particles.update()

            if self.phase_manager.game_mode == GameMode.SINGLEPLAYER.value:
                self.update_singleplayer()
            else:  # Multiplayer
                self.update_multiplayer()

    def update_singleplayer(self, current_time_ms: Optional[int] = None) -> None:
        """
        Atualiza a lógica do modo singleplayer.
        
        Args:
            current_time_ms: Tempo atual em milissegundos (opcional, usa pygame.time.get_ticks() se None)
                            Permite injeção de tempo para testabilidade
        """
        # Fail fast: valida que estamos no estado correto
        if self.game_state != GameState.PLAYING:
            return
        
        if current_time_ms is None:
            current_time_ms = pygame.time.get_ticks()
        
        time_elapsed = (current_time_ms - self.game_start_time) // 1000
        time_remaining = SINGLEPLAYER_TIME_LIMIT_SECONDS - time_elapsed
        self.hud.update(max(0, time_remaining))  # Garante não-negativo
        
        if time_remaining < 0:
            current_score = self.phase_manager.current_phase
            best_score = self.records.get(self.current_mode_key, 0)
            if current_score > best_score:
                self.records[self.current_mode_key] = current_score
                log_info(
                    "New record achieved",
                    mode_key=self.current_mode_key,
                    new_record=current_score,
                    previous_record=best_score
                )
                try:
                    self.save_records()
                except SaveDataError as e:
                    log_error(
                        "Failed to save new record",
                        exception=e,
                        mode_key=self.current_mode_key,
                        record=current_score
                    )
            else:
                log_info(
                    "Game ended",
                    mode_key=self.current_mode_key,
                    final_score=current_score,
                    best_score=best_score
                )
            self.winner_message = f"Tempo Esgotado! Fases: {current_score}"
            self.game_state = GameState.END_SCREEN
            set_context(game_state="end_screen")
            return
        
        is_complete, _ = self.phase_manager.is_phase_complete()
        if is_complete:
            if 'phase_win' in self.assets.sounds:
                self.assets.sounds['phase_win'].play()
            log_info(
                "Phase completed",
                phase=self.phase_manager.current_phase,
                time_remaining=time_remaining
            )
            self.phase_manager.load_next_phase()
            set_context(phase=self.phase_manager.current_phase)

    def update_multiplayer(self) -> None:
        """Atualiza a lógica do modo multiplayer."""
        is_complete, winner = self.phase_manager.is_phase_complete()
        if is_complete:
            if 'phase_win' in self.assets.sounds:
                self.assets.sounds['phase_win'].play()
            log_info(
                "Phase completed",
                phase=self.phase_manager.current_phase,
                winner=winner,
                p1_score=self.phase_manager.player_one_score,
                p2_score=self.phase_manager.player_two_score
            )
            self.phase_manager.update_score(winner)
            
            if self.phase_manager.is_progression_complete():
                self.winner_side = self.phase_manager.get_final_winner()
                log_info(
                    "Multiplayer progression complete",
                    winner=self.winner_side,
                    final_p1_score=self.phase_manager.player_one_score,
                    final_p2_score=self.phase_manager.player_two_score
                )
                self.game_state = GameState.SPLIT_VICTORY
                set_context(game_state="split_victory")
            else:
                self.phase_manager.load_next_phase()
                set_context(phase=self.phase_manager.current_phase)

    def draw(self) -> None:
        """Desenha o estado atual do jogo."""
        if self.game_state == GameState.MENU and self.current_screen:
            self.current_screen.draw()
        elif self.game_state == GameState.PLAYING:
            self.screen.fill(PLAYER_AREA_COLOR)
            if is_multiplayer_mode(self.phase_manager.game_mode):
                self._draw_multiplayer_divider()
            self.phase_manager.draw(self.screen)
            self.particles.draw(self.screen)
            self.hud.draw(
                self.screen, self.phase_manager.game_mode,
                self.phase_manager.current_phase,
                self.phase_manager.player_one_score,
                self.phase_manager.player_two_score
            )
            self.back_button.draw(self.screen)
        elif self.game_state == GameState.END_SCREEN:
            self.draw_end_screen()
        elif self.game_state == GameState.SPLIT_VICTORY:
            self.draw_split_victory_screen()
        
        # Atualiza a tela para exibir as mudanças
        pygame.display.flip()

    def _draw_multiplayer_divider(self) -> None:
        """Desenha a linha divisória e área do oponente no modo multiplayer."""
        screen_midpoint = SCREEN_HEIGHT // 2
        pygame.draw.rect(
            self.screen, OPPONENT_AREA_COLOR,
            (0, screen_midpoint, SCREEN_WIDTH, screen_midpoint)
        )
        pygame.draw.line(
            self.screen, GRAY,
            (0, screen_midpoint), (SCREEN_WIDTH, screen_midpoint),
            DIVIDER_LINE_WIDTH
        )
    
    def draw_end_screen(self) -> None:
        """Desenha a tela de fim de jogo."""
        end_menu = self.screens.get(MenuName.END_SCREEN.value)
        if end_menu:
            end_menu.title_surf = end_menu.title_font.render(
                self.winner_message, True, (203, 213, 225)
            )
            end_menu.title_rect = end_menu.title_surf.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            )
            end_menu.draw()
            
    def draw_split_victory_screen(self) -> None:
        """Desenha a tela de vitória/derrota dividida com base no vencedor geral."""
        player_one_message, player_two_message = self._get_victory_messages()
        self._render_player_area(player_one_message, 0, PLAYER_AREA_COLOR)
        self._render_player_area(player_two_message, SCREEN_HEIGHT // 2, OPPONENT_AREA_COLOR)
        self._render_divider_line()
    
    def _get_victory_messages(self) -> tuple[str, str]:
        """
        Determina as mensagens de vitória baseado no vencedor.
        
        Returns:
            Tupla (player_one_message, player_two_message)
        """
        final_winner = self.winner_side
        
        if final_winner == "Empate":
            return ("EMPATE!", "EMPATE!")
        elif final_winner == "Jogador 1":
            return ("VOCÊ VENCEU!", "VOCÊ PERDEU!")
        else:
            return ("VOCÊ PERDEU!", "VOCÊ VENCEU!")
    
    def _render_player_area(self, message: str, y_offset: int, bg_color: Color) -> None:
        """
        Renderiza a área de um jogador na tela de vitória.
        
        Args:
            message: Mensagem a exibir
            y_offset: Offset Y da área
            bg_color: Cor de fundo da área
        """
        area_rect = pygame.Rect(0, y_offset, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, bg_color, area_rect)
        
        text_surf = self.assets.fonts['title'].render(message, True, WHITE)
        text_rect = text_surf.get_rect(center=area_rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def _render_divider_line(self) -> None:
        """Renderiza a linha divisória na tela de vitória."""
        screen_midpoint = SCREEN_HEIGHT // 2
        pygame.draw.line(
            self.screen, GRAY,
            (0, screen_midpoint), (SCREEN_WIDTH, screen_midpoint),
            DIVIDER_LINE_WIDTH
        )

    def set_current_screen(self, screen_name: str) -> None:
        """Define a tela atual do jogo."""
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]