"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { CreateProjectView } from "@/features/main/components/create-project-view";

export default function NewProjectPage() {
  return (
    <>
      <div className="mb-(--space-6)">
        <Link
          href="/projects"
          className="mb-(--space-4) inline-flex items-center gap-(--space-2) text-(--text-body) text-(--color-neutral-500) hover:text-(--color-neutral-700)"
        >
          <ArrowLeft size={18} />
          Back to Projects
        </Link>
        <h1 className="text-(--text-display) font-bold text-(--color-neutral-950)">
          New Project
        </h1>
      </div>
      <CreateProjectView />
    </>
  );
}
