"""
Type aliases e dataclasses para tipagem forte do projeto.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import TypedDict


# ============================================================================
# TYPE ALIASES
# ============================================================================

Color = tuple[int, int, int]
"""Tipo para cores RGB (r, g, b)."""

Bounds = tuple[int, int, int, int]
"""Tipo para limites (x_min, x_max, y_min, y_max)."""

Position = tuple[int, int]
"""Tipo para posição (x, y)."""


# ============================================================================
# TYPED DICTS
# ============================================================================

class SaveDataDict(TypedDict):
    """Estrutura do arquivo de save."""
    records: dict[str, int]


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class PhaseParameters:
    """Parâmetros calculados para uma fase."""
    num_balls: int
    speed: float
    gravity: float
    pop_sound: object  # pygame.mixer.Sound | None


@dataclass
class BallCreationParams:
    """Parâmetros para criação de uma bola."""
    speed: float
    gravity: float
    pop_sound: object  # pygame.mixer.Sound | None


@dataclass
class GameSettings:
    """Configurações gerais do jogo."""
    screen_width: int
    screen_height: int
    fps: int
    singleplayer_time_limit: int
    multiplayer_phase_limit: int

