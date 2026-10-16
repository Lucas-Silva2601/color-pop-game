"use client";

import { useEffect, useRef } from "react";
import {
  AI_THINK_INTERVAL_MS,
  MULTIPLAYER_PHASE_LIMIT,
  OPPONENT_AREA_COLOR,
  PLAYER_AREA_COLOR,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
  SINGLEPLAYER_TIME_LIMIT_SECONDS,
} from "@/lib/config";
import {
  aiMove,
  createPhaseBalls,
  isPhaseComplete,
  updateBall,
} from "@/lib/game-logic";
import type { BallBehavior, BallEntity, GameMode } from "@/types/game";
import { modeKey, saveRecord } from "@/hooks/useRecords";

interface Props {
  mode: GameMode;
  behavior: BallBehavior;
  onExit: (result: { phases: number; message: string }) => void;
  muted: boolean;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  color: string;
}

function playPop(muted: boolean) {
  if (muted) return;
  try {
    const audio = new Audio("/sounds/bubble_pop.wav");
    audio.volume = 0.4;
    void audio.play().catch(() => {});
  } catch {
    /* ignore */
  }
}

export default function GameCanvas({ mode, behavior, onExit, muted }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const stateRef = useRef({
    player: [] as BallEntity[],
    opponent: [] as BallEntity[],
    particles: [] as Particle[],
    phase: 1,
    p1Score: 0,
    p2Score: 0,
    startTime: Date.now(),
    timeLeft: SINGLEPLAYER_TIME_LIMIT_SECONDS,
    lastAi: 0,
    finished: false,
  });

  useEffect(() => {
    const s = stateRef.current;
    s.phase = 1;
    s.p1Score = 0;
    s.p2Score = 0;
    s.startTime = Date.now();
    s.finished = false;
    s.particles = [];
    const init = createPhaseBalls(mode, behavior, 1);
    s.player = init.player;
    s.opponent = init.opponent;
  }, [mode, behavior]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;

    const loadNextPhase = () => {
      const s = stateRef.current;
      s.phase += 1;
      const next = createPhaseBalls(mode, behavior, s.phase);
      s.player = next.player;
      s.opponent = next.opponent;
    };

    const finish = (message: string) => {
      const s = stateRef.current;
      if (s.finished) return;
      s.finished = true;
      if (mode === "singleplayer") {
        saveRecord(modeKey(mode, behavior), s.phase);
      }
      onExit({ phases: s.phase, message });
    };

    const loop = () => {
      const s = stateRef.current;
      if (!s.finished) {
        for (const b of s.player) updateBall(b);
        for (const b of s.opponent) updateBall(b);

        if (mode === "pve") {
          const now = performance.now();
          if (now - s.lastAi > AI_THINK_INTERVAL_MS) {
            s.lastAi = now;
            aiMove(s.opponent);
          }
        }

        // partículas
        s.particles = s.particles.filter((p) => p.life > 0);
        for (const p of s.particles) {
          p.x += p.vx;
          p.y += p.vy;
          p.life -= 1;
        }

        if (mode === "singleplayer") {
          const elapsed = Math.floor((Date.now() - s.startTime) / 1000);
          s.timeLeft = SINGLEPLAYER_TIME_LIMIT_SECONDS - elapsed;
          if (s.timeLeft < 0) {
            finish(`Tempo esgotado! Fases: ${s.phase}`);
          } else if (isPhaseComplete(s.player)) {
            loadNextPhase();
          }
        } else {
          const p1Done = isPhaseComplete(s.player);
          const p2Done = isPhaseComplete(s.opponent);
          if (p1Done || p2Done) {
            const winner = p1Done ? "Jogador 1" : mode === "pvp" ? "Jogador 2" : "Bot";
            if (winner === "Jogador 1") s.p1Score += 1;
            else s.p2Score += 1;
            if (s.phase >= MULTIPLAYER_PHASE_LIMIT) {
              const final =
                s.p1Score > s.p2Score
                  ? "Jogador 1 venceu!"
                  : s.p2Score > s.p1Score
                    ? `${winner} venceu!`
                    : "Empate!";
              finish(`${final} (${s.p1Score} x ${s.p2Score})`);
            } else {
              loadNextPhase();
            }
          }
        }
      }

      // ---- draw ----
      const s2 = stateRef.current;
      ctx.fillStyle = PLAYER_AREA_COLOR;
      ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
      const isMulti = mode !== "singleplayer";
      if (isMulti) {
        ctx.fillStyle = OPPONENT_AREA_COLOR;
        ctx.fillRect(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2);
        ctx.strokeStyle = "#646464";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(0, SCREEN_HEIGHT / 2);
        ctx.lineTo(SCREEN_WIDTH, SCREEN_HEIGHT / 2);
        ctx.stroke();
        ctx.fillStyle = "#e2e8f0";
        ctx.font = "12px system-ui";
        ctx.fillText(`P1 ${s2.p1Score}  ·  Fase ${s2.phase}/${MULTIPLAYER_PHASE_LIMIT}`, 12, 24);
        ctx.fillText(
          `${mode === "pvp" ? "P2" : "Bot"} ${s2.p2Score}`,
          12,
          SCREEN_HEIGHT / 2 + 22,
        );
      } else {
        ctx.fillStyle = s2.timeLeft <= 10 ? "#f87171" : "#e2e8f0";
        ctx.font = "bold 20px system-ui";
        ctx.fillText(`Fase ${s2.phase}  ·  ${Math.max(0, s2.timeLeft)}s`, 12, 30);
      }

      for (const b of [...s2.player, ...s2.opponent]) {
        const r = Math.max(1, b.radius * b.scale);
        ctx.beginPath();
        ctx.arc(b.x, b.y, r, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.5)";
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      for (const p of s2.particles) {
        ctx.globalAlpha = Math.max(0, p.life / 20);
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 3, 3);
        ctx.globalAlpha = 1;
      }

      raf = requestAnimationFrame(loop);
    };

    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [mode, behavior, onExit]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * SCREEN_WIDTH;
    const y = ((e.clientY - rect.top) / rect.height) * SCREEN_HEIGHT;
    const s = stateRef.current;

    let target = s.player;
    if (mode === "pvp" && y > SCREEN_HEIGHT / 2) target = s.opponent;
    if (mode === "pve" && y > SCREEN_HEIGHT / 2) return;

    for (const b of target) {
      const dx = b.x - x;
      const dy = b.y - y;
      if (dx * dx + dy * dy <= b.radius * b.radius) {
        const old = b.color;
        b.color = b.color === b.colorA ? b.colorB : b.colorA;
        b.animating = true;
        b.animationTimer = 0;
        playPop(muted);
        for (let i = 0; i < 10; i++) {
          s.particles.push({
            x: b.x,
            y: b.y,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            life: 20,
            color: old,
          });
        }
        break;
      }
    }
  };

  return (
    <canvas
      ref={canvasRef}
      width={SCREEN_WIDTH}
      height={SCREEN_HEIGHT}
      onClick={handleClick}
      className="game-canvas h-[70vh] max-h-[640px] w-auto cursor-pointer rounded-2xl shadow-2xl ring-1 ring-white/10"
    />
  );
}
