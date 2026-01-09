"""
HUD (Heads-Up Display) para exibir informações do jogo na tela.
"""
from __future__ import annotations
import pygame
from mygame.core.asset_manager import AssetManager
from mygame.core.game_mode import GameMode
from mygame.utils.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, CYAN, MAGENTA,
    MULTIPLAYER_PHASE_LIMIT, HUD_TIMER_WARNING_THRESHOLD
)


class HUD:
    """Gerencia a exibição de informações do jogo (fase, timer, placar)."""
    
    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self.phase_font = self.assets.fonts['hud_phase']
        self.timer_font = self.assets.fonts['hud_timer']
        self.score_font = self.assets.fonts['button']  # Reutilizando uma fonte
        self.time_remaining = 0

    def update(self, time_remaining: int) -> None:
        """Atualiza o tempo restante."""
        self.time_remaining = time_remaining

    def reset_timer(self, start_time: int) -> None:
        """Reseta o timer para um valor inicial."""
        self.time_remaining = start_time

    def draw(
        self,
        screen: pygame.Surface,
        game_mode: str,
        phase_number: int,
        player_one_score: int = 0,
        player_two_score: int = 0
    ) -> None:
        """
        Desenha o HUD apropriado baseado no modo de jogo.
        
        Args:
            screen: Superfície do pygame
            game_mode: Modo de jogo atual
            phase_number: Número da fase atual
            player_one_score: Score do jogador 1 (multiplayer)
            player_two_score: Score do jogador 2 (multiplayer)
        """
        if game_mode == GameMode.SINGLEPLAYER.value:
            self.draw_singleplayer_hud(screen, phase_number)
        else:
            self.draw_multiplayer_hud(screen, phase_number, player_one_score, player_two_score)

    def draw_singleplayer_hud(self, screen: pygame.Surface, phase_number: int) -> None:
        """
        Desenha o HUD para modo singleplayer (timer + fase).
        
        Args:
            screen: Superfície do pygame
            phase_number: Número da fase atual
        """
        minutes, seconds = divmod(max(0, self.time_remaining), 60)
        timer_text_str = f"{minutes:02}:{seconds:02}"
        
        # Pisca vermelho quando tempo está acabando
        time_color = (
            RED if self.time_remaining <= HUD_TIMER_WARNING_THRESHOLD and pygame.time.get_ticks() % 1000 > 500
            else WHITE
        )
        
        timer_text = self.timer_font.render(timer_text_str, True, time_color)
        # Posiciona o timer à direita da tela
        timer_rect = timer_text.get_rect(midright=(SCREEN_WIDTH - 15, 27))
        screen.blit(timer_text, timer_rect)
        
        phase_text = self.phase_font.render(f"Fase: {phase_number}", True, WHITE)
        phase_rect = phase_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(phase_text, phase_rect)

    def draw_multiplayer_hud(
        self,
        screen: pygame.Surface,
        phase_number: int,
        player_one_score: int,
        player_two_score: int
    ) -> None:
        """
        Desenha o HUD para modo multiplayer (fase + placar).
        
        Args:
            screen: Superfície do pygame
            phase_number: Número da fase atual
            player_one_score: Score do jogador 1
            player_two_score: Score do jogador 2
        """
        # Fase (Ex: Fase 3/10)
        phase_text = self.phase_font.render(
            f"Fase: {phase_number}/{MULTIPLAYER_PHASE_LIMIT}", True, WHITE
        )
        phase_rect = phase_text.get_rect(midtop=(SCREEN_WIDTH / 2, 10))
        screen.blit(phase_text, phase_rect)

        # Placar (Ex: J1: 2 vs J2: 1)
        player_one_text = self.score_font.render(f"J1: {player_one_score}", True, CYAN)
        player_two_text = self.score_font.render(f"J2: {player_two_score}", True, MAGENTA)
        
        screen.blit(player_one_text, (20, SCREEN_HEIGHT // 2 - 50))
        screen.blit(player_two_text, (20, SCREEN_HEIGHT // 2 + 20))
