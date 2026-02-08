"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { LoginCard } from "@/features/auth/components/login-card";

function LoginContent() {
  const searchParams = useSearchParams();
  const expired = searchParams.get("expired") === "true";

  return (
    <div className="flex min-h-screen items-center justify-center bg-(--color-neutral-50) p-(--space-4)">
      <LoginCard expiredMessage={expired} />
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginContent />
    </Suspense>
  );
}
