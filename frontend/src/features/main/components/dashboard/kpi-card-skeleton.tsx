import { Card } from "@/shared/components/card";
import { Skeleton } from "@/shared/components/skeleton";

export function KpiCardSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-(--space-4) sm:grid-cols-2 lg:grid-cols-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i}>
          <div className="flex flex-col gap-(--space-3)">
            <Skeleton width="120px" height="14px" />
            <Skeleton width="60px" height="32px" />
            <Skeleton width="90px" height="12px" />
          </div>
        </Card>
      ))}
    </div>
  );
}
