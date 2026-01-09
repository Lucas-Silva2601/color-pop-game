"""
Ponto de entrada principal do jogo Color Pop.
"""
from __future__ import annotations
import pygame
from mygame.core.game import Game
from mygame.core.factories import create_game_instance
from mygame.core.asset_manager import AssetManager
from mygame.ui.animated_background import BackgroundManager
from mygame.ui.menu_factory import (
    create_main_menu,
    create_singleplayer_menu,
    create_multiplayer_menu,
    create_end_screen
)
from mygame.ui.menu_names import MenuName
from mygame.core.game_mode import GameMode
from mygame.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION


def initialize_pygame() -> pygame.Surface:
    """
    Inicializa o pygame e retorna a superfície da tela.
    
    Returns:
        Superfície do pygame configurada
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    return screen


def create_all_menus(
    screen: pygame.Surface,
    assets: AssetManager,
    background: BackgroundManager,
    game: Game
) -> dict:
    """
    Cria todos os menus do jogo.
    
    Args:
        screen: Superfície do pygame
        assets: Gerenciador de assets
        background: Gerenciador de fundo animado
        game: Instância do jogo
        
    Returns:
        Dicionário com todos os menus criados
    """
    def start_mode(game_mode: str, behavior: str) -> None:
        """Callback para iniciar um modo de jogo."""
        game.start_game_mode(game_mode, behavior)
    
    def goto_menu(menu_name: str) -> None:
        """Callback para navegar entre menus."""
        game.set_current_screen(menu_name)
    
    screens = {}
    
    # Menu Principal
    screens[MenuName.MAIN_MENU.value] = create_main_menu(
        screen, assets, background, goto_menu
    )
    
    # Menu Singleplayer
    screens[MenuName.SINGLEPLAYER_MENU.value] = create_singleplayer_menu(
        screen, assets, background, game.records, start_mode, goto_menu
    )
    
    # Menu Player vs Player
    screens[MenuName.PLAYER_VS_PLAYER_MENU.value] = create_multiplayer_menu(
        screen, assets, background,
        "Player vs Player", GameMode.PLAYER_VS_PLAYER.value,
        start_mode, goto_menu
    )
    
    # Menu Player vs Bot
    screens[MenuName.PLAYER_VS_BOT_MENU.value] = create_multiplayer_menu(
        screen, assets, background,
        "Player vs Bot", GameMode.PLAYER_VS_BOT.value,
        start_mode, goto_menu
    )
    
    # Tela de Fim de Jogo
    screens[MenuName.END_SCREEN.value] = create_end_screen(
        screen, assets, background, goto_menu
    )
    
    return screens


def main() -> None:
    """Função principal do jogo."""
    screen = initialize_pygame()
    
    assets = AssetManager()
    # Usa factory function para criar Game com injeção de dependências
    game = create_game_instance(screen)
    background = BackgroundManager()
    
    screens = create_all_menus(screen, assets, background, game)
    
    game.screens = screens
    game.current_screen = screens[MenuName.MAIN_MENU.value]
    game.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()