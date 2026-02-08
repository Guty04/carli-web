import Link from "next/link";
import { ShieldX } from "lucide-react";

export default function ForbiddenPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <ShieldX size={64} className="text-(--color-error)" />
      <h1 className="mt-(--space-4) text-(--text-display) font-bold text-(--color-neutral-950)">
        403 — Access Denied
      </h1>
      <p className="mt-(--space-2) text-(--text-body) text-(--color-neutral-500)">
        You do not have permission to access this page.
      </p>
      <Link
        href="/projects"
        className="mt-(--space-6) inline-flex min-h-11 items-center justify-center rounded-(--radius-full) bg-(--color-brand-dark) px-6 py-2.5 text-(--text-body-medium) font-medium text-white transition-colors hover:bg-(--color-brand-dark-hover)"
      >
        Go to Projects
      </Link>
    </div>
  );
}
