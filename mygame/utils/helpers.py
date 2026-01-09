"""
Funções utilitárias gerais para o jogo.
"""
from __future__ import annotations
from mygame.core.game_mode import GameMode


def is_multiplayer_mode(game_mode: str) -> bool:
    """
    Verifica se um modo de jogo é multiplayer.
    
    Args:
        game_mode: String do modo de jogo
        
    Returns:
        True se for modo multiplayer (PvP ou PvE)
    """
    return game_mode in [GameMode.PLAYER_VS_PLAYER.value, GameMode.PLAYER_VS_BOT.value]


def is_singleplayer_mode(game_mode: str) -> bool:
    """
    Verifica se um modo de jogo é singleplayer.
    
    Args:
        game_mode: String do modo de jogo
        
    Returns:
        True se for modo singleplayer
    """
    return game_mode == GameMode.SINGLEPLAYER.value

