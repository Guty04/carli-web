"use client";

import { DashboardHeader } from "@/features/main/components/dashboard/dashboard-header";
import { DashboardSkeleton } from "@/features/main/components/dashboard/dashboard-skeleton";
import { KpiCards } from "@/features/main/components/dashboard/kpi-cards";
import { RecentProjects } from "@/features/main/components/dashboard/recent-projects";
import { useDashboardStats } from "@/features/main/hooks";

export default function DashboardPage() {
  const { data: stats, isLoading } = useDashboardStats();

  if (isLoading || !stats) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="flex flex-col gap-(--space-6)">
      <DashboardHeader />
      <KpiCards stats={stats} />

      <div className="grid grid-cols-1 gap-(--space-4) lg:grid-cols-5">
        <div className="lg:col-span-6">
          <RecentProjects projects={stats.recent_projects} />
        </div>
      </div>
    </div>
  );
}
