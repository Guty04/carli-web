"use client";

import { StatusBadge } from "@/shared/components/badge";
import { CopyButton } from "@/shared/components/copy-button";
import { ArrowLeft, Calendar } from "lucide-react";
import * as m from "motion/react-client";
import Link from "next/link";
import type { ProjectOverview } from "../schemas";

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function getQualityGateVariant(status?: string) {
  if (status === "OK") return "success" as const;
  if (status === "WARN") return "warning" as const;
  if (status === "ERROR") return "error" as const;
  return "neutral" as const;
}

function getQualityGateLabel(status?: string) {
  if (status === "OK") return "Passed";
  if (status === "WARN") return "Warning";
  if (status === "ERROR") return "Failed";
  return "Unknown";
}

export function ProjectHero({
  project,
}: Readonly<{ project: ProjectOverview }>) {
  return (
    <m.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="relative min-h-35 overflow-hidden rounded-lg bg-linear-to-r from-(--color-brand-primary) to-[#2563EB] p-(--space-4) text-white lg:min-h-50 lg:rounded-b-(--radius-xl) lg:p-(--space-6)"
    >
      <Link
        href="/projects"
        className="mb-(--space-3) inline-flex items-center gap-(--space-2) text-white/80 hover:text-white"
      >
        <ArrowLeft size={18} />
        Back
      </Link>

      <div className="flex flex-wrap items-center gap-(--space-2)">
        {project.quality_gate && (
          <StatusBadge
            variant={getQualityGateVariant(project.quality_gate.status)}
          >
            {getQualityGateLabel(project.quality_gate.status)}
          </StatusBadge>
        )}
      </div>

      <h1 className="mt-(--space-3) text-[24px] font-bold lg:text-[36px] lg:font-extrabold">
        {project.name}
      </h1>

      <div className="mt-(--space-2) flex flex-wrap items-center gap-(--space-4) text-white/80">
        <div className="flex items-center gap-(--space-2)">
          <code className="truncate font-mono text-(--text-mono)">
            {project.url_repository}
          </code>
          <CopyButton
            text={project.url_repository}
            className="text-white/80 hover:text-white"
          />
        </div>
        <div className="flex items-center gap-(--space-1)">
          <Calendar size={14} />
          <span className="">Created on {formatDate(project.created_at)}</span>
        </div>
      </div>
    </m.div>
  );
}
