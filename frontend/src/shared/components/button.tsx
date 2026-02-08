"use client";

import { Loader2 } from "lucide-react";
import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";

type ButtonVariant =
  | "primary-dark"
  | "primary-accent"
  | "secondary"
  | "ghost-success"
  | "ghost-danger"
  | "ghost-text";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  loading?: boolean;
  icon?: ReactNode;
  iconPosition?: "left" | "right";
}

const variantClasses: Record<ButtonVariant, string> = {
  "primary-dark":
    "bg-(--color-brand-dark) text-white rounded-(--radius-full) hover:bg-(--color-brand-dark-hover)",
  "primary-accent":
    "bg-(--color-brand-accent) text-white rounded-(--radius-md) hover:bg-(--color-brand-accent-hover)",
  secondary:
    "bg-white text-(--color-neutral-700) border border-(--color-neutral-300) rounded-(--radius-full) hover:bg-(--color-neutral-100)",
  "ghost-success":
    "bg-transparent text-(--color-success) border border-(--color-success) rounded-(--radius-full) hover:bg-(--color-success-light)",
  "ghost-danger":
    "bg-transparent text-(--color-error) border border-(--color-error) rounded-(--radius-full) hover:bg-(--color-error-light)",
  "ghost-text":
    "bg-transparent text-(--color-neutral-500) rounded-(--radius-md) hover:text-(--color-neutral-700)",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button(
    {
      variant = "primary-dark",
      loading = false,
      icon,
      iconPosition = "left",
      children,
      disabled,
      className = "",
      ...props
    },
    ref,
  ) {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={`inline-flex min-h-11 items-center justify-center gap-(--space-2) px-6 py-2.5 text-(--text-body-medium) font-medium transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-50 ${variantClasses[variant]} ${className}`}
        {...props}
      >
        {loading ? (
          <Loader2 size={20} className="animate-spin" />
        ) : (
          <>
            {icon && iconPosition === "left" && icon}
            {children}
            {icon && iconPosition === "right" && icon}
          </>
        )}
      </button>
    );
  },
);
