"""
Exceções customizadas para o jogo, permitindo tratamento específico de erros.
"""
from __future__ import annotations


class GameError(Exception):
    """Exceção base para todos os erros do jogo."""
    pass


class AssetError(GameError):
    """Erro relacionado ao carregamento de assets."""
    def __init__(self, message: str, asset_path: str | None = None):
        super().__init__(message)
        self.asset_path = asset_path


class ConfigurationError(GameError):
    """Erro relacionado à configuração do jogo."""
    def __init__(self, message: str, config_key: str | None = None):
        super().__init__(message)
        self.config_key = config_key


class GameStateError(GameError):
    """Erro relacionado ao estado do jogo."""
    def __init__(self, message: str, current_state: str | None = None):
        super().__init__(message)
        self.current_state = current_state


class SaveDataError(GameError):
    """Erro relacionado ao salvamento/carregamento de dados."""
    def __init__(self, message: str, file_path: str | None = None):
        super().__init__(message)
        self.file_path = file_path


class InvalidGameModeError(GameError):
    """Erro quando um modo de jogo inválido é usado."""
    def __init__(self, mode: str):
        super().__init__(f"Modo de jogo inválido: {mode}")
        self.mode = mode


class InvalidBallBehaviorError(GameError):
    """Erro quando um comportamento de bola inválido é usado."""
    def __init__(self, behavior: str):
        super().__init__(f"Comportamento de bola inválido: {behavior}")
        self.behavior = behavior


class InvalidConfigurationError(ConfigurationError):
    """Erro quando uma configuração inválida é detectada."""
    pass


class AssetNotFoundError(AssetError):
    """Erro quando um asset não é encontrado."""
    def __init__(self, asset_path: str):
        super().__init__(f"Asset não encontrado: {asset_path}", asset_path)

