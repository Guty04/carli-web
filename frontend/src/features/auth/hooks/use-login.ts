"use client";

import { setToken } from "@/shared/token-storage";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import type { LoginInput } from "../schemas";
import { login } from "../services/auth.service";

export function useLogin() {
  const router = useRouter();

  return useMutation({
    mutationFn: (data: LoginInput) => login(data.email, data.password),
    onSuccess: (response) => {
      setToken(response.access_token);
      router.push("/projects");
    },
  });
}
