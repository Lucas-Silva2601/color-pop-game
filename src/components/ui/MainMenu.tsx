"use client";

import { BALL_BEHAVIORS } from "@/lib/config";
import type { BallBehavior, GameMode, ScreenState } from "@/types/game";
import { loadRecords, type Records } from "@/hooks/useRecords";
import { useEffect, useState } from "react";

interface Props {
  screen: ScreenState;
  onNavigate: (s: ScreenState) => void;
  onStart: (mode: GameMode, behavior: BallBehavior) => void;
}

function menuFor(screen: ScreenState): { title: string; mode: GameMode } | null {
  if (screen === "singleplayer-menu") return { title: "Singleplayer", mode: "singleplayer" };
  if (screen === "pvp-menu") return { title: "Player vs Player", mode: "pvp" };
  if (screen === "pve-menu") return { title: "Player vs Bot", mode: "pve" };
  return null;
}

export default function MainMenu({ screen, onNavigate, onStart }: Props) {
  // Estado inicial vazio = igual ao HTML do servidor. Recordes são
  // carregados após a hidratação para não divergir do SSR.
  const [records, setRecords] = useState<Records>({});
  useEffect(() => {
    setRecords(loadRecords());
  }, []);

  if (screen === "main-menu") {
    return (
      <div className="flex w-full max-w-sm flex-col gap-3">
        <h1 className="mb-2 text-center text-5xl font-black tracking-tight">
          Color <span className="text-cyan-400">Pop</span>
        </h1>
        <p className="mb-4 text-center text-sm text-slate-400">
          Deixe todas as bolinhas da mesma cor clicando nelas.
        </p>
        {(
          [
            { label: "Singleplayer", target: "singleplayer-menu", color: "bg-cyan-500 hover:bg-cyan-400" },
            { label: "Player vs Player", target: "pvp-menu", color: "bg-pink-500 hover:bg-pink-400" },
            { label: "Player vs Bot", target: "pve-menu", color: "bg-pink-500 hover:bg-pink-400" },
          ] as const
        ).map((b) => (
          <button
            key={b.target}
            onClick={() => onNavigate(b.target)}
            className={`${b.color} rounded-xl px-6 py-4 font-bold text-slate-950 shadow-lg transition active:scale-95`}
          >
            {b.label}
          </button>
        ))}
        <p className="mt-4 text-center text-xs text-slate-500">
          Pygame original → port React + Next.js + Canvas
        </p>
      </div>
    );
  }

  const info = menuFor(screen);
  if (!info) return null;

  return (
    <div className="flex w-full max-w-sm flex-col gap-3">
      <h2 className="mb-2 text-center text-3xl font-extrabold">{info.title}</h2>
      {BALL_BEHAVIORS.map((b) => {
        const key = `${info.mode}_${b.value}`;
        const record = records[key] ?? 0;
        return (
          <div key={b.value}>
            <button
              onClick={() => onStart(info.mode, b.value as BallBehavior)}
              className="w-full rounded-xl bg-cyan-500 px-6 py-4 font-bold text-slate-950 shadow-lg transition hover:bg-cyan-400 active:scale-95"
            >
              {b.label}
            </button>
            <p className="mt-1 text-center text-xs text-slate-400">
              {b.hint}
              {info.mode === "singleplayer" && ` · Recorde: ${record} fases`}
            </p>
          </div>
        );
      })}
      <button
        onClick={() => onNavigate("main-menu")}
        className="mt-2 rounded-xl bg-slate-700 px-6 py-3 font-semibold text-white transition hover:bg-slate-600 active:scale-95"
      >
        Voltar
      </button>
    </div>
  );
}
