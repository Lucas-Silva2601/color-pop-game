"""
Classe base abstrata para todas as bolinhas do jogo.
"""
from __future__ import annotations
import pygame
import random
from abc import ABC, abstractmethod
from mygame.utils.types import Color, Bounds, Position
from mygame.utils.config import BALL_RADIUS


class Ball(ABC):
    """Classe base para bolinhas, com animação de clique."""
    
    def __init__(
        self,
        color: Color,
        color_options: list[Color],
        bounds: Bounds,
        pop_sound: pygame.mixer.Sound | None,
        **kwargs
    ) -> None:
        self.radius = BALL_RADIUS
        self.x = random.randint(bounds[0] + self.radius, bounds[1] - self.radius)
        self.y = random.randint(bounds[2] + self.radius, bounds[3] - self.radius)
        
        self.color = color
        self.color1, self.color2 = color_options
        self.bounds = bounds
        self.pop_sound = pop_sound

        self.scale = 1.0
        self.is_animating = False
        self.animation_timer = 0
        self.animation_duration = 10

    def draw(self, screen: pygame.Surface) -> None:
        """Desenha a bola na tela."""
        current_radius = int(self.radius * self.scale)
        if current_radius > 0:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), current_radius
            )

    @abstractmethod
    def _move(self) -> None:
        """Método abstrato para movimento da bola. Deve ser implementado pelas subclasses."""
        pass

    def update(self) -> None:
        """Atualiza a posição e animação da bola."""
        self._move()
        if self.is_animating:
            self.animation_timer += 1
            if self.animation_timer < self.animation_duration / 2:
                self.scale -= 0.08
            else:
                self.scale += 0.08
            
            if self.animation_timer >= self.animation_duration:
                self.is_animating = False
                self.scale = 1.0

    def is_clicked(self, pos: Position) -> bool:
        """
        Verifica se a bola foi clicada na posição especificada.
        
        Args:
            pos: Posição do clique (x, y)
            
        Returns:
            True se a bola foi clicada
        """
        distance_sq = (self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2
        return distance_sq <= self.radius ** 2

    def switch_color(self) -> Color:
        """
        Alterna a cor, inicia a animação e retorna a cor anterior.
        
        Returns:
            Cor anterior da bola
        """
        previous_color = self.color
        self.color = self.color2 if self.color == self.color1 else self.color1
        if self.pop_sound:
            self.pop_sound.play()
        
        self.is_animating = True
        self.animation_timer = 0
        self.scale = 1.0
        return previous_color
