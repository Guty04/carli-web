import { TOKEN_KEY } from "@/configuration/env";

function isBrowser() {
  return typeof window !== "undefined";
}

export function getToken(): string | null {
  if (!isBrowser()) return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  if (!isBrowser()) return;
  localStorage.setItem(TOKEN_KEY, token);
  window.dispatchEvent(new StorageEvent("storage", { key: TOKEN_KEY }));
}

export function clearToken(): void {
  if (!isBrowser()) return;
  localStorage.removeItem(TOKEN_KEY);
  window.dispatchEvent(new StorageEvent("storage", { key: TOKEN_KEY }));
}
