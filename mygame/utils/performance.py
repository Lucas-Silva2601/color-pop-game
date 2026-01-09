"""
Utilitários para profiling e métricas de performance.
"""
from __future__ import annotations
import time
from typing import Dict, List, Optional
from mygame.utils.logger import log_debug


class PerformanceMonitor:
    """
    Monitor de performance para rastrear FPS e tempos de execução.
    """
    
    def __init__(self, track_fps: bool = True) -> None:
        """
        Inicializa o monitor de performance.
        
        Args:
            track_fps: Se True, rastreia FPS
        """
        self.track_fps = track_fps
        self.frame_times: List[float] = []
        self.max_frame_history = 60  # Mantém histórico de 60 frames
        self.last_frame_time = time.time()
        self.fps = 0.0
        
        # Métricas de tempo
        self._timings: Dict[str, List[float]] = {}
    
    def update(self) -> None:
        """Atualiza métricas de performance (chamar a cada frame)."""
        if not self.track_fps:
            return
        
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Adiciona ao histórico
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frame_history:
            self.frame_times.pop(0)
        
        # Calcula FPS médio
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def get_fps(self) -> float:
        """
        Retorna o FPS atual.
        
        Returns:
            FPS médio dos últimos frames
        """
        return self.fps
    
    def start_timing(self, name: str) -> None:
        """
        Inicia medição de tempo para uma operação.
        
        Args:
            name: Nome da operação
        """
        if name not in self._timings:
            self._timings[name] = []
        self._timings[name].append(time.time())
    
    def end_timing(self, name: str) -> float:
        """
        Finaliza medição de tempo e retorna duração.
        
        Args:
            name: Nome da operação
            
        Returns:
            Duração em segundos
        """
        if name not in self._timings or not self._timings[name]:
            return 0.0
        
        start_time = self._timings[name].pop()
        duration = time.time() - start_time
        
        # Mantém apenas últimas 100 medições
        if len(self._timings[name]) > 100:
            self._timings[name] = self._timings[name][-100:]
        
        return duration
    
    def get_avg_timing(self, name: str) -> Optional[float]:
        """
        Retorna tempo médio de uma operação.
        
        Args:
            name: Nome da operação
            
        Returns:
            Tempo médio em segundos ou None se não houver medições
        """
        if name not in self._timings or not self._timings[name]:
            return None
        
        # Calcula média dos últimos 10 timings
        recent_timings = self._timings[name][-10:]
        return sum(recent_timings) / len(recent_timings) if recent_timings else None
    
    def log_performance(self, min_fps: float = 30.0) -> None:
        """
        Loga métricas de performance se FPS estiver abaixo do mínimo.
        
        Args:
            min_fps: FPS mínimo esperado
        """
        if self.fps < min_fps:
            log_debug(
                "Low FPS detected",
                fps=self.fps,
                min_fps=min_fps,
                frame_times_count=len(self.frame_times)
            )
    
    def reset(self) -> None:
        """Reseta todas as métricas."""
        self.frame_times.clear()
        self._timings.clear()
        self.fps = 0.0
        self.last_frame_time = time.time()

