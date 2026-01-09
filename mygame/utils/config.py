"""
Arquivo de configuração central para todas as constantes e valores ajustáveis do jogo.
Organizado por categorias para melhor manutenibilidade.
"""
import pygame

# ============================================================================
# CONFIGURAÇÕES DA TELA
# ============================================================================
SCREEN_WIDTH: int = 360
SCREEN_HEIGHT: int = 640
CAPTION: str = "Color Pop"
FPS: int = 60

# ============================================================================
# CONFIGURAÇÕES DE JOGO
# ============================================================================
# Modo Singleplayer
SINGLEPLAYER_TIME_LIMIT_SECONDS: int = 120  # 2 minutos

# Modo Multiplayer
MULTIPLAYER_PHASE_LIMIT: int = 10  # Número de fases no multiplayer

# ============================================================================
# CONFIGURAÇÕES DE PROGRESSÃO
# ============================================================================
BASE_BALL_COUNT: int = 6
BALL_COUNT_INCREASE_PER_PHASE: int = 2

# ============================================================================
# FÍSICA E MOVIMENTO
# ============================================================================
BALL_RADIUS: int = 25
BASE_FREE_BALL_SPEED: float = 2.0
SPEED_INCREASE_PER_PHASE: float = 0.5
BASE_GRAVITY: float = 0.3
GRAVITY_INCREASE_PER_PHASE: float = 0.05

# ============================================================================
# PALETA DE CORES
# ============================================================================
# Cores da UI
DARK_BLUE: tuple[int, int, int] = (15, 23, 42)
LIGHT_GRAY: tuple[int, int, int] = (203, 213, 225)
CYAN: tuple[int, int, int] = (34, 211, 238)
MAGENTA: tuple[int, int, int] = (236, 72, 153)
WHITE: tuple[int, int, int] = (240, 240, 240)
BLACK: tuple[int, int, int] = (10, 10, 10)
RED: tuple[int, int, int] = (220, 20, 60)
GRAY: tuple[int, int, int] = (100, 100, 100)

# Cores das áreas do jogo
PLAYER_AREA_COLOR: tuple[int, int, int] = (40, 40, 40)
OPPONENT_AREA_COLOR: tuple[int, int, int] = (50, 50, 50)

# Cores das bolinhas (paleta pastel)
COLORS_PASTEL: list[tuple[int, int, int]] = [
    (255, 179, 186), (255, 223, 186), (255, 255, 186),
    (186, 255, 201), (186, 225, 255)
]

# ============================================================================
# ASSETS - FONTES
# ============================================================================
MODERN_FONT_PATH: str = "assets/fonts/ModernFont.ttf"
PIXEL_FONT_PATH: str = "assets/fonts/PixelFont.ttf"

# Tamanhos de fonte
TITLE_FONT_SIZE: int = 20
SUBTITLE_FONT_SIZE: int = 22
BUTTON_FONT_SIZE: int = 17
HUD_PHASE_FONT_SIZE: int = 30
HUD_TIMER_FONT_SIZE: int = 32

# ============================================================================
# ASSETS - SONS E MÚSICA
# ============================================================================
SOUND_UI_HOVER_PATH: str = "assets/sounds/ui_hover.wav"
SOUND_UI_CLICK_PATH: str = "assets/sounds/ui_click.wav"
SOUND_POP_PATH: str = "assets/sounds/bubble_pop.wav"
MUSIC_BACKGROUND_PATH: str = "assets/sounds/background_music.mp3"

# ============================================================================
# CONFIGURAÇÕES DE DESIGN
# ============================================================================
DECORATIVE_BALL_COUNT: int = 15
DECORATIVE_BALL_MIN_SPEED: float = 0.2
DECORATIVE_BALL_MAX_SPEED: float = 0.8

# ============================================================================
# CONFIGURAÇÕES DE ANIMAÇÃO E INTERAÇÃO
# ============================================================================
BUTTON_ANIMATION_SPEED: float = 0.2
BUTTON_HOVER_SCALE: float = 1.05
BUTTON_SHADOW_OFFSET: int = 3
BUTTON_BORDER_RADIUS: int = 12
BUTTON_SHADOW_BORDER_RADIUS: int = 15

# ============================================================================
# CONFIGURAÇÕES DE FÍSICA E COLISÃO
# ============================================================================
SAFE_POSITION_MAX_ATTEMPTS: int = 100
COLLISION_MARGIN_MULTIPLIER: float = 2.2

# ============================================================================
# CONFIGURAÇÕES DE UI
# ============================================================================
HUD_TIMER_WARNING_THRESHOLD: int = 10  # Segundos para timer piscar vermelho
DIVIDER_LINE_WIDTH: int = 4

# ============================================================================
# ARQUIVOS DE DADOS
# ============================================================================
SAVE_FILE: str = "save_data.json"