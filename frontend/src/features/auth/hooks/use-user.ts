"use client";

import { getToken } from "@/shared/token-storage";
import { jwtDecode } from "jwt-decode";
import { useSyncExternalStore } from "react";

interface UserPayload {
  sub: string;
  name: string;
  role: string;
}

let cachedToken: string | null = null;
let cachedUser: UserPayload | null = null;

function subscribe(callback: () => void) {
  window.addEventListener("storage", callback);
  return () => window.removeEventListener("storage", callback);
}

export function parseTokenPayload(token: string): UserPayload | null {
  try {
    return jwtDecode<UserPayload>(token);
  } catch {
    return null;
  }
}

function getSnapshot(): UserPayload | null {
  const token = getToken();

  if (token === cachedToken) return cachedUser;

  cachedToken = token;
  cachedUser = token ? parseTokenPayload(token) : null;

  return cachedUser;
}

function getServerSnapshot(): UserPayload | null {
  return null;
}

export function useUser() {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}
