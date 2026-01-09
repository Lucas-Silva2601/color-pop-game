"""
Interfaces (Protocols) para principais componentes do jogo.
Permite injeção de dependência e facilita testes com mocks.
"""
from __future__ import annotations
from typing import Protocol, Dict, Optional
import pygame


class IAssetManager(Protocol):
    """Interface para gerenciador de assets."""
    
    fonts: Dict[str, pygame.font.Font]
    sounds: Dict[str, pygame.mixer.Sound]
    
    def play_music(self) -> None:
        """Inicia a reprodução da música de fundo."""
        ...


class IParticleSystem(Protocol):
    """Interface para sistema de partículas."""
    
    def emit(self, x: float, y: float, color: tuple[int, int, int], count: int = 10) -> None:
        """
        Emite partículas em uma posição.
        
        Args:
            x: Posição X
            y: Posição Y
            color: Cor das partículas
            count: Número de partículas
        """
        ...
    
    def update(self) -> None:
        """Atualiza o sistema de partículas."""
        ...
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha as partículas na tela.
        
        Args:
            screen: Superfície do pygame
        """
        ...


class IConfigProvider(Protocol):
    """Interface para provedor de configuração."""
    
    def get(self, key: str, default: any = None) -> any:
        """
        Obtém um valor de configuração.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se não encontrado
            
        Returns:
            Valor da configuração ou default
        """
        ...
    
    def get_all(self) -> Dict[str, any]:
        """
        Obtém todas as configurações.
        
        Returns:
            Dicionário com todas as configurações
        """
        ...

