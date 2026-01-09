"""
Testes unitários para funções helper.
"""
import pytest
from mygame.utils.helpers import is_multiplayer_mode, is_singleplayer_mode
from mygame.core.game_mode import GameMode


class TestIsMultiplayerMode:
    """Testes para is_multiplayer_mode."""
    
    def test_pvp_mode(self):
        """Testa com modo PvP."""
        assert is_multiplayer_mode(GameMode.PLAYER_VS_PLAYER.value) is True
    
    def test_pve_mode(self):
        """Testa com modo PvE."""
        assert is_multiplayer_mode(GameMode.PLAYER_VS_BOT.value) is True
    
    def test_singleplayer_mode(self):
        """Testa com modo singleplayer."""
        assert is_multiplayer_mode(GameMode.SINGLEPLAYER.value) is False


class TestIsSingleplayerMode:
    """Testes para is_singleplayer_mode."""
    
    def test_singleplayer_mode(self):
        """Testa com modo singleplayer."""
        assert is_singleplayer_mode(GameMode.SINGLEPLAYER.value) is True
    
    def test_pvp_mode(self):
        """Testa com modo PvP."""
        assert is_singleplayer_mode(GameMode.PLAYER_VS_PLAYER.value) is False
    
    def test_pve_mode(self):
        """Testa com modo PvE."""
        assert is_singleplayer_mode(GameMode.PLAYER_VS_BOT.value) is False

