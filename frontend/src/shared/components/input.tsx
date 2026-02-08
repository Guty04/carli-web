"use client";

import { forwardRef, type InputHTMLAttributes, type ReactNode } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, error, helperText, leftIcon, className = "", id, ...props },
  ref,
) {
  const inputId = id || label?.toLowerCase().replaceAll(/\s+/g, "-");

  return (
    <div className="flex flex-col gap-(--space-2)">
      {label && (
        <label
          htmlFor={inputId}
          className="font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)"
        >
          {label}
        </label>
      )}
      <div className="relative">
        {leftIcon && (
          <span className="pointer-events-none absolute left-(--space-3) top-1/2 -translate-y-1/2 text-(--color-neutral-500)">
            {leftIcon}
          </span>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`h-11 w-full rounded-md border bg-white text-(--color-neutral-950) placeholder:text-(--color-neutral-500) focus:outline-none focus:ring-[3px] disabled:cursor-not-allowed disabled:bg-(--color-neutral-100) ${
            leftIcon ? "pl-11" : "px-(--space-4)"
          } ${
            error
              ? "border-(--color-error) focus:ring-error/15"
              : "border-(--color-neutral-200) focus:border-(--color-brand-accent) focus:ring-(--color-brand-accent)/15"
          } ${leftIcon ? "pr-(--space-4)" : ""} ${className}`}
          {...props}
        />
      </div>
      {error && <p className=" text-(--color-error)">{error}</p>}
      {helperText && !error && (
        <p className=" text-(--color-neutral-500)">{helperText}</p>
      )}
    </div>
  );
});
