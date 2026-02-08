import { AUTH_LOGIN, AUTH_LOGOUT } from "@/api/endpoints";
import { post, postForm } from "@/api/http";
import { tokenSchema, type TokenResponse } from "../schemas";

export async function login(email: string, password: string) {
  const params = new URLSearchParams();
  params.set("username", email);
  params.set("password", password);
  const data = await postForm<TokenResponse>(AUTH_LOGIN, params);
  return tokenSchema.parse(data);
}

export async function logout() {
  await post<void>(AUTH_LOGOUT);
}
