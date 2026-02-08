"use client";

import * as m from "motion/react-client";
import type { ReactNode } from "react";

interface EmptyStateProps {
  icon: ReactNode;
  heading: string;
  description?: string;
  action?: ReactNode;
}

export function EmptyState({
  icon,
  heading,
  description,
  action,
}: Readonly<EmptyStateProps>) {
  return (
    <m.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="flex flex-col items-center justify-center py-12 text-center"
    >
      <m.div
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.1, type: "spring", stiffness: 200, damping: 15 }}
        className="mb-(--space-4) text-(--color-neutral-300)"
      >
        {icon}
      </m.div>
      <h3 className="text-(--text-heading) font-semibold">{heading}</h3>
      {description && (
        <p className="mt-(--space-2) max-w-sm text-(--color-neutral-500)">
          {description}
        </p>
      )}
      {action && <div className="mt-(--space-6)">{action}</div>}
    </m.div>
  );
}
