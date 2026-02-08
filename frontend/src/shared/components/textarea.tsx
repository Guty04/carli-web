"use client";

import { forwardRef, type TextareaHTMLAttributes } from "react";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  function Textarea(
    { label, error, helperText, className = "", id, ...props },
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
        <textarea
          ref={ref}
          id={inputId}
          className={`min-h-25 w-full resize-y border bg-white p-(--space-3) px-(--space-4) rounded-md text-(--color-neutral-950) placeholder:text-(--color-neutral-500) focus:outline-none focus:ring-[3px] disabled:cursor-not-allowed disabled:bg-(--color-neutral-100) ${
            error
              ? "border-(--color-error) focus:ring-error/15"
              : "border-(--color-neutral-200) focus:border-(--color-brand-accent) focus:ring-(--color-brand-accent)/15"
          } ${className}`}
          {...props}
        />
        {error && <p className=" text-(--color-error)">{error}</p>}
        {helperText && !error && (
          <p className=" text-(--color-neutral-500)">{helperText}</p>
        )}
      </div>
    );
  },
);
