"use client";

import { getToken } from "@/shared/token-storage";
import { useSyncExternalStore } from "react";

function subscribe(callback: () => void) {
  window.addEventListener("storage", callback);
  return () => window.removeEventListener("storage", callback);
}

function getSnapshot() {
  return getToken() !== null;
}

function getServerSnapshot() {
  return false;
}

export function useAuth() {
  const isAuthenticated = useSyncExternalStore(
    subscribe,
    getSnapshot,
    getServerSnapshot,
  );
  return { isAuthenticated };
}
