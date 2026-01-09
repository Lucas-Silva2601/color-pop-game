"""
Tela de menu com botões e textos customizáveis.
"""
from __future__ import annotations
import pygame
from mygame.ui.button import Button
from mygame.ui.animated_background import BackgroundManager


class MenuScreen:
    """Gerencia uma tela de menu com botões e textos."""
    
    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        title_font: pygame.font.Font,
        background: BackgroundManager
    ) -> None:
        self.screen = screen
        self.title_text = title
        self.title_font = title_font
        self.background = background
        self.buttons: list[Button] = []
        self.extra_texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        
        self.title_surf = self.title_font.render(self.title_text, True, (203, 213, 225))
        self.title_rect = self.title_surf.get_rect(
            center=(screen.get_width() / 2, 120)
        )

    def add_button(self, button: Button) -> None:
        """
        Adiciona um botão à tela.
        
        Args:
            button: Botão a ser adicionado
        """
        self.buttons.append(button)

    def add_text(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Adiciona um texto extra para ser desenhado na tela.
        
        Args:
            surface: Superfície com o texto renderizado
            rect: Retângulo com a posição do texto
        """
        self.extra_texts.append((surface, rect))

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Processa eventos para todos os botões.
        
        Args:
            event: Evento do pygame
        """
        for button in self.buttons:
            button.handle_event(event)

    def draw(self) -> None:
        """Desenha a tela de menu completa."""
        self.background.update()
        self.background.draw(self.screen)
        
        self.screen.blit(self.title_surf, self.title_rect)
        
        for button in self.buttons:
            button.update()
            button.draw(self.screen)
            
        for surf, rect in self.extra_texts:
            self.screen.blit(surf, rect)
