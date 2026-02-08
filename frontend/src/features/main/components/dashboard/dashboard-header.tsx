export function DashboardHeader() {
  return (
    <div className="animate-[fade-in_0.4s_ease-out]">
      <h1 className="font-bold text-(--color-neutral-950) text-[length:var(--text-display)]">
        Dashboard
      </h1>
      <p className="mt-(--space-1) text-(--color-neutral-500) text-[length:var(--text-body)]">
        Project health overview at a glance
      </p>
    </div>
  );
}
