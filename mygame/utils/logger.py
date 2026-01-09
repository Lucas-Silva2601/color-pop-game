"""
Sistema de logging estruturado para o jogo.
Fornece logs categorizados por nível com contexto e timestamps.
"""
from __future__ import annotations
import logging
import sys
from typing import Any
from datetime import datetime


# Configuração do logger principal
_logger: logging.Logger | None = None
_context: dict[str, Any] = {}


def _get_logger() -> logging.Logger:
    """Retorna o logger configurado, criando se necessário."""
    global _logger
    if _logger is None:
        _logger = logging.getLogger("color_pop_game")
        _logger.setLevel(logging.DEBUG)
        
        # Evitar handlers duplicados
        if not _logger.handlers:
            # Handler para console
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Formatação com timestamp e contexto
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            _logger.addHandler(console_handler)
    
    return _logger


def set_context(**kwargs: Any) -> None:
    """
    Define contexto global para logs.
    
    Args:
        **kwargs: Pares chave-valor para contexto (ex: game_mode, phase, score)
    """
    global _context
    _context.update(kwargs)


def clear_context() -> None:
    """Limpa o contexto global."""
    global _context
    _context.clear()


def _format_message(message: str, **context: Any) -> str:
    """
    Formata mensagem com contexto.
    
    Args:
        message: Mensagem base
        **context: Contexto adicional
        
    Returns:
        Mensagem formatada com contexto
    """
    # Merge contexto global com contexto local
    full_context = {**_context, **context}
    
    if not full_context:
        return message
    
    # Formata contexto como string
    context_str = ", ".join(f"{k}={v}" for k, v in sorted(full_context.items()))
    return f"{message} | {context_str}"


def log_debug(message: str, **context: Any) -> None:
    """
    Log de nível DEBUG (informações detalhadas para debugging).
    
    Args:
        message: Mensagem do log
        **context: Contexto adicional (ex: phase=3, game_mode="singleplayer")
    """
    logger = _get_logger()
    logger.debug(_format_message(message, **context))


def log_info(message: str, **context: Any) -> None:
    """
    Log de nível INFO (informações gerais sobre o funcionamento).
    
    Args:
        message: Mensagem do log
        **context: Contexto adicional
    """
    logger = _get_logger()
    logger.info(_format_message(message, **context))


def log_warning(message: str, **context: Any) -> None:
    """
    Log de nível WARNING (avisos sobre situações não críticas).
    
    Args:
        message: Mensagem do log
        **context: Contexto adicional
    """
    logger = _get_logger()
    logger.warning(_format_message(message, **context))


def log_error(
    message: str,
    exception: Exception | None = None,
    **context: Any
) -> None:
    """
    Log de nível ERROR (erros que não impedem o funcionamento).
    
    Args:
        message: Mensagem do log
        exception: Exceção relacionada (opcional)
        **context: Contexto adicional
    """
    logger = _get_logger()
    
    if exception:
        # Adiciona informações da exceção ao contexto
        context['exception_type'] = type(exception).__name__
        context['exception_message'] = str(exception)
        logger.error(_format_message(message, **context), exc_info=exception)
    else:
        logger.error(_format_message(message, **context))


def log_critical(
    message: str,
    exception: Exception | None = None,
    **context: Any
) -> None:
    """
    Log de nível CRITICAL (erros críticos que podem impedir o funcionamento).
    
    Args:
        message: Mensagem do log
        exception: Exceção relacionada (opcional)
        **context: Contexto adicional
    """
    logger = _get_logger()
    
    if exception:
        context['exception_type'] = type(exception).__name__
        context['exception_message'] = str(exception)
        logger.critical(_format_message(message, **context), exc_info=exception)
    else:
        logger.critical(_format_message(message, **context))


def set_log_level(level: str) -> None:
    """
    Define o nível mínimo de log.
    
    Args:
        level: Nível ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    logger = _get_logger()
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    logger.setLevel(level_map.get(level.upper(), logging.INFO))
    for handler in logger.handlers:
        handler.setLevel(level_map.get(level.upper(), logging.INFO))

