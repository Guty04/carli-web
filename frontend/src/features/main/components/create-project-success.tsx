"use client";

import { Button } from "@/shared/components/button";
import { CopyButton } from "@/shared/components/copy-button";
import { CheckCircle2 } from "lucide-react";
import * as m from "motion/react-client";
import Link from "next/link";
import type { ProjectCreated } from "../schemas";

interface CreateProjectSuccessProps {
  result: ProjectCreated;
  onCreateAnother: () => void;
}

export function CreateProjectSuccess({
  result,
  onCreateAnother,
}: Readonly<CreateProjectSuccessProps>) {
  return (
    <m.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="flex max-w-120 flex-col items-center text-center"
    >
      <m.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{
          delay: 0.15,
          type: "spring",
          stiffness: 300,
          damping: 20,
        }}
      >
        <CheckCircle2 size={56} className="text-(--color-brand-accent)" />
      </m.div>
      <h2 className="mt-(--space-4) font-semibold text-(--color-neutral-950)">
        Project created successfully!
      </h2>

      <div className="mt-(--space-6) flex w-full items-center gap-(--space-2) rounded-md border border-(--color-neutral-200) bg-(--color-neutral-50) px-(--space-4) py-(--space-3)">
        <code className="min-w-0 flex-1 truncate text-left font-mono text-(--color-neutral-700)">
          {result.repo_url}
        </code>
        <CopyButton text={result.repo_url} />
      </div>

      <div className="mt-(--space-8) flex w-full flex-col gap-(--space-3) sm:flex-row">
        <Link href={`/projects/${result.project_id}`} className="flex-1">
          <Button variant="primary-dark" className="w-full">
            Go to Project
          </Button>
        </Link>
        <Button
          variant="secondary"
          className="flex-1"
          onClick={onCreateAnother}
        >
          Create Another
        </Button>
      </div>
    </m.div>
  );
}
