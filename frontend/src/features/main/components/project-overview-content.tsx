"use client";

import { Button } from "@/shared/components/button";
import { EmptyState } from "@/shared/components/empty-state";
import { AlertTriangle } from "lucide-react";
import { useProject } from "../hooks";
import { DeploymentStagesCard } from "./deployment-stages-card";
import { ProjectHero } from "./project-hero";
import { ProjectOverviewSkeleton } from "./project-overview-skeleton";
import { QualityGateCard } from "./quality-gate-card";
import { TeamMembersCard } from "./team-members-card";

export function ProjectOverviewContent({
  projectId,
}: Readonly<{ projectId: string }>) {
  const { data: project, isLoading, isError, refetch } = useProject(projectId);

  if (isLoading) return <ProjectOverviewSkeleton />;

  if (isError || !project) {
    return (
      <EmptyState
        icon={<AlertTriangle size={64} />}
        heading="Failed to load project"
        description="An error occurred while loading the project details."
        action={
          <Button variant="primary-dark" onClick={() => refetch()}>
            Retry
          </Button>
        }
      />
    );
  }

  return (
    <div className="flex flex-col gap-(--space-6)">
      <ProjectHero project={project} />

      <div className="grid grid-cols-1 gap-(--space-4) lg:grid-cols-3">
        {project.quality_gate && (
          <QualityGateCard qualityGate={project.quality_gate} />
        )}
        <DeploymentStagesCard stages={project.stages} />
        <TeamMembersCard members={project.members} />
      </div>
    </div>
  );
}
