"""
Gerenciador de assets (fontes, sons, música) do jogo.
"""
from __future__ import annotations
import pygame
from typing import Dict
from mygame.utils.config import (
    MODERN_FONT_PATH, PIXEL_FONT_PATH,
    TITLE_FONT_SIZE, BUTTON_FONT_SIZE,
    HUD_PHASE_FONT_SIZE, HUD_TIMER_FONT_SIZE,
    SOUND_POP_PATH, SOUND_UI_HOVER_PATH, SOUND_UI_CLICK_PATH,
    MUSIC_BACKGROUND_PATH
)
from mygame.utils.exceptions import AssetError, AssetNotFoundError
from mygame.utils.validators import validate_file_exists
from mygame.utils.logger import log_info, log_warning, log_error


class AssetManager:
    """
    Classe para carregar e gerenciar todos os assets do jogo,
    como fontes e sons, para evitar carregamentos repetidos.
    """
    
    def __init__(self) -> None:
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        log_info("Initializing AssetManager")
        self.load_assets()

    def load_assets(self) -> None:
        """Carrega todas as fontes e sons definidos no config."""
        log_info("Loading game assets")
        self._load_fonts()
        self._load_sounds()
        log_info("Assets loaded successfully", fonts_count=len(self.fonts), sounds_count=len(self.sounds))

    def _load_fonts(self) -> None:
        """Carrega todas as fontes do jogo."""
        font_configs = [
            ('title', MODERN_FONT_PATH, TITLE_FONT_SIZE),
            ('button', MODERN_FONT_PATH, BUTTON_FONT_SIZE),
            ('hud_phase', PIXEL_FONT_PATH, HUD_PHASE_FONT_SIZE),
            ('hud_timer', PIXEL_FONT_PATH, HUD_TIMER_FONT_SIZE),
            ('back_button', PIXEL_FONT_PATH, 10),
        ]
        
        for font_key, font_path, font_size in font_configs:
            try:
                # Valida que o arquivo existe antes de tentar carregar
                validate_file_exists(font_path, "fonte")
                self.fonts[font_key] = pygame.font.Font(font_path, font_size)
                log_info("Font loaded", font_type=font_key, path=font_path, size=font_size)
            except AssetNotFoundError as e:
                # Fallback para fonte padrão se não conseguir carregar
                fallback_size = font_size if font_key != 'back_button' else 24
                self.fonts[font_key] = pygame.font.Font(None, fallback_size)
                log_warning(
                    "Font file not found, using default font",
                    font_type=font_key,
                    path=font_path,
                    error=str(e),
                    fallback_size=fallback_size
                )
            except pygame.error as e:
                # Erro do pygame ao carregar fonte
                fallback_size = font_size if font_key != 'back_button' else 24
                self.fonts[font_key] = pygame.font.Font(None, fallback_size)
                log_error(
                    "Error loading font, using default",
                    exception=e,
                    font_type=font_key,
                    path=font_path,
                    fallback_size=fallback_size
                )
            except Exception as e:
                # Erro inesperado
                log_error(
                    "Unexpected error loading font",
                    exception=e,
                    font_type=font_key,
                    path=font_path
                )
                # Tenta fallback mesmo em caso de erro inesperado
                fallback_size = font_size if font_key != 'back_button' else 24
                self.fonts[font_key] = pygame.font.Font(None, fallback_size)

    def _load_sounds(self) -> None:
        """Carrega todos os sons e música do jogo."""
        sound_configs = [
            ('pop', SOUND_POP_PATH),
            ('ui_hover', SOUND_UI_HOVER_PATH),
            ('ui_click', SOUND_UI_CLICK_PATH),
            ('phase_win', SOUND_POP_PATH),  # Reutiliza o som de pop
        ]
        
        for sound_key, sound_path in sound_configs:
            try:
                validate_file_exists(sound_path, "som")
                self.sounds[sound_key] = pygame.mixer.Sound(sound_path)
                log_info("Sound loaded", sound_type=sound_key, path=sound_path)
            except AssetNotFoundError as e:
                log_warning(
                    "Sound file not found",
                    sound_type=sound_key,
                    path=sound_path,
                    error=str(e)
                )
                # Não adiciona ao dicionário se falhar
            except pygame.error as e:
                log_error(
                    "Error loading sound",
                    exception=e,
                    sound_type=sound_key,
                    path=sound_path
                )
                # Não adiciona ao dicionário se falhar
            except Exception as e:
                log_error(
                    "Unexpected error loading sound",
                    exception=e,
                    sound_type=sound_key,
                    path=sound_path
                )
        
        # Carrega música de fundo
        try:
            validate_file_exists(MUSIC_BACKGROUND_PATH, "música")
            pygame.mixer.music.load(MUSIC_BACKGROUND_PATH)
            pygame.mixer.music.set_volume(0.3)
            log_info("Background music loaded", path=MUSIC_BACKGROUND_PATH, volume=0.3)
        except AssetNotFoundError as e:
            log_warning(
                "Background music file not found",
                path=MUSIC_BACKGROUND_PATH,
                error=str(e)
            )
        except pygame.error as e:
            log_error(
                "Error loading background music",
                exception=e,
                path=MUSIC_BACKGROUND_PATH
            )
        except Exception as e:
            log_error(
                "Unexpected error loading background music",
                exception=e,
                path=MUSIC_BACKGROUND_PATH
            )

    def play_music(self) -> None:
        """Inicia a reprodução da música de fundo em loop."""
        try:
            pygame.mixer.music.play(-1)
            log_info("Background music started")
        except pygame.error as e:
            log_error(
                "Error playing background music",
                exception=e
            )
