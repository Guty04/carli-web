"use client";

import { Button } from "@/shared/components/button";
import { Plus } from "lucide-react";
import * as m from "motion/react-client";
import Link from "next/link";

export function ProjectsPageHeader() {
  return (
    <m.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="mb-(--space-6) flex items-center justify-between"
    >
      <h1 className="font-bold text-(--color-neutral-950)">Projects</h1>
      <Link href="/projects/new">
        <Button variant="primary-dark" icon={<Plus size={20} />}>
          <span className="hidden sm:inline">New Project</span>
        </Button>
      </Link>
    </m.div>
  );
}
