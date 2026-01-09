"""
Bolinha que é afetada pela gravidade e pula ao atingir o chão.
"""
from __future__ import annotations
import random
from mygame.entities.ball_base import Ball
from mygame.utils.config import BASE_GRAVITY, BASE_FREE_BALL_SPEED


class JumpBall(Ball):
    """Bolinha que é afetada pela gravidade e pula ao atingir o chão."""
    
    def __init__(
        self,
        *args,
        gravity: float = BASE_GRAVITY,
        speed: float = BASE_FREE_BALL_SPEED,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.vx = random.choice([-speed / 2, speed / 2, -speed / 3, speed / 3])
        self.vy = 0.0
        self.gravity = gravity
        
        # Cada bolinha tem sua própria força de pulo
        self.jump_strength = random.uniform(-10, -15)

    def _move(self) -> None:
        """Aplica gravidade e movimento, e verifica colisões."""
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= self.bounds[0] or self.x + self.radius >= self.bounds[1]:
            self.vx *= -1
            self.x = max(self.x, self.bounds[0] + self.radius)
            self.x = min(self.x, self.bounds[1] - self.radius)
        
        if self.y + self.radius >= self.bounds[3]:
            self.y = self.bounds[3] - self.radius
            self.vy = self.jump_strength  # Usa sua força de pulo individual

        if self.y - self.radius <= self.bounds[2]:
            self.y = self.bounds[2] + self.radius
            self.vy = 0
