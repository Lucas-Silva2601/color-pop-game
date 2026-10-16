# 🎮 Color Pop Game — React + Next.js + Tailwind CSS

![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![React](https://img.shields.io/badge/React-19-61DAFB.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-4-38BDF8.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Descrição

**Color Pop** é um puzzle viciante onde o objetivo é deixar todas as bolinhas da mesma cor clicando nelas para alternar entre 2 cores.

- **🎯 Singleplayer:** 120s, máximo de fases possível, recorde em `localStorage`
- **👥 PvP local:** tela dividida (topo vs fundo), melhor de 10 fases
- **🤖 PvE (vs Bot):** IA que a cada 1.2s converte bolas da cor minoritária
- **⚪🔵🟡 Comportamentos:** `parado` | `movimento` (quique livre) | `saltitando` (gravidade)
- **📈 Progressão:** `6 + 2/fase` bolas, velocidade `2.0 + 0.5/fase`, gravidade `0.3 + 0.05/fase`
- **✨ Efeitos:** partículas no clique, animação de escala, sons `bubble_pop.wav`

---

## 🛠️ Stack

- **Next.js 15 (App Router)** + **React 19** + **TypeScript strict**
- **Tailwind CSS v4** (`@import "tailwindcss"`)
- **Canvas 2D** para o jogo a 60fps (`requestAnimationFrame`)
- Sem dependência de game engine — lógica pura em `src/lib/game-logic.ts`

## 📁 Estrutura

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
│   │   ├── config.ts       # Constantes de gameplay (tela, física, cores)
│   │   └── game-logic.ts   # Fases, bolas, colisão, IA, vitória
│   ├── hooks/
│   │   └── useRecords.ts   # Recordes em localStorage
│   └── types/
│       └── game.ts         # GameMode, BallBehavior, BallEntity, Bounds
├── public/
│   ├── sounds/             # bubble_pop.wav, ui_click.wav, ui_hover.wav, bg music
│   └── fonts/              # ModernFont.ttf, PixelFont.ttf
├── docs/
│   └── screenshots/        # Prints do jogo
├── package.json
├── tsconfig.json (paths @/*)
├── next.config.mjs
└── postcss.config.mjs
```

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

## 🎯 Como jogar

1. Escolha modo → comportamento (`Parado` / `Movimento` / `Saltitando`)
2. Clique nas bolinhas para alternar a cor
3. Vença quando **todas na sua área** tiverem a mesma cor
4. PvP/PvE: tela dividida em 2 áreas; no PvE sua área é só a de cima

## 🧪 Qualidade

```bash
npm run lint
npx tsc --noEmit
```

## 🔮 Roadmap

- [ ] Música de fundo com toggle real + WebAudio sprites
- [ ] Leaderboard global (ex: Vercel KV)
- [ ] Temas de cores + modo daltônico
- [ ] PWA / offline + mobile touch tuning
- [ ] Testes Vitest para `game-logic.ts`

---
<div align="center"><b>Feito com ❤️ — React + Next.js + Tailwind CSS</b></div>
