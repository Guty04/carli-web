import type { StageStatus } from "../schemas";

const stageLabels: Record<string, string> = {
  development: "Dev",
  staging: "Stg",
  production: "Prod",
};

const stageColors: Record<string, string> = {
  development: "var(--color-stage-dev)",
  staging: "var(--color-stage-staging)",
  production: "var(--color-stage-prod)",
};

export function StageIndicator({
  stage,
}: Readonly<{ stage: StageStatus }>) {
  const label = stageLabels[stage.stage] ?? stage.stage;
  const color = stageColors[stage.stage] ?? "var(--color-neutral-500)";

  return (
    <div className="flex items-center gap-(--space-1)" title={`${stage.stage} — ${stage.is_ready ? "Ready" : "Not Ready"}`}>
      <span
        className="inline-block h-2 w-2 shrink-0 rounded-full"
        style={{
          backgroundColor: stage.is_ready ? color : "var(--color-neutral-300)",
          boxShadow: stage.is_ready ? `0 0 6px ${color}40` : "none",
        }}
      />
      <span
        className={`text-(--text-small) font-medium ${
          stage.is_ready
            ? "text-(--color-neutral-950)"
            : "text-(--color-neutral-500)"
        }`}
      >
        {label}
      </span>
    </div>
  );
}
