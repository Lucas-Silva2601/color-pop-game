"""
Factory para criação de menus e botões, eliminando duplicação de código.
"""
from __future__ import annotations
import pygame
from typing import Callable
from mygame.ui.menu_screen import MenuScreen
from mygame.ui.button import Button
from mygame.ui.animated_background import BackgroundManager
from mygame.ui.menu_names import MenuName
from mygame.core.asset_manager import AssetManager
from mygame.utils.config import (
    SCREEN_WIDTH, CYAN, GRAY, WHITE, MAGENTA
)
from mygame.utils.types import Color
from mygame.utils.types import Color


# Constantes para botões
BUTTON_WIDTH: int = 280
BUTTON_HEIGHT: int = 60


def create_menu_button(
    text: str,
    y_position: int,
    callback: Callable[[], None],
    assets: AssetManager,
    bg_color: Color = CYAN
) -> Button:
    """
    Cria um botão de menu padronizado.
    
    Args:
        text: Texto do botão
        y_position: Posição Y do botão
        callback: Função a ser chamada ao clicar
        assets: Gerenciador de assets
        bg_color: Cor de fundo do botão
        
    Returns:
        Button configurado
    """
    button_x = (SCREEN_WIDTH - BUTTON_WIDTH) / 2
    return Button(
        pygame.Rect(button_x, y_position, BUTTON_WIDTH, BUTTON_HEIGHT),
        text,
        assets.fonts['button'],
        callback,
        bg_color=bg_color,
        hover_sound=assets.sounds.get('ui_hover'),
        click_sound=assets.sounds.get('ui_click')
    )


def create_main_menu(
    screen: pygame.Surface,
    assets: AssetManager,
    background: BackgroundManager,
    goto_menu_callback: Callable[[str], None]
) -> MenuScreen:
    """
    Cria o menu principal do jogo.
    
    Args:
        screen: Superfície do pygame
        assets: Gerenciador de assets
        background: Gerenciador de fundo animado
        goto_menu_callback: Função para navegar entre menus
        
    Returns:
        MenuScreen configurado
    """
    menu = MenuScreen(screen, "Color Pop", assets.fonts['title'], background)
    
    menu.add_button(create_menu_button(
        "Singleplayer",
        220,
        lambda: goto_menu_callback(MenuName.SINGLEPLAYER_MENU.value),
        assets
    ))
    
    menu.add_button(create_menu_button(
        "Player vs Player",
        300,
        lambda: goto_menu_callback(MenuName.PLAYER_VS_PLAYER_MENU.value),
        assets
    ))
    
    menu.add_button(create_menu_button(
        "Player vs Bot",
        380,
        lambda: goto_menu_callback(MenuName.PLAYER_VS_BOT_MENU.value),
        assets
    ))
    
    return menu


def create_singleplayer_menu(
    screen: pygame.Surface,
    assets: AssetManager,
    background: BackgroundManager,
    game_records: dict,
    start_mode_callback: Callable[[str, str], None],
    goto_menu_callback: Callable[[str], None]
) -> MenuScreen:
    """
    Cria o menu de singleplayer com recordes.
    
    Args:
        screen: Superfície do pygame
        assets: Gerenciador de assets
        background: Gerenciador de fundo animado
        game_records: Dicionário com recordes do jogo
        start_mode_callback: Função para iniciar modo de jogo
        goto_menu_callback: Função para navegar entre menus
        
    Returns:
        MenuScreen configurado
    """
    from mygame.core.game_mode import BallBehavior
    
    menu = MenuScreen(screen, "Singleplayer", assets.fonts['title'], background)
    record_font = assets.fonts['back_button']
    
    # Botão Parado
    record_parado = game_records.get("singleplayer_parado", 0)
    parado_btn = create_menu_button(
        "Parado",
        220,
        lambda: start_mode_callback("singleplayer", BallBehavior.STATIONARY.value),
        assets
    )
    parado_record_surf = record_font.render(f"Recorde: {record_parado} fases", True, WHITE)
    parado_record_rect = parado_record_surf.get_rect(midtop=parado_btn.base_rect.midbottom)
    menu.add_button(parado_btn)
    menu.add_text(parado_record_surf, parado_record_rect)
    
    # Botão Movimento
    record_mov = game_records.get("singleplayer_movimento", 0)
    mov_btn = create_menu_button(
        "Movimento",
        320,
        lambda: start_mode_callback("singleplayer", BallBehavior.FREE_MOVEMENT.value),
        assets
    )
    mov_record_surf = record_font.render(f"Recorde: {record_mov} fases", True, WHITE)
    mov_record_rect = mov_record_surf.get_rect(midtop=mov_btn.base_rect.midbottom)
    menu.add_button(mov_btn)
    menu.add_text(mov_record_surf, mov_record_rect)
    
    # Botão Saltitando
    record_salt = game_records.get("singleplayer_saltitando", 0)
    salt_btn = create_menu_button(
        "Saltitando",
        420,
        lambda: start_mode_callback("singleplayer", BallBehavior.JUMPING.value),
        assets
    )
    salt_record_surf = record_font.render(f"Recorde: {record_salt} fases", True, WHITE)
    salt_record_rect = salt_record_surf.get_rect(midtop=salt_btn.base_rect.midbottom)
    menu.add_button(salt_btn)
    menu.add_text(salt_record_surf, salt_record_rect)
    
    # Botão Voltar
    menu.add_button(create_menu_button(
        "Voltar",
        520,
        lambda: goto_menu_callback(MenuName.MAIN_MENU.value),
        assets,
        bg_color=GRAY
    ))
    
    return menu


def create_multiplayer_menu(
    screen: pygame.Surface,
    assets: AssetManager,
    background: BackgroundManager,
    title: str,
    game_mode: str,
    start_mode_callback: Callable[[str, str], None],
    goto_menu_callback: Callable[[str], None],
    bg_color: Color | None = None
) -> MenuScreen:
    """
    Cria um menu multiplayer (PvP ou PvE).
    
    Args:
        screen: Superfície do pygame
        assets: Gerenciador de assets
        background: Gerenciador de fundo animado
        title: Título do menu
        game_mode: Modo de jogo ("pvp" ou "pve")
        start_mode_callback: Função para iniciar modo de jogo
        goto_menu_callback: Função para navegar entre menus
        bg_color: Cor de fundo dos botões (padrão: MAGENTA)
        
    Returns:
        MenuScreen configurado
    """
    from mygame.core.game_mode import BallBehavior
    from mygame.utils.config import MAGENTA
    
    if bg_color is None:
        bg_color = MAGENTA
    
    menu = MenuScreen(screen, title, assets.fonts['title'], background)
    
    menu.add_button(create_menu_button(
        "Parado",
        220,
        lambda: start_mode_callback(game_mode, BallBehavior.STATIONARY.value),
        assets,
        bg_color=bg_color
    ))
    
    menu.add_button(create_menu_button(
        "Movimento",
        300,
        lambda: start_mode_callback(game_mode, BallBehavior.FREE_MOVEMENT.value),
        assets,
        bg_color=bg_color
    ))
    
    menu.add_button(create_menu_button(
        "Saltitando",
        380,
        lambda: start_mode_callback(game_mode, BallBehavior.JUMPING.value),
        assets,
        bg_color=bg_color
    ))
    
    menu.add_button(create_menu_button(
        "Voltar",
        500,
        lambda: goto_menu_callback(MenuName.MAIN_MENU.value),
        assets,
        bg_color=GRAY
    ))
    
    return menu


def create_end_screen(
    screen: pygame.Surface,
    assets: AssetManager,
    background: BackgroundManager,
    goto_menu_callback: Callable[[str], None]
) -> MenuScreen:
    """
    Cria a tela de fim de jogo.
    
    Args:
        screen: Superfície do pygame
        assets: Gerenciador de assets
        background: Gerenciador de fundo animado
        goto_menu_callback: Função para navegar entre menus
        
    Returns:
        MenuScreen configurado
    """
    menu = MenuScreen(screen, "", assets.fonts['title'], background)
    menu.add_button(create_menu_button(
        "Voltar ao Menu",
        450,
        lambda: goto_menu_callback(MenuName.MAIN_MENU.value),
        assets,
        bg_color=GRAY
    ))
    return menu

