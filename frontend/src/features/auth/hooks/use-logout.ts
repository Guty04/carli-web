"use client";

import { clearToken } from "@/shared/token-storage";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { logout } from "../services/auth.service";

export function useLogout() {
  const router = useRouter();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: logout,
    onSettled: () => {
      clearToken();
      queryClient.clear();
      router.push("/login");
    },
  });
}
