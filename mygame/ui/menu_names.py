"""
Constantes para identificadores de menus, eliminando strings mágicas.
"""
from enum import Enum


class MenuName(Enum):
    """Identificadores de menus do jogo."""
    MAIN_MENU = "main_menu"
    SINGLEPLAYER_MENU = "sp_menu"
    PLAYER_VS_PLAYER_MENU = "pvp_menu"
    PLAYER_VS_BOT_MENU = "pve_menu"
    END_SCREEN = "end_screen"

