export type GameMode = "singleplayer" | "pvp" | "pve";

export type BallBehavior = "parado" | "movimento" | "saltitando";

export type ScreenState =
  | "main-menu"
  | "singleplayer-menu"
  | "pvp-menu"
  | "pve-menu"
  | "playing"
  | "end"
  | "victory";

export interface Rgb {
  r: number;
  g: number;
  b: number;
}

export interface BallEntity {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
  colorA: string;
  colorB: string;
  scale: number;
  animating: boolean;
  animationTimer: number;
  bounds: Bounds;
  behavior: BallBehavior;
  gravity: number;
  speed: number;
}

export type Bounds = {
  xMin: number;
  xMax: number;
  yMin: number;
  yMax: number;
};

export interface PhaseConfig {
  numBalls: number;
  speed: number;
  gravity: number;
}
