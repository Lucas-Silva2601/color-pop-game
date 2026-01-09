"""
Factory para criação de bolas, encapsulando a lógica de instanciação.
"""
from __future__ import annotations
import random
from typing import Type
from mygame.entities.ball_base import Ball
from mygame.entities.ball_free import FreeBall
from mygame.entities.ball_jump import JumpBall
from mygame.entities.stationary_ball import StationaryBall
from mygame.core.game_mode import BallBehavior
from mygame.utils.types import Color, Bounds, Position
from mygame.utils.config import BALL_RADIUS


class BallFactory:
    """Factory para criar instâncias de bolas."""
    
    # Mapeamento de comportamentos para classes
    _BALL_CLASSES: dict[str, Type[Ball]] = {
        BallBehavior.STATIONARY.value: StationaryBall,
        BallBehavior.FREE_MOVEMENT.value: FreeBall,
        BallBehavior.JUMPING.value: JumpBall,
    }
    
    @classmethod
    def create_ball(
        cls,
        behavior: str,
        color: Color,
        color_options: list[Color],
        bounds: Bounds,
        position: Position | None = None,
        **params
    ) -> Ball:
        """
        Cria uma instância de bola baseada no comportamento especificado.
        
        Args:
            behavior: Comportamento da bola (validado)
            color: Cor inicial da bola
            color_options: Lista de cores disponíveis
            bounds: Limites da área da bola
            position: Posição inicial (opcional, será aleatória se None)
            **params: Parâmetros adicionais (speed, gravity, pop_sound, etc)
            
        Returns:
            Instância de Ball configurada
        """
        ball_class = cls._BALL_CLASSES.get(behavior, StationaryBall)
        
        # Se posição não for fornecida, gera aleatória dentro dos bounds
        if position is None:
            x = random.randint(bounds[0] + BALL_RADIUS, bounds[1] - BALL_RADIUS)
            y = random.randint(bounds[2] + BALL_RADIUS, bounds[3] - BALL_RADIUS)
            position = Position((x, y))
        
        # Remove pop_sound de params para evitar duplicação (já passamos como argumento posicional)
        params_without_pop_sound = {k: v for k, v in params.items() if k != 'pop_sound'}
        ball = ball_class(color, color_options, bounds, params.get('pop_sound'), **params_without_pop_sound)
        ball.x, ball.y = position
        return ball
    
    @classmethod
    def get_ball_class(cls, behavior: str) -> Type[Ball]:
        """
        Retorna a classe de bola para um comportamento.
        
        Args:
            behavior: Comportamento da bola
            
        Returns:
            Classe de bola correspondente
        """
        return cls._BALL_CLASSES.get(behavior, StationaryBall)

