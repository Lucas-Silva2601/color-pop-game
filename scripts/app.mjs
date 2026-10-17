// Gerenciador da aplicação em segundo plano.
//
// Uso:
//   node scripts/app.mjs start [--prod] [--port 3000] [--no-open]
//   node scripts/app.mjs stop
//   node scripts/app.mjs restart [--prod] [--port 3000] [--no-open]
//   node scripts/app.mjs status
//   node scripts/app.mjs open
//
// O estado (PID/porta/modo) fica em .app.pid e os logs em .app.log.
// Se a porta preferida estiver ocupada, a próxima livre é usada sozinha.
import { spawn } from "node:child_process";
import {
  existsSync,
  openSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import net from "node:net";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const APP_ID = "color-pop-game";
const STATE_FILE = path.join(ROOT, ".app.pid");
const LOG_FILE = path.join(ROOT, ".app.log");
const DEFAULT_PORT = 3000;
const READY_TIMEOUT_MS = 120_000;

// ---------------------------------------------------------------- argumentos

const argv = process.argv.slice(2);
const command = (argv.shift() ?? "start").toLowerCase();
const flags = new Set(argv.filter((a) => a.startsWith("--")));
const prod = flags.has("--prod");
const noOpen = flags.has("--no-open") || process.env.NO_OPEN === "1";

function readOption(name, short) {
  const idx = argv.findIndex((a) => a === name || a === short);
  if (idx === -1) return undefined;
  const value = Number(argv[idx + 1]);
  return Number.isFinite(value) && value > 0 ? value : undefined;
}

const explicitPort = readOption("--port", "-p");

// -------------------------------------------------------------------- estado

function readState() {
  try {
    const state = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    if (state?.app !== APP_ID || !Number.isInteger(state.pid)) return null;
    return state;
  } catch {
    return null;
  }
}

function saveState(state) {
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function clearState() {
  rmSync(STATE_FILE, { force: true });
}

function isAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (err) {
    // EPERM = processo existe, mas sem permissão para sinalizar.
    return err.code === "EPERM";
  }
}

function isRunning() {
  const state = readState();
  return state && isAlive(state.pid) ? state : null;
}

// --------------------------------------------------------------------- porta

function isPortFree(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once("error", () => resolve(false));
    server.once("listening", () => server.close(() => resolve(true)));
    server.listen({ port, exclusive: true });
  });
}

async function findFreePort(preferred) {
  for (let port = preferred; port < preferred + 25; port += 1) {
    if (await isPortFree(port)) return port;
  }
  throw new Error(`Nenhuma porta livre entre ${preferred} e ${preferred + 24}.`);
}

async function waitForServer(url, timeoutMs, pid) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (pid && !isAlive(pid)) return false;
    try {
      const res = await fetch(url, {
        method: "GET",
        signal: AbortSignal.timeout(2000),
      });
      if (res.status < 500) return true;
    } catch {
      // servidor ainda subindo
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

// ------------------------------------------------------------------ navegador

function openBrowser(url) {
  const options = { detached: true, stdio: "ignore", windowsHide: true };
  if (process.platform === "win32") {
    spawn("cmd.exe", ["/c", "start", "", url], options).unref();
  } else if (process.platform === "darwin") {
    spawn("open", [url], options).unref();
  } else {
    spawn("xdg-open", [url], options).unref();
  }
}

// ---------------------------------------------------------------- ciclo de vida

function nextBin() {
  const bin = path.join(
    ROOT,
    "node_modules",
    "next",
    "dist",
    "bin",
    "next",
  );
  if (!existsSync(bin)) {
    throw new Error(
      "Next.js não encontrado em node_modules. Rode `npm install` primeiro.",
    );
  }
  return bin;
}

function tailLog(lines = 20) {
  try {
    const content = readFileSync(LOG_FILE, "utf8").trimEnd().split(/\r?\n/);
    return content.slice(-lines).join("\n");
  } catch {
    return "(sem log)";
  }
}

function logSize() {
  try {
    return statSync(LOG_FILE).size;
  } catch {
    return 0;
  }
}

function logSince(offset) {
  try {
    return readFileSync(LOG_FILE).subarray(offset).toString("utf8");
  } catch {
    return "";
  }
}

function rotateLogIfNeeded() {
  try {
    if (statSync(LOG_FILE).size > 2 * 1024 * 1024) {
      writeFileSync(LOG_FILE, "");
    }
  } catch {
    // log ainda não existe
  }
}

function killTree(pid, signal = "SIGTERM") {
  return new Promise((resolve) => {
    if (process.platform === "win32") {
      // /T = árvore inteira, /F = força (usado só no fallback).
      const args = ["/PID", String(pid), "/T"];
      if (signal === "SIGKILL") args.push("/F");
      const killer = spawn("taskkill", args, {
        stdio: "ignore",
        windowsHide: true,
      });
      killer.once("exit", () => resolve());
      killer.once("error", () => resolve());
      return;
    }

    try {
      // O processo foi criado "detached", então também lidera um grupo.
      process.kill(-pid, signal);
    } catch {
      try {
        process.kill(pid, signal);
      } catch {
        // já morreu
      }
    }
    resolve();
  });
}

async function waitUntil(predicate, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (predicate()) return true;
    await new Promise((r) => setTimeout(r, 200));
  }
  return predicate();
}

async function stop({ quiet = false } = {}) {
  const state = readState();

  if (!state) {
    if (!quiet) console.log("[app] Nenhuma instância registrada. Nada a parar.");
    clearState();
    return true;
  }

  if (!isAlive(state.pid)) {
    clearState();
    if (!quiet)
      console.log("[app] O processo já não estava rodando. Estado limpo.");
    return true;
  }

  if (!quiet)
    console.log(`[app] Parando ${state.mode === "start" ? "produção" : "dev"} (pid ${state.pid})...`);

  await killTree(state.pid, "SIGTERM");
  let stopped = await waitUntil(() => !isAlive(state.pid), 8000);

  if (!stopped) {
    await killTree(state.pid, "SIGKILL");
    stopped = await waitUntil(() => !isAlive(state.pid), 5000);
  }

  if (!stopped) {
    console.error(`[app] Não foi possível encerrar o pid ${state.pid}.`);
    return false;
  }

  clearState();

  // No Windows a porta pode levar alguns instantes para ser liberada.
  if (state.port) {
    const freed = await waitUntilAsync(() => isPortFree(state.port), 6000);
    if (!freed && !quiet) {
      console.log(`[app] Aviso: a porta ${state.port} ainda está ocupada.`);
    }
  }

  if (!quiet) console.log("[app] Aplicação parada.");
  return true;
}

async function start({
  port,
  prod: isProd = prod,
  open = !noOpen,
  attempt = 1,
} = {}) {
  const running = isRunning();
  if (running) {
    const responsive = await waitForServer(running.url, 5000, running.pid);
    if (!responsive) {
      console.error(
        `[app] O processo ${running.pid} existe mas não responde em ${running.url}.`,
      );
      console.error("[app] Use `npm run app:restart` (ou `app:stop`).");
      return false;
    }
    console.log(`[app] Já está rodando (pid ${running.pid}) em ${running.url}`);
    if (open) openBrowser(running.url);
    return true;
  }

  // Estado órfão de uma execução anterior que morreu.
  if (readState()) clearState();

  const mode = isProd ? "start" : "dev";

  if (isProd && !existsSync(path.join(ROOT, ".next", "BUILD_ID"))) {
    console.error(
      "[app] Build de produção não encontrado. Rode `npm run build` antes de usar --prod.",
    );
    return false;
  }

  const envPort = Number(process.env.PORT);
  const requested =
    port ??
    explicitPort ??
    (Number.isFinite(envPort) && envPort > 0 ? envPort : DEFAULT_PORT);
  const preferred = requested;
  const chosenPort = await findFreePort(preferred);
  if (chosenPort !== preferred) {
    console.log(`[app] Porta ${preferred} ocupada; usando ${chosenPort}.`);
  }

  const url = `http://localhost:${chosenPort}`;
  rotateLogIfNeeded();
  const logOffset = logSize();
  const logFd = openSync(LOG_FILE, "a");

  const child = spawn(
    process.execPath,
    [nextBin(), mode, "-p", String(chosenPort)],
    {
      cwd: ROOT,
      detached: true,
      windowsHide: true,
      stdio: ["ignore", logFd, logFd],
      env: { ...process.env, PORT: String(chosenPort), NO_OPEN: "1" },
    },
  );
  child.unref();

  const state = {
    app: APP_ID,
    pid: child.pid,
    port: chosenPort,
    mode,
    url,
    startedAt: new Date().toISOString(),
  };
  saveState(state);

  console.log(
    `[app] Iniciando ${isProd ? "produção" : "dev"} (pid ${child.pid}) em ${url}...`,
  );

  const ready = await waitForServer(url, READY_TIMEOUT_MS, child.pid);

  if (!ready) {
    const recentLog = logSince(logOffset);
    const stateStillOurs = readState()?.pid === child.pid;
    if (stateStillOurs) await stop({ quiet: true });

    // No Windows, antivírus/indexador às vezes segura arquivos do .next
    // (EBUSY) logo após um stop. Uma segunda tentativa resolve.
    const lockedOnWindows =
      process.platform === "win32" &&
      /EBUSY|resource busy or locked/i.test(recentLog);

    if (attempt === 1 && lockedOnWindows) {
      console.log("[app] Arquivos do build estavam em uso. Tentando de novo...");
      await waitUntilAsync(() => isPortFree(chosenPort), 10_000);
      await new Promise((r) => setTimeout(r, 1500));
      return start({ port: chosenPort, prod: isProd, open, attempt: 2 });
    }

    console.error(`[app] A aplicação não respondeu em ${url}.`);
    console.error(`[app] Últimas linhas de ${path.basename(LOG_FILE)}:\n${tailLog()}`);
    return false;
  }

  console.log(`[app] Pronta em ${url} (log: ${path.basename(LOG_FILE)})`);
  if (open) {
    openBrowser(url);
    console.log("[app] Abrindo o navegador...");
  }
  return true;
}

async function status() {
  const state = readState();

  if (!state || !isAlive(state.pid)) {
    if (state) clearState();
    console.log("[app] Parada.");
    return true;
  }

  const reachable = await waitForServer(state.url, 3000, state.pid);
  console.log(`[app] Rodando (${state.mode === "start" ? "produção" : "dev"})`);
  console.log(`      URL:   ${state.url}`);
  console.log(`      PID:   ${state.pid}`);
  console.log(`      Desde: ${state.startedAt}`);
  console.log(`      HTTP:  ${reachable ? "respondendo" : "sem resposta ainda"}`);
  console.log(`      Log:   ${LOG_FILE}`);
  return true;
}

async function restart(options) {
  const previous = readState();
  const wasProd = previous?.mode === "start";
  const port = options.port ?? previous?.port;

  if (!(await stop())) return false;

  // Garante que a porta antiga foi realmente liberada antes de subir de novo.
  if (port) {
    const freed = await waitUntilAsync(() => isPortFree(port), 10_000);
    if (!freed) console.log(`[app] Aviso: porta ${port} ainda ocupada.`);
  }

  return start({
    port,
    prod: flags.has("--prod") ? true : wasProd,
    open: !noOpen,
  });
}

async function waitUntilAsync(predicate, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await predicate()) return true;
    await new Promise((r) => setTimeout(r, 300));
  }
  return Boolean(await predicate());
}

async function open() {
  const running = isRunning();
  if (!running) {
    console.error("[app] Aplicação não está rodando. Use `npm run app:start`.");
    return false;
  }
  console.log(`[app] Abrindo ${running.url}`);
  openBrowser(running.url);
  return true;
}

// ---------------------------------------------------------------------- main

const actions = {
  start: () => start(),
  stop: () => stop(),
  restart: () => restart(explicitPort ? { port: explicitPort } : {}),
  status: () => status(),
  open: () => open(),
};

const action = actions[command];

if (!action) {
  console.error(`[app] Comando desconhecido: "${command}"`);
  console.error("[app] Use: start | stop | restart | status | open");
  process.exit(1);
}

try {
  const ok = await action();
  process.exit(ok ? 0 : 1);
} catch (err) {
  console.error(`[app] Erro: ${err.message}`);
  process.exit(1);
}
