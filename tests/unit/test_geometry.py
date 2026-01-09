"""
Testes unitários para funções geométricas.
"""
import pytest
import sys
from unittest.mock import MagicMock

# Mock pygame antes de importar módulos que dependem dele
mock_pygame = MagicMock()
sys.modules['pygame'] = mock_pygame

from mygame.utils.geometry import (
    calculate_centered_position,
    calculate_bounds_for_singleplayer,
    calculate_bounds_for_multiplayer,
    calculate_distance_squared,
    is_position_in_bounds
)
from mygame.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT


class TestCalculateCenteredPosition:
    """Testes para calculate_centered_position."""
    
    def test_centered_position(self):
        """Testa cálculo de posição centralizada."""
        width, height = 100, 50
        x, y = calculate_centered_position(width, height)
        
        expected_x = (SCREEN_WIDTH - width) / 2
        expected_y = (SCREEN_HEIGHT - height) / 2
        
        assert x == int(expected_x)
        assert y == int(expected_y)
    
    def test_custom_screen_size(self):
        """Testa com tamanho de tela customizado."""
        width, height = 200, 100
        screen_w, screen_h = 800, 600
        x, y = calculate_centered_position(width, height, screen_w, screen_h)
        
        assert x == 300  # (800 - 200) / 2
        assert y == 250  # (600 - 100) / 2


class TestCalculateBoundsForSingleplayer:
    """Testes para calculate_bounds_for_singleplayer."""
    
    def test_bounds(self):
        """Testa cálculo de bounds para singleplayer."""
        bounds = calculate_bounds_for_singleplayer()
        
        assert bounds[0] == 0  # x_min
        assert bounds[1] == SCREEN_WIDTH  # x_max
        assert bounds[2] == 0  # y_min
        assert bounds[3] == SCREEN_HEIGHT  # y_max


class TestCalculateBoundsForMultiplayer:
    """Testes para calculate_bounds_for_multiplayer."""
    
    def test_bounds(self):
        """Testa cálculo de bounds para multiplayer."""
        p1_bounds, p2_bounds = calculate_bounds_for_multiplayer()
        
        screen_midpoint = SCREEN_HEIGHT // 2
        
        # Player 1 (topo)
        assert p1_bounds[0] == 0
        assert p1_bounds[1] == SCREEN_WIDTH
        assert p1_bounds[2] == 0
        assert p1_bounds[3] == screen_midpoint
        
        # Player 2 (base)
        assert p2_bounds[0] == 0
        assert p2_bounds[1] == SCREEN_WIDTH
        assert p2_bounds[2] == screen_midpoint
        assert p2_bounds[3] == SCREEN_HEIGHT


class TestCalculateDistanceSquared:
    """Testes para calculate_distance_squared."""
    
    def test_distance_squared(self):
        """Testa cálculo de distância ao quadrado."""
        pos1 = (0, 0)
        pos2 = (3, 4)
        
        # Distância ao quadrado: 3² + 4² = 9 + 16 = 25
        result = calculate_distance_squared(pos1, pos2)
        assert result == 25.0
    
    def test_same_position(self):
        """Testa com mesma posição."""
        pos = (10, 20)
        result = calculate_distance_squared(pos, pos)
        assert result == 0.0


class TestIsPositionInBounds:
    """Testes para is_position_in_bounds."""
    
    def test_position_inside(self):
        """Testa posição dentro dos bounds."""
        pos = (50, 50)
        bounds = (0, 100, 0, 100)
        assert is_position_in_bounds(pos, bounds) is True
    
    def test_position_outside(self):
        """Testa posição fora dos bounds."""
        pos = (150, 50)
        bounds = (0, 100, 0, 100)
        assert is_position_in_bounds(pos, bounds) is False
    
    def test_position_on_edge(self):
        """Testa posição na borda dos bounds."""
        pos = (100, 50)
        bounds = (0, 100, 0, 100)
        assert is_position_in_bounds(pos, bounds) is True  # Inclui bordas

