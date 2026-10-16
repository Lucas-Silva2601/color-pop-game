"use client";

import { useState } from "react";
import GameCanvas from "@/components/game/GameCanvas";
import MainMenu from "@/components/ui/MainMenu";
import type { BallBehavior, GameMode, ScreenState } from "@/types/game";

export default function GameShell() {
  const [screen, setScreen] = useState<ScreenState>("main-menu");
  const [mode, setMode] = useState<GameMode>("singleplayer");
  const [behavior, setBehavior] = useState<BallBehavior>("parado");
  const [muted, setMuted] = useState(false);
  const [endMessage, setEndMessage] = useState("");

  const start = (m: GameMode, b: BallBehavior) => {
    setMode(m);
    setBehavior(b);
    setScreen("playing");
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col items-center justify-center gap-6 px-4 py-10">
      {(screen === "main-menu" ||
        screen === "singleplayer-menu" ||
        screen === "pvp-menu" ||
        screen === "pve-menu") && (
        <MainMenu screen={screen} onNavigate={setScreen} onStart={start} />
      )}

      {screen === "playing" && (
        <div className="flex flex-col items-center gap-4">
          <div className="flex w-full max-w-[360px] items-center justify-between">
            <button
              onClick={() => setScreen("main-menu")}
              className="rounded-lg bg-slate-800 px-4 py-2 text-sm font-semibold ring-1 ring-white/10 hover:bg-slate-700"
            >
              ← Voltar (ESC)
            </button>
            <button
              onClick={() => setMuted((v) => !v)}
              className="rounded-lg bg-slate-800 px-4 py-2 text-sm font-semibold ring-1 ring-white/10 hover:bg-slate-700"
            >
              {muted ? "🔇 Mudo" : "🔊 Som"}
            </button>
          </div>
          <p className="text-sm text-slate-400">
            {mode} · {behavior} — clique nas bolinhas para igualar as cores
          </p>
          <GameCanvas
            mode={mode}
            behavior={behavior}
            muted={muted}
            onExit={(r) => {
              setEndMessage(r.message);
              setScreen(r.message.includes("venceu") || r.message.includes("Empate") ? "victory" : "end");
            }}
          />
        </div>
      )}

      {(screen === "end" || screen === "victory") && (
        <div className="flex w-full max-w-sm flex-col items-center gap-4 text-center">
          <h2 className="text-3xl font-black">{endMessage}</h2>
          <button
            onClick={() => setScreen("main-menu")}
            className="w-full rounded-xl bg-slate-200 px-6 py-4 font-bold text-slate-950 hover:bg-white"
          >
            Voltar ao Menu
          </button>
        </div>
      )}
    </main>
  );
}
