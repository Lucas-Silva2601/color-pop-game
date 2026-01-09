"""
Testes unitários para validadores.
"""
import pytest
from mygame.utils.validators import (
    validate_color, validate_bounds, validate_game_mode, validate_ball_behavior
)
from mygame.utils.exceptions import InvalidGameModeError
from mygame.core.game_mode import GameMode, BallBehavior


class TestValidateColor:
    """Testes para validate_color."""
    
    def test_valid_color(self):
        """Testa validação de cor válida."""
        color = (255, 128, 64)
        result = validate_color(color)
        assert result == color
    
    def test_invalid_type(self):
        """Testa validação com tipo inválido."""
        with pytest.raises(ValueError, match="Cor deve ser uma tupla"):
            validate_color([255, 128, 64])
    
    def test_invalid_length(self):
        """Testa validação com tupla de tamanho incorreto."""
        with pytest.raises(ValueError, match="Cor deve ser uma tupla de 3 inteiros"):
            validate_color((255, 128))
    
    def test_invalid_range(self):
        """Testa validação com valores fora do range."""
        with pytest.raises(ValueError, match="Valores RGB devem estar entre 0 e 255"):
            validate_color((255, 128, 300))
    
    def test_negative_value(self):
        """Testa validação com valor negativo."""
        with pytest.raises(ValueError):
            validate_color((255, -10, 64))


class TestValidateBounds:
    """Testes para validate_bounds."""
    
    def test_valid_bounds(self):
        """Testa validação de bounds válidos."""
        bounds = (0, 100, 0, 200)
        result = validate_bounds(bounds)
        assert result == bounds
    
    def test_invalid_type(self):
        """Testa validação com tipo inválido."""
        with pytest.raises(ValueError, match="Bounds deve ser uma tupla"):
            validate_bounds([0, 100, 0, 200])
    
    def test_invalid_length(self):
        """Testa validação com tupla de tamanho incorreto."""
        with pytest.raises(ValueError, match="Bounds deve ser uma tupla de 4 inteiros"):
            validate_bounds((0, 100, 0))
    
    def test_invalid_range(self):
        """Testa validação com x_min >= x_max."""
        with pytest.raises(ValueError, match="Bounds inválidos"):
            validate_bounds((100, 50, 0, 200))
    
    def test_invalid_range_y(self):
        """Testa validação com y_min >= y_max."""
        with pytest.raises(ValueError, match="Bounds inválidos"):
            validate_bounds((0, 100, 200, 50))


class TestValidateGameMode:
    """Testes para validate_game_mode."""
    
    def test_valid_singleplayer(self):
        """Testa validação de modo singleplayer."""
        result = validate_game_mode(GameMode.SINGLEPLAYER.value)
        assert result == GameMode.SINGLEPLAYER.value
    
    def test_valid_pvp(self):
        """Testa validação de modo PvP."""
        result = validate_game_mode(GameMode.PLAYER_VS_PLAYER.value)
        assert result == GameMode.PLAYER_VS_PLAYER.value
    
    def test_invalid_mode(self):
        """Testa validação com modo inválido."""
        with pytest.raises(InvalidGameModeError):
            validate_game_mode("invalid_mode")


class TestValidateBallBehavior:
    """Testes para validate_ball_behavior."""
    
    def test_valid_stationary(self):
        """Testa validação de comportamento stationary."""
        result = validate_ball_behavior(BallBehavior.STATIONARY.value)
        assert result == BallBehavior.STATIONARY.value
    
    def test_valid_free_movement(self):
        """Testa validação de comportamento free movement."""
        result = validate_ball_behavior(BallBehavior.FREE_MOVEMENT.value)
        assert result == BallBehavior.FREE_MOVEMENT.value
    
    def test_invalid_behavior(self):
        """Testa validação com comportamento inválido."""
        from mygame.utils.exceptions import InvalidBallBehaviorError
        with pytest.raises(InvalidBallBehaviorError):
            validate_ball_behavior("invalid_behavior")

