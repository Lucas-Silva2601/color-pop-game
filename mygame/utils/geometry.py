"""
Funções utilitárias para cálculos geométricos e posicionamento.
"""
from __future__ import annotations
from mygame.utils.types import Bounds, Position, Color
from mygame.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS


def calculate_centered_position(
    width: int, height: int, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT
) -> Position:
    """
    Calcula posição centralizada para um elemento.
    
    Args:
        width: Largura do elemento
        height: Altura do elemento
        screen_width: Largura da tela
        screen_height: Altura da tela
        
    Returns:
        Tupla (x, y) com posição centralizada
    """
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    return Position((int(x), int(y)))


def calculate_bounds_for_singleplayer() -> Bounds:
    """
    Calcula os bounds para modo singleplayer (tela inteira).
    
    Returns:
        Bounds (x_min, x_max, y_min, y_max)
    """
    return Bounds((0, SCREEN_WIDTH, 0, SCREEN_HEIGHT))


def calculate_bounds_for_multiplayer() -> tuple[Bounds, Bounds]:
    """
    Calcula os bounds para modo multiplayer (área dividida).
    
    Returns:
        Tupla (player_one_bounds, player_two_bounds)
    """
    screen_midpoint = SCREEN_HEIGHT // 2
    player_one_bounds = Bounds((0, SCREEN_WIDTH, 0, screen_midpoint))
    player_two_bounds = Bounds((0, SCREEN_WIDTH, screen_midpoint, SCREEN_HEIGHT))
    return player_one_bounds, player_two_bounds


def calculate_distance_squared(pos1: Position, pos2: Position) -> float:
    """
    Calcula a distância ao quadrado entre duas posições (mais eficiente que distância).
    
    Args:
        pos1: Primeira posição (x, y)
        pos2: Segunda posição (x, y)
        
    Returns:
        Distância ao quadrado
    """
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return dx * dx + dy * dy


def is_position_in_bounds(pos: Position, bounds: Bounds) -> bool:
    """
    Verifica se uma posição está dentro dos bounds.
    
    Args:
        pos: Posição (x, y)
        bounds: Bounds (x_min, x_max, y_min, y_max)
        
    Returns:
        True se a posição está dentro dos bounds
    """
    x, y = pos
    return bounds[0] <= x <= bounds[1] and bounds[2] <= y <= bounds[3]

