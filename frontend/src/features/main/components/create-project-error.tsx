"use client";

import { Button } from "@/shared/components/button";
import { AlertTriangle } from "lucide-react";
import * as m from "motion/react-client";

interface CreateProjectErrorProps {
  onRetry: () => void;
}

export function CreateProjectError({
  onRetry,
}: Readonly<CreateProjectErrorProps>) {
  return (
    <m.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="flex max-w-120 flex-col items-center text-center"
    >
      <m.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{
          delay: 0.15,
          type: "spring",
          stiffness: 300,
          damping: 20,
        }}
      >
        <AlertTriangle size={56} className="text-(--color-error)" />
      </m.div>
      <h2 className="mt-(--space-4) font-semibold text-(--color-neutral-950)">
        Failed to create project
      </h2>
      <p className="mt-(--space-2) text-(--color-neutral-500)">
        Please try again or contact support.
      </p>
      <div className="mt-(--space-6)">
        <Button variant="primary-dark" onClick={onRetry}>
          Try Again
        </Button>
      </div>
    </m.div>
  );
}
