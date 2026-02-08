import { Card } from "@/shared/components/card";
import { Skeleton } from "@/shared/components/skeleton";
import { KpiCardSkeleton } from "./kpi-card-skeleton";

export function DashboardSkeleton() {
  return (
    <div className="flex flex-col gap-(--space-6)">
      {/* Header skeleton */}
      <div>
        <Skeleton width="160px" height="30px" />
        <div className="mt-(--space-2)">
          <Skeleton width="240px" height="14px" />
        </div>
      </div>

      {/* KPI row */}
      <KpiCardSkeleton />

      {/* Bottom grid */}
      <div className="grid grid-cols-1 gap-(--space-4) lg:grid-cols-5">
        {/* Recent projects skeleton */}
        <Card className="lg:col-span-6">
          <div className="mb-(--space-4) flex items-center justify-between">
            <Skeleton width="140px" height="20px" />
            <Skeleton width="70px" height="14px" />
          </div>
          <div className="flex flex-col gap-(--space-3)">
            {Array.from({ length: 5 }).map((_, i) => (
              <div
                key={i}
                className="flex items-center justify-between py-(--space-2)"
              >
                <div className="flex items-center gap-(--space-3)">
                  <Skeleton
                    width="8px"
                    height="8px"
                    rounded="var(--radius-full)"
                  />
                  <div className="flex flex-col gap-(--space-1)">
                    <Skeleton width="140px" height="14px" />
                    <Skeleton width="90px" height="12px" />
                  </div>
                </div>
                <Skeleton
                  width="60px"
                  height="22px"
                  rounded="var(--radius-full)"
                />
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
