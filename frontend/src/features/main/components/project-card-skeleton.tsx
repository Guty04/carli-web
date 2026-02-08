import { Card } from "@/shared/components/card";
import { Skeleton } from "@/shared/components/skeleton";

export function ProjectCardSkeleton() {
  return (
    <Card className="flex flex-col gap-(--space-3)">
      {/* Header: name + badge */}
      <div className="flex items-start justify-between gap-(--space-3)">
        <div className="min-w-0 flex-1 space-y-2">
          <Skeleton width="65%" height="18px" />
          <Skeleton width="80%" height="14px" />
        </div>
        <Skeleton width="72px" height="22px" />
      </div>

      {/* Stages */}
      <div className="flex flex-col gap-(--space-2)">
        <Skeleton width="90px" height="12px" />
        <div className="flex items-center gap-(--space-4)">
          <Skeleton width="48px" height="16px" />
          <Skeleton width="40px" height="16px" />
          <Skeleton width="48px" height="16px" />
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between border-t border-(--color-neutral-100) pt-(--space-3)">
        <div className="flex -space-x-2">
          <Skeleton width="28px" height="28px" className="rounded-full" />
          <Skeleton width="28px" height="28px" className="rounded-full" />
          <Skeleton width="28px" height="28px" className="rounded-full" />
        </div>
        <Skeleton width="100px" height="14px" />
      </div>
    </Card>
  );
}
