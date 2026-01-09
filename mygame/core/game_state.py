"""
Enum para estados do jogo, eliminando strings mágicas.
"""
from enum import Enum


class GameState(Enum):
    """Estados possíveis do jogo."""
    MENU = "menu"
    PLAYING = "playing"
    END_SCREEN = "end_screen"
    SPLIT_VICTORY = "split_victory"

