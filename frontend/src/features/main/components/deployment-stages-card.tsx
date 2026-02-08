import { Card } from "@/shared/components/card";
import { StatusDot } from "@/shared/components/status-dot";
import { Code, FlaskConical, Globe } from "lucide-react";
import type { StageStatus } from "../schemas";

const stageConfig: Record<
  string,
  { label: string; icon: typeof Code; color: string }
> = {
  development: {
    label: "Development",
    icon: Code,
    color: "var(--color-stage-dev)",
  },
  staging: {
    label: "Staging",
    icon: FlaskConical,
    color: "var(--color-stage-staging)",
  },
  production: {
    label: "Production",
    icon: Globe,
    color: "var(--color-stage-prod)",
  },
};

export function DeploymentStagesCard({
  stages,
}: Readonly<{ stages: StageStatus[] }>) {
  return (
    <Card className="flex flex-col gap-(--space-4)">
      <h3 className="font-semibold text-(--color-neutral-950)">
        Deployment Stages
      </h3>

      <div className="flex flex-col gap-(--space-3)">
        {stages.map((stage) => {
          const config = stageConfig[stage.stage];
          if (!config) return null;
          const Icon = config.icon;

          return (
            <div
              key={stage.stage}
              className="flex items-center justify-between border-b border-(--color-neutral-100) pb-(--space-3) last:border-0 last:pb-0"
            >
              <div className="flex items-center gap-(--space-3)">
                <div
                  className="flex h-9 w-9 items-center justify-center rounded-md"
                  style={{
                    backgroundColor: `${config.color}15`,
                    color: config.color,
                  }}
                >
                  <Icon size={18} />
                </div>
                <span className="font-medium text-(--color-neutral-950)">
                  {config.label}
                </span>
              </div>
              <div className="flex items-center gap-(--space-2)">
                <StatusDot color={stage.is_ready ? "success" : "error"} />
                <span
                  className={` font-medium ${
                    stage.is_ready
                      ? "text-(--color-success)"
                      : "text-(--color-error)"
                  }`}
                >
                  {stage.is_ready ? "Online" : "Offline"}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
