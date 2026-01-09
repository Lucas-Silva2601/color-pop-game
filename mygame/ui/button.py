"""
Componente de botão interativo com animação e feedback sonoro.
"""
from __future__ import annotations
import pygame
from typing import Callable
from mygame.utils.types import Color


class Button:
    """
    Uma classe de botão aprimorada com animação de escala e feedback sonoro.
    """
    
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        callback: Callable[[], None],
        bg_color: Color = (34, 211, 238),  # Cyan
        hover_color: Color = (236, 72, 153),  # Magenta
        text_color: Color = (15, 23, 42),  # Dark Blue
        hover_sound: pygame.mixer.Sound | None = None,
        click_sound: pygame.mixer.Sound | None = None
    ) -> None:
        self.base_rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        
        self.is_hovered = False
        self.played_hover_sound = False
        
        # Atributos para animação
        self.scale = 1.0
        self.target_scale = 1.0
        from mygame.utils.config import BUTTON_ANIMATION_SPEED
        self.animation_speed = BUTTON_ANIMATION_SPEED
        
        # Cache de renderização
        self._cached_rect: pygame.Rect | None = None
        self._cached_scale: float = -1.0
        self._cached_text_surf: pygame.Surface | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Processa eventos de mouse para o botão.
        
        Args:
            event: Evento do pygame
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.base_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                if self.click_sound:
                    self.click_sound.play()
                self.callback()

    def update(self) -> None:
        """Atualiza a animação de escala do botão."""
        self.target_scale = 1.05 if self.is_hovered else 1.0
        self.scale += (self.target_scale - self.scale) * self.animation_speed
        
        if self.is_hovered and not self.played_hover_sound:
            if self.hover_sound:
                self.hover_sound.play()
            self.played_hover_sound = True
        elif not self.is_hovered:
            self.played_hover_sound = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o botão com sua escala atual.
        Usa cache para evitar recálculos desnecessários.
        
        Args:
            screen: Superfície do pygame
        """
        # Recalcula apenas se scale ou hover mudou
        if self.scale != self._cached_scale or self._cached_rect is None:
            current_width = int(self.base_rect.width * self.scale)
            current_height = int(self.base_rect.height * self.scale)
            self._cached_rect = pygame.Rect(0, 0, current_width, current_height)
            self._cached_rect.center = self.base_rect.center
            self._cached_scale = self.scale
            
            # Recria text surface apenas se necessário
            self._cached_text_surf = None
        
        current_rect = self._cached_rect
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Sombra sutil
        shadow_rect = current_rect.copy()
        shadow_rect.move_ip(0, 3)
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=15)

        pygame.draw.rect(screen, color, current_rect, border_radius=12)
        
        # Cache de text surface
        if self._cached_text_surf is None:
            self._cached_text_surf = self.font.render(self.text, True, self.text_color)
        
        text_rect = self._cached_text_surf.get_rect(center=current_rect.center)
        screen.blit(self._cached_text_surf, text_rect)
