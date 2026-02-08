interface SkeletonProps {
  width?: string;
  height?: string;
  rounded?: string;
  className?: string;
}

export function Skeleton({
  width,
  height = "20px",
  rounded = "var(--radius-md)",
  className = "",
}: Readonly<SkeletonProps>) {
  return (
    <div
      className={`animate-[shimmer_1.5s_linear_infinite] bg-[length:200%_100%] ${className}`}
      style={{
        width,
        height,
        borderRadius: rounded,
        backgroundImage:
          "linear-gradient(90deg, var(--color-neutral-100) 25%, var(--color-neutral-200) 50%, var(--color-neutral-100) 75%)",
      }}
    />
  );
}
