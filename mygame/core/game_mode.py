"""
Enums para modos de jogo e comportamentos de bola, eliminando strings mágicas.
"""
from enum import Enum


class GameMode(Enum):
    """Modos de jogo disponíveis."""
    SINGLEPLAYER = "singleplayer"
    PLAYER_VS_PLAYER = "pvp"
    PLAYER_VS_BOT = "pve"


class BallBehavior(Enum):
    """Comportamentos de bola disponíveis."""
    STATIONARY = "parado"
    FREE_MOVEMENT = "movimento"
    JUMPING = "saltitando"

