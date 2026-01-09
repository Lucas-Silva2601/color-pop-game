"""
Fundo animado para telas de menu com bolinhas decorativas.
"""
from __future__ import annotations
import pygame
import random
from typing import List
from mygame.utils.types import Color
from mygame.utils.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS_PASTEL, DECORATIVE_BALL_COUNT,
    DECORATIVE_BALL_MIN_SPEED, DECORATIVE_BALL_MAX_SPEED, DARK_BLUE
)


class DecorativeBall:
    """Uma bolinha decorativa que se move lentamente e tem transparência."""
    
    def __init__(self) -> None:
        self.radius = random.randint(10, 40)
        self.x = random.uniform(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.uniform(self.radius, SCREEN_HEIGHT - self.radius)
        self.color: Color = random.choice(COLORS_PASTEL)
        
        speed = random.uniform(DECORATIVE_BALL_MIN_SPEED, DECORATIVE_BALL_MAX_SPEED)
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1])
        
        self.alpha = random.randint(30, 100)
        self.surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.surface, (*self.color, self.alpha),
            (self.radius, self.radius), self.radius
        )

    def update(self) -> None:
        """Move e quica a bolinha decorativa."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.vy *= -1

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a bolinha na tela.
        
        Args:
            screen: Superfície do pygame
        """
        screen.blit(self.surface, (int(self.x - self.radius), int(self.y - self.radius)))


class BackgroundManager:
    """Gerencia a criação e animação do fundo da tela de menu."""
    
    def __init__(self) -> None:
        self.balls: List[DecorativeBall] = [
            DecorativeBall() for _ in range(DECORATIVE_BALL_COUNT)
        ]

    def update(self) -> None:
        """Atualiza todas as bolinhas decorativas."""
        for ball in self.balls:
            ball.update()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o fundo e todas as bolinhas decorativas.
        
        Args:
            screen: Superfície do pygame
        """
        screen.fill(DARK_BLUE)  # Cor de fundo
        for ball in self.balls:
            ball.draw(screen)
