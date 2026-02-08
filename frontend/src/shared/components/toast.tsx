"use client";

import { AlertTriangle, CheckCircle2, Info, X, XCircle } from "lucide-react";
import * as m from "motion/react-client";
import { useEffect, useState } from "react";

export type ToastVariant = "success" | "error" | "warning" | "info";

interface ToastProps {
  variant: ToastVariant;
  title?: string;
  message: string;
  onClose: () => void;
  duration?: number;
}

const variantStyles: Record<
  ToastVariant,
  { bg: string; icon: typeof CheckCircle2 }
> = {
  success: { bg: "bg-(--color-brand-accent)", icon: CheckCircle2 },
  error: { bg: "bg-(--color-error)", icon: XCircle },
  warning: { bg: "bg-(--color-warning)", icon: AlertTriangle },
  info: { bg: "bg-(--color-info)", icon: Info },
};

export function Toast({
  variant,
  title,
  message,
  onClose,
  duration = 5000,
}: Readonly<ToastProps>) {
  const [exiting, setExiting] = useState(false);
  const { bg, icon: Icon } = variantStyles[variant];

  useEffect(() => {
    const timer = setTimeout(() => setExiting(true), duration - 300);
    const removeTimer = setTimeout(onClose, duration);
    return () => {
      clearTimeout(timer);
      clearTimeout(removeTimer);
    };
  }, [duration, onClose]);

  return (
    <m.div
      role="alert"
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={
        exiting
          ? { opacity: 0, y: 20, scale: 0.95 }
          : { opacity: 1, y: 0, scale: 1 }
      }
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={`${bg} flex w-[calc(100vw-2*var(--space-4))] max-w-[400px] items-start gap-(--space-3) rounded-(--radius-lg) p-(--space-4) pr-(--space-5) text-white shadow-(--shadow-xl) md:w-[400px]`}
    >
      <Icon size={20} className="mt-0.5 shrink-0" />
      <div className="min-w-0 flex-1">
        {title && (
          <p className="text-(--text-body-medium) font-semibold">{title}</p>
        )}
        <p className="">{message}</p>
      </div>
      <button
        onClick={onClose}
        className="shrink-0 rounded-full p-1 hover:bg-white/20"
        aria-label="Close notification"
      >
        <X size={14} />
      </button>
    </m.div>
  );
}
