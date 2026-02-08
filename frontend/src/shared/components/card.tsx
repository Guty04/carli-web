import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  hoverable?: boolean;
}

export function Card({
  children,
  hoverable = false,
  className = "",
  ...props
}: Readonly<CardProps>) {
  return (
    <div
      className={`rounded-(--radius-lg) border border-(--color-neutral-200) bg-white p-(--space-5) shadow-(--shadow-md) ${
        hoverable
          ? "cursor-pointer transition-all duration-150 hover:-translate-y-[2px] hover:shadow-(--shadow-lg)"
          : ""
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
