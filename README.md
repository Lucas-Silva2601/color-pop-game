# 🎮 Color Pop Game — React + Next.js + Tailwind CSS

![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![React](https://img.shields.io/badge/React-19-61DAFB.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-4-38BDF8.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Descrição

**Color Pop** é um puzzle viciante onde o objetivo é deixar todas as bolinhas da mesma cor clicando nelas para alternar entre 2 cores.

Esta é a **migração web do projeto original em Python + Pygame** (`main.py` + `mygame/`) para uma stack web moderna. O gameplay foi portado 1:1:

- **🎯 Singleplayer:** 120s, máximo de fases possível, recorde em `localStorage`
- **👥 PvP local:** tela dividida (topo vs fundo), melhor de 10 fases
- **🤖 PvE (vs Bot):** IA que a cada 1.2s converte bolas da cor minoritária
- **⚪🔵🟡 Comportamentos:** `parado` | `movimento` (quique livre) | `saltitando` (gravidade)
- **📈 Progressão:** `6 + 2/fase` bolas, velocidade `2.0 + 0.5/fase`, gravidade `0.3 + 0.05/fase`
- **✨ Efeitos:** partículas no clique, animação de escala, sons `bubble_pop.wav`

> Legado Python preservado nesta branch em `main.py`, `mygame/`, `assets/`, `tests/` para referência.

---

## 🛠️ Stack

- **Next.js 15 (App Router)** + **React 19** + **TypeScript strict**
- **Tailwind CSS v4** (`@import "tailwindcss"`)
- **Canvas 2D** para o jogo a 60fps (`requestAnimationFrame`)
- Sem dependência de game engine — lógica pura em `src/lib/game-logic.ts`

## 📁 Estrutura profissional

```
color-pop-game/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout + metadata
│   │   ├── page.tsx        # Home → GameShell
│   │   └── globals.css     # Tailwind v4
│   ├── components/
│   │   ├── game/
│   │   │   ├── GameShell.tsx   # Máquina de telas (menus → playing → end/victory)
│   │   │   └── GameCanvas.tsx  # Loop, física, IA, partículas, input
│   │   └── ui/
│   │       └── MainMenu.tsx    # Menus principal / single / pvp / pve
│   ├── lib/
│   │   ├── config.ts       # Port de mygame/utils/config.py
│   │   └── game-logic.ts   # Port de PhaseManager + Ball + BallFactory
│   ├── hooks/
│   │   └── useRecords.ts   # Recordes em localStorage (era save_data.json)
│   └── types/
│       └── game.ts         # GameMode, BallBehavior, BallEntity, Bounds
├── public/
│   └── sounds/             # bubble_pop.wav, ui_click.wav, ui_hover.wav, bg music
├── legacy (referência):
│   ├── main.py, mygame/, tests/, assets/, docs/
├── package.json
├── tsconfig.json (paths @/*)
├── next.config.mjs
└── postcss.config.mjs
```

Mapeamento Pygame → Web:

| Pygame | Web |
|---|---|
| `mygame/utils/config.py` | `src/lib/config.ts` |
| `mygame/core/phase_manager.py` + `entities/ball_*.py` | `src/lib/game-logic.ts` |
| `mygame/core/game.py` (loop/estados) | `GameCanvas.tsx` + `GameShell.tsx` |
| `mygame/ui/menu_factory.py` | `MainMenu.tsx` |
| `save_data.json` | `localStorage color-pop:records:v1` |
| `ParticleSystem` | partículas inline no Canvas |
| `pygame.mixer` | `HTMLAudio(/sounds/...)` |

---

## 🚀 Como rodar

```bash
npm install
npm run dev
# abra http://localhost:3000
```

Build produção:

```bash
npm run build
npm start
```

Legado Pygame (opcional):

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 🎯 Como jogar

1. Escolha modo → comportamento (`Parado` / `Movimento` / `Saltitando`)
2. Clique nas bolinhas para alternar a cor
3. Vença quando **todas na sua área** tiverem a mesma cor
4. PvP/PvE: tela dividida em 2 áreas; no PvE sua área é só a de cima (cliques embaixo ignorados, como no original)

## 🧪 Testes / Qualidade

```bash
npm run lint
npx tsc --noEmit
```

## 🔮 Roadmap

- [ ] Música de fundo com toggle real + WebAudio sprites
- [ ] Leaderboard global (ex: Vercel KV)
- [ ] Temas de cores + modo daltônico
- [ ] PWA / offline + mobile touch tuning
- [ ] Testes Vitest para `game-logic.ts` (port de `tests/unit/`)

---
<div align="center"><b>Feito com ❤️ — migração Pygame → Next.js na branch <code>feature/nextjs-migration</code></b></div>
