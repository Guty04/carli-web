"use client";

import { Card } from "@/shared/components/card";
import { CopyButton } from "@/shared/components/copy-button";
import { Calendar, ExternalLink, GitBranch } from "lucide-react";
import Link from "next/link";
import type { ProjectOverview } from "../schemas";
import { MemberAvatars } from "./member-avatars";
import { QualityGateBadge } from "./quality-gate-badge";
import { StageIndicator } from "./stage-indicator";

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function extractRepoPath(url: string) {
  try {
    return new URL(url).pathname.slice(1);
  } catch {
    return url;
  }
}

export function ProjectCard({
  project,
}: Readonly<{ project: ProjectOverview }>) {
  const stages = project.stages ?? [];
  const members = project.members ?? [];
  const qualityGateStatus = project.quality_gate?.status ?? "NONE";

  return (
    <Link
      href={`/projects/${project.id}`}
      className="block rounded-(--radius-lg) focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--color-brand-accent)"
    >
      <Card hoverable className="group flex flex-col gap-(--space-3)">
        {/* Header: name + quality gate */}
        <div className="flex items-start justify-between gap-(--space-3)">
          <div className="min-w-0 flex-1">
            <h3 className="truncate text-(--text-subheading) font-semibold text-(--color-neutral-950)">
              {project.name}
            </h3>
            <div className="mt-(--space-1) flex items-center gap-(--space-1) text-(--text-small) text-(--color-neutral-500)">
              <GitBranch size={12} className="shrink-0" />
              <span className="min-w-0 truncate font-mono text-(--text-mono)">
                {extractRepoPath(project.url_repository)}
              </span>
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  window.open(project.url_repository, "_blank", "noopener,noreferrer");
                }}
                className="shrink-0 opacity-0 transition-opacity group-hover:opacity-100"
                aria-label="Open repository"
              >
                <ExternalLink size={12} />
              </button>
              <CopyButton text={project.url_repository} />
            </div>
          </div>
          <QualityGateBadge status={qualityGateStatus} />
        </div>

        {/* Stages */}
        {stages.length > 0 && (
          <div className="flex flex-col gap-(--space-2)">
            <span className="text-(--text-label) font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
              Environments
            </span>
            <div className="flex items-center gap-(--space-4)">
              {stages.map((stage) => (
                <StageIndicator key={stage.stage} stage={stage} />
              ))}
            </div>
          </div>
        )}

        {/* Footer: members + date */}
        <div className="flex items-center justify-between border-t border-(--color-neutral-100) pt-(--space-3)">
          {members.length > 0 ? (
            <MemberAvatars members={members} />
          ) : (
            <span />
          )}
          <div className="flex items-center gap-(--space-1) text-(--text-small) text-(--color-neutral-500)">
            <Calendar size={14} />
            <span>{formatDate(project.created_at)}</span>
          </div>
        </div>
      </Card>
    </Link>
  );
}
