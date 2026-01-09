"""
Object Pool para reutilização de objetos e redução de alocações de memória.
"""
from __future__ import annotations
from typing import TypeVar, Type, Callable, Optional, List

T = TypeVar('T')


class ObjectPool:
    """
    Pool de objetos para reutilização, reduzindo alocações de memória.
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        initial_size: int = 10,
        max_size: int = 100
    ) -> None:
        """
        Inicializa o object pool.
        
        Args:
            factory: Função que cria novos objetos
            initial_size: Número inicial de objetos no pool
            max_size: Tamanho máximo do pool
        """
        self._factory = factory
        self._max_size = max_size
        self._pool: List[T] = []
        
        # Pré-popula o pool
        for _ in range(initial_size):
            self._pool.append(factory())
    
    def acquire(self) -> T:
        """
        Adquire um objeto do pool (cria novo se pool vazio).
        
        Returns:
            Objeto do pool
        """
        if self._pool:
            return self._pool.pop()
        return self._factory()
    
    def release(self, obj: T) -> None:
        """
        Libera um objeto de volta ao pool.
        
        Args:
            obj: Objeto a ser liberado
        """
        if len(self._pool) < self._max_size:
            self._pool.append(obj)
    
    def clear(self) -> None:
        """Limpa o pool, removendo todos os objetos."""
        self._pool.clear()
    
    def size(self) -> int:
        """
        Retorna o tamanho atual do pool.
        
        Returns:
            Número de objetos disponíveis no pool
        """
        return len(self._pool)

