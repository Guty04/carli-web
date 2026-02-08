import { Card } from "@/shared/components/card";
import { Skeleton } from "@/shared/components/skeleton";

export function ProjectOverviewSkeleton() {
  return (
    <div className="flex flex-col gap-(--space-6)">
      {/* Hero skeleton */}
      <Skeleton
        height="160px"
        rounded="0"
        className="w-full lg:rounded-b-(--radius-xl)!"
      />

      {/* Cards grid */}
      <div className="grid grid-cols-1 gap-(--space-4) lg:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <Card key={i} className="flex flex-col gap-(--space-3)">
            <Skeleton width="50%" height="20px" />
            <Skeleton width="100%" height="16px" />
            <Skeleton width="80%" height="16px" />
            <Skeleton width="60%" height="16px" />
          </Card>
        ))}
      </div>
    </div>
  );
}
