"use client";

import { ChevronDown } from "lucide-react";
import { forwardRef, type SelectHTMLAttributes } from "react";

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  helperText?: string;
  options: SelectOption[];
  placeholder?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  function Select(
    {
      label,
      error,
      helperText,
      options,
      placeholder,
      className = "",
      id,
      ...props
    },
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
          <select
            ref={ref}
            id={inputId}
            className={`h-11 w-full appearance-none rounded-md border bg-white px-(--space-4) pr-10 text-(--color-neutral-950) focus:outline-none focus:ring-[3px] disabled:cursor-not-allowed disabled:bg-(--color-neutral-100) ${
              error
                ? "border-(--color-error) focus:ring-error/15"
                : "border-(--color-neutral-200) focus:border-(--color-brand-accent) focus:ring-(--color-brand-accent)/15"
            } ${className}`}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
          <ChevronDown
            size={16}
            className="pointer-events-none absolute right-(--space-3) top-1/2 -translate-y-1/2 text-(--color-neutral-500)"
          />
        </div>
        {error && <p className=" text-(--color-error)">{error}</p>}
        {helperText && !error && (
          <p className=" text-(--color-neutral-500)">{helperText}</p>
        )}
      </div>
    );
  },
);
