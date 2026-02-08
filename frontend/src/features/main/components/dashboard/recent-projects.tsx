import { StatusBadge } from "@/shared/components/badge";
import { Card } from "@/shared/components/card";
import { StatusDot } from "@/shared/components/status-dot";
import { ArrowRight } from "lucide-react";
import Link from "next/link";
import type { RecentProject } from "../../schemas";

const qgBadgeVariant = {
  OK: "success",
  WARN: "warning",
  ERROR: "error",
  NONE: "neutral",
} as const;

interface RecentProjectsProps {
  projects: RecentProject[];
}

export function RecentProjects({ projects }: Readonly<RecentProjectsProps>) {
  return (
    <Card className="animate-[fade-in_0.4s_ease-out_0.2s_both]">
      <div className="mb-(--space-4) flex items-center justify-between">
        <h2 className="font-semibold text-(--color-neutral-950) text-[length:var(--text-heading)]">
          Recent Projects
        </h2>
        <Link
          href="/projects"
          className="flex items-center gap-(--space-1) font-medium text-(--color-brand-primary) text-[length:var(--text-small)] transition-colors hover:text-(--color-brand-primary-light)"
        >
          View all
          <ArrowRight size={14} />
        </Link>
      </div>

      <div className="flex flex-col divide-y divide-(--color-neutral-200)">
        {projects.map((project) => (
          <Link
            key={project.id}
            href={`/projects/${project.id}`}
            className="flex items-center justify-between py-(--space-3) transition-colors hover:bg-(--color-neutral-50) -mx-(--space-2) px-(--space-2) rounded-(--radius-md)"
          >
            <div className="flex items-center gap-(--space-3)">
              <StatusDot
                color={project.in_production ? "success" : "neutral"}
              />
              <div>
                <p className="font-medium text-(--color-neutral-950) text-[length:var(--text-body)]">
                  {project.name}
                </p>
                <p className="text-(--color-neutral-500) text-[length:var(--text-small)]">
                  {new Date(project.created_at).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </p>
              </div>
            </div>
            <StatusBadge variant={qgBadgeVariant[project.quality_gate_status]}>
              {project.quality_gate_status}
            </StatusBadge>
          </Link>
        ))}
      </div>
    </Card>
  );
}
