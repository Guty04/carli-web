"use client";

import { Button } from "@/shared/components/button";
import { EmptyState } from "@/shared/components/empty-state";
import { FolderKanban } from "lucide-react";
import * as m from "motion/react-client";
import Link from "next/link";
import { useProjects } from "../hooks";
import { ProjectCard } from "./project-card";
import { ProjectCardSkeleton } from "./project-card-skeleton";

export function ProjectsList() {
  const { data: projects, isLoading, isError } = useProjects();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-(--space-4) sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-[repeat(auto-fill,minmax(300px,1fr))]">
        {Array.from({ length: 6 }).map((_, i) => (
          <ProjectCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <EmptyState
        icon={<FolderKanban size={64} />}
        heading="Failed to load projects"
        description="An error occurred while loading your projects. Please try again."
      />
    );
  }

  if (!projects || projects.length === 0) {
    return (
      <EmptyState
        icon={<FolderKanban size={64} />}
        heading="No projects yet"
        description="Create your first project to get started with CI/CD orchestration."
        action={
          <Link href="/projects/new">
            <Button variant="primary-dark">Create Project</Button>
          </Link>
        }
      />
    );
  }

  return (
    <div className="grid grid-cols-1 gap-(--space-4) sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-[repeat(auto-fill,minmax(300px,1fr))]">
      {projects.map((project, i) => (
        <m.div
          key={project.id}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: i * 0.05, ease: "easeOut" }}
        >
          <ProjectCard project={project} />
        </m.div>
      ))}
    </div>
  );
}
