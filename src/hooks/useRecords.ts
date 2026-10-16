"use client";

import { STORAGE_KEY } from "@/lib/config";

export type Records = Record<string, number>;

export function loadRecords(): Records {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    return JSON.parse(raw) as Records;
  } catch {
    return {};
  }
}

export function saveRecord(modeKey: string, value: number): Records {
  const current = loadRecords();
  const best = current[modeKey] ?? 0;
  const next = { ...current, [modeKey]: Math.max(best, value) };
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // storage indisponível (SSR/privado) — ignora
  }
  return next;
}

export function modeKey(mode: string, behavior: string) {
  return `${mode}_${behavior}`;
}
