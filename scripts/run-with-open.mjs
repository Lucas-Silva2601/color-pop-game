// Roda o Next.js (dev ou start) e abre o navegador automaticamente.
// Uso: node scripts/run-with-open.mjs dev -- -p 3000
// Pula a abertura com: NO_OPEN=1 / BROWSER=none
import { spawn, exec } from "node:child_process";
import path from "node:path";

const mode = process.argv[2] === "start" ? "start" : "dev";
// Remove separadores "--" (npm/node) — o Next não precisa deles e os
// interpretaria como diretório do projeto.
const extraArgs = process.argv.slice(3).filter((a) => a !== "--");

function resolvePort() {
  if (process.env.PORT) return Number(process.env.PORT);
  const idx = extraArgs.findIndex((a) => a === "-p" || a === "--port");
  if (idx !== -1 && extraArgs[idx + 1]) return Number(extraArgs[idx + 1]);
  return 3000;
}

const port = resolvePort();
const url = `http://localhost:${port}`;

function shouldOpen() {
  if (process.env.NO_OPEN === "1") return false;
  if (process.env.BROWSER === "none") return false;
  return true;
}

function openBrowser(target) {
  const platform = process.platform;
  const cmd =
    platform === "win32"
      ? `start "" "${target}"`
      : platform === "darwin"
        ? `open "${target}"`
        : `xdg-open "${target}"`;
  exec(cmd, (err) => {
    if (err) console.log(`[run-with-open] Abra manualmente: ${target}`);
    else console.log(`[run-with-open] Navegador aberto em ${target}`);
  });
}

async function waitForServer(timeoutMs = 60000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url, { method: "HEAD" });
      if (res.ok || res.status < 500) return true;
    } catch {
      // ainda subindo
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

// Invoca o binário local do Next diretamente (sem npx — evita shims
// quebrados de node_modules/.bin no Windows).
const nextBin = path.join(process.cwd(), "node_modules", "next", "dist", "bin", "next");
const command = [`"${process.execPath}"`, `"${nextBin}"`, mode, ...extraArgs]
  .map((a) => (a.startsWith('"') ? a : `"${a.replace(/"/g, "")}"`))
  .join(" ");
const child = spawn(command, {
  stdio: "inherit",
  shell: true,
  env: { ...process.env, PORT: String(port) },
});

if (shouldOpen()) {
  waitForServer().then((ready) => {
    if (ready) openBrowser(url);
    else console.log(`[run-with-open] Timeout aguardando ${url}`);
  });
} else {
  console.log(`[run-with-open] Abertura automática desativada. App em ${url}`);
}

child.on("exit", (code) => process.exit(code ?? 0));
