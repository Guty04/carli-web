import type { ReactNode } from "react";

type BadgeVariant = "success" | "error" | "warning" | "info" | "neutral";

interface StatusBadgeProps {
  variant: BadgeVariant;
  children: ReactNode;
  dot?: boolean;
}

const statusStyles: Record<
  BadgeVariant,
  { dot: string; text: string; bg: string }
> = {
  success: {
    dot: "bg-(--color-success)",
    text: "text-[#15803D]",
    bg: "bg-(--color-success-light)",
  },
  error: {
    dot: "bg-(--color-error)",
    text: "text-[#B91C1C]",
    bg: "bg-(--color-error-light)",
  },
  warning: {
    dot: "bg-(--color-warning)",
    text: "text-[#92400E]",
    bg: "bg-(--color-warning-light)",
  },
  info: {
    dot: "bg-(--color-info)",
    text: "text-(--color-info)",
    bg: "bg-(--color-info-light)",
  },
  neutral: {
    dot: "bg-(--color-neutral-500)",
    text: "text-(--color-neutral-700)",
    bg: "bg-(--color-neutral-100)",
  },
};

export function StatusBadge({
  variant,
  children,
  dot = true,
}: Readonly<StatusBadgeProps>) {
  const styles = statusStyles[variant];
  return (
    <span
      className={`inline-flex items-center gap-(--space-1) rounded-full ${styles.bg} px-3 py-1  font-semibold ${styles.text}`}
    >
      {dot && (
        <span
          className={`inline-block h-1.5 w-1.5 rounded-full ${styles.dot}`}
        />
      )}
      {children}
    </span>
  );
}

interface CategoryBadgeProps {
  children: ReactNode;
}

export function CategoryBadge({ children }: Readonly<CategoryBadgeProps>) {
  return (
    <span className="inline-flex items-center rounded-sm border border-(--color-neutral-200) bg-(--color-neutral-100) px-2.5 py-1 font-bold uppercase tracking-[0.05em] text-(--color-neutral-700)">
      {children}
    </span>
  );
}
