// Port de mygame/utils/config.py para a web.
// Mantém os mesmos valores de gameplay do Pygame original (360x640 @ 60fps).

export const SCREEN_WIDTH = 360;
export const SCREEN_HEIGHT = 640;
export const FPS = 60;

export const SINGLEPLAYER_TIME_LIMIT_SECONDS = 120;
export const MULTIPLAYER_PHASE_LIMIT = 10;

export const BASE_BALL_COUNT = 6;
export const BALL_COUNT_INCREASE_PER_PHASE = 2;

export const BALL_RADIUS = 25;
export const BASE_FREE_BALL_SPEED = 2.0;
export const SPEED_INCREASE_PER_PHASE = 0.5;
export const BASE_GRAVITY = 0.3;
export const GRAVITY_INCREASE_PER_PHASE = 0.05;

export const COLORS_PASTEL = [
  "#ffb3ba",
  "#ffdfba",
  "#ffffba",
  "#baffc9",
  "#bae1ff",
] as const;

export const PLAYER_AREA_COLOR = "#282828";
export const OPPONENT_AREA_COLOR = "#323232";

export const AI_THINK_INTERVAL_MS = 1200;
export const TIMER_WARNING_THRESHOLD = 10;

export const STORAGE_KEY = "color-pop:records:v1";

export const GAME_MODES = [
  { value: "singleplayer", label: "Singleplayer" },
  { value: "pvp", label: "Player vs Player" },
  { value: "pve", label: "Player vs Bot" },
] as const;

export const BALL_BEHAVIORS = [
  { value: "parado", label: "Parado", hint: "Bolas estáticas — estratégia pura" },
  { value: "movimento", label: "Movimento", hint: "Bolas em movimento livre" },
  {
    value: "saltitando",
    label: "Saltitando",
    hint: "Física com gravidade — mais desafiador",
  },
] as const;
