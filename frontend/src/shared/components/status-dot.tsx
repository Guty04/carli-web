type DotColor = "success" | "error" | "warning" | "info" | "neutral";

interface StatusDotProps {
  color: DotColor;
  className?: string;
}

const colorMap: Record<DotColor, string> = {
  success: "bg-(--color-success)",
  error: "bg-(--color-error)",
  warning: "bg-(--color-warning)",
  info: "bg-(--color-info)",
  neutral: "bg-(--color-neutral-500)",
};

export function StatusDot({ color, className = "" }: Readonly<StatusDotProps>) {
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${colorMap[color]} ${className}`}
      aria-hidden="true"
    />
  );
}
