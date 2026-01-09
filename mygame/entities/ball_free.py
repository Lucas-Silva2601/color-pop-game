"""
Bolinha que se move livremente pela tela e quica nas bordas.
"""
from __future__ import annotations
import random
from mygame.entities.ball_base import Ball
from mygame.utils.config import BASE_FREE_BALL_SPEED


class FreeBall(Ball):
    """Bolinha que se move livremente pela tela e quica nas bordas."""
    
    def __init__(self, *args, speed: float = BASE_FREE_BALL_SPEED, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        # Garante que a velocidade não seja zero em nenhum eixo
        vx_options = [-speed, speed, -speed * 0.7, speed * 0.7]
        vy_options = [-speed, speed, -speed * 0.7, speed * 0.7]
        self.vx = random.choice(vx_options)
        self.vy = random.choice(vy_options)

    def _move(self) -> None:
        """Move a bolinha e verifica colisões com as bordas."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= self.bounds[0] or self.x + self.radius >= self.bounds[1]:
            self.vx *= -1
            self.x = max(self.x, self.bounds[0] + self.radius)
            self.x = min(self.x, self.bounds[1] - self.radius)
        if self.y - self.radius <= self.bounds[2] or self.y + self.radius >= self.bounds[3]:
            self.vy *= -1
            self.y = max(self.y, self.bounds[2] + self.radius)
            self.y = min(self.y, self.bounds[3] - self.radius)
