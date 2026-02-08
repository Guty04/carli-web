import { Loader2 } from "lucide-react";

export function CreateProjectLoading() {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-white/90">
      <Loader2 size={48} className="animate-spin text-(--color-brand-accent)" />
      <p className="mt-(--space-4) font-semibold text-(--color-neutral-950)">
        Setting up your project...
      </p>
      <p className="mt-(--space-2) text-(--color-neutral-500)">
        This may take up to 30 seconds.
      </p>
    </div>
  );
}
