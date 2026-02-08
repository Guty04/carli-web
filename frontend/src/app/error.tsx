"use client";

import { AlertTriangle } from "lucide-react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-(--color-neutral-50) p-(--space-4)">
      <AlertTriangle size={64} className="text-(--color-error)" />
      <h1 className="mt-(--space-4) text-(--text-heading) font-semibold text-(--color-neutral-950)">
        Something went wrong
      </h1>
      <p className="mt-(--space-2) text-(--text-body) text-(--color-neutral-500)">
        {error.message || "An unexpected error occurred."}
      </p>
      <button
        onClick={reset}
        className="mt-(--space-6) inline-flex min-h-11 items-center justify-center rounded-(--radius-full) bg-(--color-brand-dark) px-6 py-2.5 text-(--text-body-medium) font-medium text-white transition-colors hover:bg-(--color-brand-dark-hover)"
      >
        Try Again
      </button>
    </div>
  );
}
