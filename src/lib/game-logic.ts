import {
  BALL_COUNT_INCREASE_PER_PHASE,
  BALL_RADIUS,
  BASE_BALL_COUNT,
  BASE_FREE_BALL_SPEED,
  BASE_GRAVITY,
  COLORS_PASTEL,
  GRAVITY_INCREASE_PER_PHASE,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
  SPEED_INCREASE_PER_PHASE,
} from "./config";
import type {
  BallBehavior,
  BallEntity,
  Bounds,
  GameMode,
  PhaseConfig,
} from "@/types/game";

let nextId = 1;

export function phaseParameters(phase: number): PhaseConfig {
  const raw = BASE_BALL_COUNT + (phase - 1) * BALL_COUNT_INCREASE_PER_PHASE;
  const numBalls = Math.floor(raw / 2) * 2; // sempre par (igual ao Pygame)
  return {
    numBalls,
    speed: BASE_FREE_BALL_SPEED + (phase - 1) * SPEED_INCREASE_PER_PHASE,
    gravity: BASE_GRAVITY + (phase - 1) * GRAVITY_INCREASE_PER_PHASE,
  };
}

export function singleplayerBounds(): Bounds {
  return {
    xMin: 0,
    xMax: SCREEN_WIDTH,
    yMin: 70,
    yMax: SCREEN_HEIGHT - 10,
  };
}

export function multiplayerBounds(): [Bounds, Bounds] {
  const mid = SCREEN_HEIGHT / 2;
  return [
    { xMin: 0, xMax: SCREEN_WIDTH, yMin: 70, yMax: mid - 8 },
    { xMin: 0, xMax: SCREEN_WIDTH, yMin: mid + 8, yMax: SCREEN_HEIGHT - 10 },
  ];
}

function randomPos(bounds: Bounds) {
  return {
    x: bounds.xMin + BALL_RADIUS + Math.random() * (bounds.xMax - bounds.xMin - BALL_RADIUS * 2),
    y: bounds.yMin + BALL_RADIUS + Math.random() * (bounds.yMax - bounds.yMin - BALL_RADIUS * 2),
  };
}

function safePosition(bounds: Bounds, existing: BallEntity[]): { x: number; y: number } {
  if (existing.length === 0) return randomPos(bounds);
  const margin = BALL_RADIUS * 2.2;
  const marginSq = margin * margin;
  for (let i = 0; i < 100; i++) {
    const p = randomPos(bounds);
    const overlap = existing.some((b) => {
      const dx = b.x - p.x;
      const dy = b.y - p.y;
      return dx * dx + dy * dy < marginSq;
    });
    if (!overlap) return p;
  }
  return randomPos(bounds);
}

function pickTwoColors(): [string, string] {
  const shuffled = [...COLORS_PASTEL].sort(() => Math.random() - 0.5);
  return [shuffled[0], shuffled[1]];
}

function makeBall(
  color: string,
  colors: [string, string],
  bounds: Bounds,
  behavior: BallBehavior,
  speed: number,
  gravity: number,
  existing: BallEntity[],
): BallEntity {
  const pos = safePosition(bounds, existing);
  const angle = Math.random() * Math.PI * 2;
  return {
    id: nextId++,
    x: pos.x,
    y: pos.y,
    vx: behavior === "movimento" ? Math.cos(angle) * speed : 0,
    vy: behavior === "movimento" ? Math.sin(angle) * speed : 0,
    radius: BALL_RADIUS,
    color,
    colorA: colors[0],
    colorB: colors[1],
    scale: 1,
    animating: false,
    animationTimer: 0,
    bounds,
    behavior,
    gravity,
    speed,
  };
}

export interface PhaseBalls {
  player: BallEntity[];
  opponent: BallEntity[];
  colors: [string, string];
}

export function createPhaseBalls(
  mode: GameMode,
  behavior: BallBehavior,
  phase: number,
): PhaseBalls {
  const { numBalls, speed, gravity } = phaseParameters(phase);
  const colors = pickTwoColors();

  if (mode === "singleplayer") {
    const bounds = singleplayerBounds();
    const player: BallEntity[] = [];
    for (let i = 0; i < numBalls; i++) {
      player.push(
        makeBall(colors[i % 2], colors, bounds, behavior, speed, gravity, player),
      );
    }
    return { player, opponent: [], colors };
  }

  const [top, bottom] = multiplayerBounds();
  const half = numBalls / 2;
  const player: BallEntity[] = [];
  const opponent: BallEntity[] = [];
  for (let i = 0; i < half; i++) {
    player.push(makeBall(colors[i % 2], colors, top, behavior, speed, gravity, player));
    opponent.push(
      makeBall(colors[i % 2], colors, bottom, behavior, speed, gravity, opponent),
    );
  }
  return { player, opponent, colors };
}

export function updateBall(ball: BallEntity): void {
  if (ball.behavior === "movimento") {
    ball.x += ball.vx;
    ball.y += ball.vy;
    if (ball.x - ball.radius < ball.bounds.xMin || ball.x + ball.radius > ball.bounds.xMax) {
      ball.vx *= -1;
      ball.x = Math.min(Math.max(ball.x, ball.bounds.xMin + ball.radius), ball.bounds.xMax - ball.radius);
    }
    if (ball.y - ball.radius < ball.bounds.yMin || ball.y + ball.radius > ball.bounds.yMax) {
      ball.vy *= -1;
      ball.y = Math.min(Math.max(ball.y, ball.bounds.yMin + ball.radius), ball.bounds.yMax - ball.radius);
    }
  } else if (ball.behavior === "saltitando") {
    ball.vy += ball.gravity * 0.4;
    if (ball.vx === 0 && ball.vy === 0) {
      ball.vx = (Math.random() - 0.5) * ball.speed * 2;
      ball.vy = -Math.abs(ball.speed);
    }
    ball.x += ball.vx;
    ball.y += ball.vy;
    const floor = ball.bounds.yMax - ball.radius;
    if (ball.y >= floor) {
      ball.y = floor;
      ball.vy = -Math.abs(ball.vy) * 0.85;
      if (Math.abs(ball.vy) < 1) ball.vy = -(2 + Math.random() * 2);
    }
    if (ball.x - ball.radius < ball.bounds.xMin || ball.x + ball.radius > ball.bounds.xMax) {
      ball.vx *= -1;
      ball.x = Math.min(Math.max(ball.x, ball.bounds.xMin + ball.radius), ball.bounds.xMax - ball.radius);
    }
    if (ball.y - ball.radius < ball.bounds.yMin) {
      ball.y = ball.bounds.yMin + ball.radius;
      ball.vy = Math.abs(ball.vy);
    }
  }

  if (ball.animating) {
    ball.animationTimer += 1;
    if (ball.animationTimer < 5) ball.scale -= 0.08;
    else ball.scale += 0.08;
    if (ball.animationTimer >= 10) {
      ball.animating = false;
      ball.scale = 1;
    }
  }
}

export function isPhaseComplete(balls: BallEntity[]): boolean {
  if (balls.length === 0) return false;
  const first = balls[0].color;
  return balls.every((b) => b.color === first);
}

export function aiMove(opponent: BallEntity[]): BallEntity | null {
  if (opponent.length === 0) return null;
  const counts = new Map<string, number>();
  for (const b of opponent) counts.set(b.color, (counts.get(b.color) ?? 0) + 1);
  if (counts.size <= 1) return null;
  const majority = [...counts.entries()].sort((a, b) => b[1] - a[1])[0][0];
  const minority = opponent.filter((b) => b.color !== majority);
  if (minority.length === 0) return null;
  const pick = minority[Math.floor(Math.random() * minority.length)];
  pick.color = pick.color === pick.colorA ? pick.colorB : pick.colorA;
  pick.animating = true;
  pick.animationTimer = 0;
  return pick;
}
