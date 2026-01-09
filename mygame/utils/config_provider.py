"""
Provedor de configuração que abstrai acesso às constantes.
Permite injeção de configuração mock para testes.
"""
from __future__ import annotations
from typing import Dict, Any
from mygame.core.interfaces import IConfigProvider
import mygame.utils.config as config_module


class ConfigProvider:
    """
    Implementação padrão de IConfigProvider que lê de config.py.
    """
    
    def __init__(self, config_dict: Dict[str, Any] | None = None) -> None:
        """
        Inicializa o provedor de configuração.
        
        Args:
            config_dict: Dicionário opcional com configurações customizadas (para testes)
        """
        self._config_dict = config_dict
        self._config_cache: Dict[str, Any] | None = None
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de configuração.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se não encontrado
            
        Returns:
            Valor da configuração ou default
        """
        if self._config_dict is not None:
            return self._config_dict.get(key, default)
        
        # Lê do módulo config
        return getattr(config_module, key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Obtém todas as configurações.
        
        Returns:
            Dicionário com todas as configurações
        """
        if self._config_dict is not None:
            return self._config_dict.copy()
        
        # Cache para evitar múltiplas leituras
        if self._config_cache is None:
            self._config_cache = {
                key: getattr(config_module, key)
                for key in dir(config_module)
                if not key.startswith('_') and not callable(getattr(config_module, key))
            }
        
        return self._config_cache.copy()


# Instância global padrão (para compatibilidade)
_default_config_provider: ConfigProvider | None = None


def get_default_config() -> ConfigProvider:
    """
    Retorna o provedor de configuração padrão (singleton).
    
    Returns:
        Instância padrão de ConfigProvider
    """
    global _default_config_provider
    if _default_config_provider is None:
        _default_config_provider = ConfigProvider()
    return _default_config_provider

