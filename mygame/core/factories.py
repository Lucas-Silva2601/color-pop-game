"""
Factory functions para criação de instâncias do jogo com injeção de dependência.
Facilita criação de objetos e permite injeção de mocks para testes.
"""
from __future__ import annotations
import pygame
from typing import Optional
from mygame.core.game import Game
from mygame.core.asset_manager import AssetManager
from mygame.core.phase_manager import PhaseManager
from mygame.fx.particle_system import ParticleSystem
from mygame.ui.hud import HUD
from mygame.ui.button import Button
from mygame.core.interfaces import IAssetManager, IParticleSystem, IConfigProvider
from mygame.utils.config_provider import ConfigProvider, get_default_config
from mygame.utils.config import GRAY, SCREEN_WIDTH, SCREEN_HEIGHT


def create_asset_manager(
    config_provider: Optional[IConfigProvider] = None
) -> AssetManager:
    """
    Cria uma instância de AssetManager.
    
    Args:
        config_provider: Provedor de configuração (opcional, usa padrão se None)
        
    Returns:
        Instância de AssetManager
    """
    return AssetManager()


def create_particle_system() -> ParticleSystem:
    """
    Cria uma instância de ParticleSystem.
    
    Returns:
        Instância de ParticleSystem
    """
    return ParticleSystem()


def create_phase_manager(
    asset_manager: Optional[IAssetManager] = None,
    particle_system: Optional[IParticleSystem] = None,
    config_provider: Optional[IConfigProvider] = None
) -> PhaseManager:
    """
    Cria uma instância de PhaseManager com dependências injetadas.
    
    Args:
        asset_manager: Gerenciador de assets (opcional, cria novo se None)
        particle_system: Sistema de partículas (opcional, cria novo se None)
        config_provider: Provedor de configuração (opcional, usa padrão se None)
        
    Returns:
        Instância de PhaseManager
    """
    if asset_manager is None:
        asset_manager = create_asset_manager(config_provider)
    if particle_system is None:
        particle_system = create_particle_system()
    
    return PhaseManager(asset_manager, particle_system)


def create_hud(asset_manager: IAssetManager) -> HUD:
    """
    Cria uma instância de HUD.
    
    Args:
        asset_manager: Gerenciador de assets
        
    Returns:
        Instância de HUD
    """
    return HUD(asset_manager)


def create_back_button(
    asset_manager: IAssetManager,
    callback: callable
) -> Button:
    """
    Cria um botão "Voltar" padronizado.
    
    Args:
        asset_manager: Gerenciador de assets
        callback: Função de callback ao clicar
        
    Returns:
        Instância de Button
    """
    return Button(
        rect=pygame.Rect(10, 10, 80, 40),
        text="Voltar",
        font=asset_manager.fonts['back_button'],
        callback=callback,
        bg_color=GRAY,
        hover_sound=asset_manager.sounds.get('ui_hover'),
        click_sound=asset_manager.sounds.get('ui_click')
    )


def create_game_instance(
    screen: pygame.Surface,
    asset_manager: Optional[IAssetManager] = None,
    particle_system: Optional[IParticleSystem] = None,
    phase_manager: Optional[PhaseManager] = None,
    config_provider: Optional[IConfigProvider] = None
) -> Game:
    """
    Cria uma instância completa de Game com todas as dependências.
    
    Args:
        screen: Superfície do pygame
        asset_manager: Gerenciador de assets (opcional, cria novo se None)
        particle_system: Sistema de partículas (opcional, cria novo se None)
        phase_manager: Gerenciador de fases (opcional, cria novo se None)
        config_provider: Provedor de configuração (opcional, usa padrão se None)
        
    Returns:
        Instância de Game configurada
    """
    if config_provider is None:
        config_provider = get_default_config()
    
    if asset_manager is None:
        asset_manager = create_asset_manager(config_provider)
    
    if particle_system is None:
        particle_system = create_particle_system()
    
    if phase_manager is None:
        phase_manager = create_phase_manager(asset_manager, particle_system, config_provider)
    
    return Game(screen, asset_manager, particle_system, phase_manager)

