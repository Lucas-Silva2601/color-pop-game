"""
Funções de validação para garantir dados válidos e implementar fail fast.
"""
from __future__ import annotations
from mygame.utils.types import Color, Bounds, Position
from mygame.utils.exceptions import (
    InvalidGameModeError,
    InvalidBallBehaviorError,
    InvalidConfigurationError,
    AssetNotFoundError
)
from mygame.core.game_mode import GameMode, BallBehavior
import os


def validate_positive_int(value: int, name: str) -> int:
    """
    Valida que um inteiro é positivo.
    
    Args:
        value: Valor a validar
        name: Nome do parâmetro para mensagem de erro
        
    Returns:
        Valor validado
        
    Raises:
        ValueError: Se o valor não for positivo
    """
    if value <= 0:
        raise ValueError(f"{name} deve ser um inteiro positivo, recebido: {value}")
    return value


def validate_non_negative_int(value: int, name: str) -> int:
    """
    Valida que um inteiro é não-negativo.
    
    Args:
        value: Valor a validar
        name: Nome do parâmetro para mensagem de erro
        
    Returns:
        Valor validado
        
    Raises:
        ValueError: Se o valor for negativo
    """
    if value < 0:
        raise ValueError(f"{name} deve ser um inteiro não-negativo, recebido: {value}")
    return value


def validate_color(color: tuple[int, ...]) -> Color:
    """
    Valida que uma tupla representa uma cor RGB válida.
    
    Args:
        color: Tupla de cor a validar
        
    Returns:
        Color validada
        
    Raises:
        ValueError: Se a cor não for válida
    """
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError(f"Cor deve ser uma tupla de 3 inteiros, recebido: {color}")
    
    r, g, b = color
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Valores RGB devem estar entre 0 e 255, recebido: {color}")
    
    return Color((r, g, b))


def validate_bounds(bounds: tuple[int, ...]) -> Bounds:
    """
    Valida que uma tupla representa bounds válidos.
    
    Args:
        bounds: Tupla de bounds a validar (x_min, x_max, y_min, y_max)
        
    Returns:
        Bounds validados
        
    Raises:
        ValueError: Se os bounds não forem válidos
    """
    if not isinstance(bounds, tuple) or len(bounds) != 4:
        raise ValueError(f"Bounds deve ser uma tupla de 4 inteiros, recebido: {bounds}")
    
    x_min, x_max, y_min, y_max = bounds
    
    if x_min >= x_max or y_min >= y_max:
        raise ValueError(
            f"Bounds inválidos: x_min ({x_min}) deve ser < x_max ({x_max}), "
            f"y_min ({y_min}) deve ser < y_max ({y_max})"
        )
    
    return Bounds((x_min, x_max, y_min, y_max))


def validate_position(pos: tuple[int, ...]) -> Position:
    """
    Valida que uma tupla representa uma posição válida.
    
    Args:
        pos: Tupla de posição a validar (x, y)
        
    Returns:
        Position validada
        
    Raises:
        ValueError: Se a posição não for válida
    """
    if not isinstance(pos, tuple) or len(pos) != 2:
        raise ValueError(f"Posição deve ser uma tupla de 2 inteiros, recebido: {pos}")
    
    x, y = pos
    return Position((x, y))


def validate_game_mode(mode: str) -> str:
    """
    Valida que um modo de jogo é válido.
    
    Args:
        mode: String do modo de jogo
        
    Returns:
        Modo validado
        
    Raises:
        InvalidGameModeError: Se o modo não for válido
    """
    valid_modes = {mode.value for mode in GameMode}
    if mode not in valid_modes:
        raise InvalidGameModeError(mode)
    return mode


def validate_ball_behavior(behavior: str) -> str:
    """
    Valida que um comportamento de bola é válido.
    
    Args:
        behavior: String do comportamento
        
    Returns:
        Comportamento validado
        
    Raises:
        InvalidBallBehaviorError: Se o comportamento não for válido
    """
    valid_behaviors = {behavior.value for behavior in BallBehavior}
    if behavior not in valid_behaviors:
        raise InvalidBallBehaviorError(behavior)
    return behavior


def validate_file_exists(file_path: str, file_type: str = "arquivo") -> str:
    """
    Valida que um arquivo existe.
    
    Args:
        file_path: Caminho do arquivo
        file_type: Tipo do arquivo para mensagem de erro
        
    Returns:
        Caminho validado
        
    Raises:
        AssetNotFoundError: Se o arquivo não existir
    """
    if not os.path.exists(file_path):
        raise AssetNotFoundError(file_path)
    return file_path


def validate_phase_number(phase: int) -> int:
    """
    Valida que um número de fase é válido.
    
    Args:
        phase: Número da fase
        
    Returns:
        Fase validada
        
    Raises:
        ValueError: Se a fase não for válida
    """
    if phase < 1:
        raise ValueError(f"Fase deve ser >= 1, recebido: {phase}")
    return phase


def validate_score(score: int) -> int:
    """
    Valida que um score é válido (não-negativo).
    
    Args:
        score: Score a validar
        
    Returns:
        Score validado
        
    Raises:
        ValueError: Se o score for negativo
    """
    return validate_non_negative_int(score, "Score")

