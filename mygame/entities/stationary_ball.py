"""
Bolinha estacionária que não se move.
"""
from __future__ import annotations
from mygame.entities.ball_base import Ball


class StationaryBall(Ball):
    """
    Uma bolinha que não se move. Sua única função é existir e
    ter sua cor trocada por um clique.
    """
    
    def __init__(self, *args, **kwargs) -> None:
        """
        Aceita **kwargs para ser compatível com o PhaseManager,
        que passa parâmetros de dificuldade como 'speed' e 'gravity',
        mas esta classe os ignora.
        """
        super().__init__(*args, **kwargs)

    def _move(self) -> None:
        """
        Esta bolinha é estacionária, então o método de atualização
        não faz nada.
        """
        pass
