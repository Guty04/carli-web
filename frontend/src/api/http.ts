import { API_BASE_URL } from "@/configuration/env";
import { getToken } from "@/shared/token-storage";
import { handleResponse } from "./interceptors";

function authHeaders(): HeadersInit {
  const token = getToken();
  if (token) return { Authorization: `Bearer ${token}` };
  return {};
}

function buildUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

export async function get<T>(path: string): Promise<T> {
  const res = await fetch(buildUrl(path), {
    method: "GET",
    headers: { ...authHeaders() },
    credentials: "include",
  });
  return handleResponse<T>(res);
}

export async function post<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(buildUrl(path), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    credentials: "include",
    body: body ? JSON.stringify(body) : undefined,
  });
  return handleResponse<T>(res);
}

export async function postForm<T>(
  path: string,
  body: URLSearchParams,
): Promise<T> {
  const res = await fetch(buildUrl(path), {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      ...authHeaders(),
    },
    credentials: "include",
    body: body.toString(),
  });
  return handleResponse<T>(res);
}

export async function put<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(buildUrl(path), {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    credentials: "include",
    body: body ? JSON.stringify(body) : undefined,
  });
  return handleResponse<T>(res);
}

export async function del<T>(path: string): Promise<T> {
  const res = await fetch(buildUrl(path), {
    method: "DELETE",
    headers: { ...authHeaders() },
    credentials: "include",
  });
  return handleResponse<T>(res);
}
