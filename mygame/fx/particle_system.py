"""
Sistema de partículas para efeitos visuais.
Otimizado com object pooling e limite de partículas.
"""
from __future__ import annotations
import pygame
import random
import math
from typing import List
from mygame.utils.types import Color
from mygame.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT
from mygame.utils.object_pool import ObjectPool


class Particle:
    """Representa uma partícula individual."""
    
    __slots__ = ('x', 'y', 'vx', 'vy', 'color', 'life', 'max_life', 'size')
    
    def __init__(self, x: float = 0.0, y: float = 0.0, color: Color = (255, 255, 255)) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.color = color
        self.life = 1.0
        self.max_life = 1.0
        self.size = 3
    
    def reset(self, x: float, y: float, color: Color) -> None:
        """
        Reseta a partícula para reutilização.
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            color: Cor da partícula
        """
        self.x = x
        self.y = y
        self.color = color
        self.life = 1.0
        self.max_life = 1.0
        self.size = random.randint(2, 4)
        
        # Velocidade aleatória
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.0, 3.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
    
    def update(self) -> bool:
        """
        Atualiza a partícula.
        
        Returns:
            True se a partícula ainda está viva, False se deve ser removida
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravidade
        self.life -= 0.02
        
        return self.life > 0 and 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT
    
    def draw(self, screen: pygame.Surface) -> None:
        """Desenha a partícula na tela."""
        alpha = int(255 * self.life)
        color_with_alpha = (*self.color, alpha)
        
        # Cria surface temporária com alpha
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    """
    Sistema de partículas otimizado com object pooling e limite máximo.
    """
    
    MAX_PARTICLES: int = 200  # Limite máximo de partículas ativas
    
    def __init__(self) -> None:
        self.particles: List[Particle] = []
        self._pool = ObjectPool(
            factory=lambda: Particle(),
            initial_size=20,
            max_size=ParticleSystem.MAX_PARTICLES
        )
    
    def emit(self, x: float, y: float, color: Color, count: int = 10) -> None:
        """
        Emite partículas em uma posição.
        
        Args:
            x: Posição X
            y: Posição Y
            color: Cor das partículas
            count: Número de partículas a emitir
        """
        # Limita o número de partículas a emitir baseado no espaço disponível
        available_slots = self.MAX_PARTICLES - len(self.particles)
        actual_count = min(count, available_slots)
        
        if actual_count <= 0:
            return  # Não há espaço para novas partículas
        
        for _ in range(actual_count):
            particle = self._pool.acquire()
            particle.reset(x, y, color)
            self.particles.append(particle)
    
    def update(self) -> None:
        """Atualiza todas as partículas e remove as mortas."""
        dead_particles: List[Particle] = []
        
        for particle in self.particles:
            if not particle.update():
                dead_particles.append(particle)
        
        # Libera partículas mortas de volta ao pool
        for particle in dead_particles:
            self.particles.remove(particle)
            self._pool.release(particle)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Desenha todas as partículas na tela."""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self) -> None:
        """Limpa todas as partículas."""
        for particle in self.particles:
            self._pool.release(particle)
        self.particles.clear()
