import { Card } from "@/shared/components/card";
import {
  FolderKanban,
  Rocket,
  ShieldCheck,
  Users,
  type LucideIcon,
} from "lucide-react";
import type { DashboardStats } from "../../schemas";

interface KpiCardProps {
  label: string;
  value: string | number;
  subtitle: string;
  icon: LucideIcon;
  iconColor: string;
  iconBg: string;
}

function KpiCard({
  label,
  value,
  subtitle,
  icon: Icon,
  iconColor,
  iconBg,
}: Readonly<KpiCardProps>) {
  return (
    <Card>
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-(--space-1)">
          <span className="font-medium text-(--color-neutral-500) text-[length:var(--text-small)]">
            {label}
          </span>
          <span className="font-bold text-(--color-neutral-950) text-[length:var(--text-display)]">
            {value}
          </span>
          <span className="text-(--color-neutral-500) text-[length:var(--text-small)]">
            {subtitle}
          </span>
        </div>
        <div
          className="flex h-10 w-10 items-center justify-center rounded-(--radius-lg)"
          style={{ backgroundColor: iconBg }}
        >
          <Icon size={20} style={{ color: iconColor }} />
        </div>
      </div>
    </Card>
  );
}

interface KpiCardsProps {
  stats: DashboardStats;
}

export function KpiCards({ stats }: Readonly<KpiCardsProps>) {
  return (
    <div className="grid grid-cols-1 gap-(--space-4) animate-[fade-in_0.4s_ease-out_0.1s_both] sm:grid-cols-2 lg:grid-cols-4">
      <KpiCard
        label="Total Projects"
        value={stats.total_projects}
        subtitle="Across all teams"
        icon={FolderKanban}
        iconColor="var(--color-brand-primary)"
        iconBg="var(--color-info-light)"
      />
      <KpiCard
        label="In Production"
        value={stats.in_production}
        subtitle={`${Math.round((stats.in_production / stats.total_projects) * 100)}% of total`}
        icon={Rocket}
        iconColor="var(--color-brand-accent)"
        iconBg="var(--color-brand-accent-light)"
      />
      <KpiCard
        label="Quality Gate Pass"
        value={`${stats.quality_gate_pass_rate}%`}
        subtitle="Projects passing QG"
        icon={ShieldCheck}
        iconColor="var(--color-success)"
        iconBg="var(--color-success-light)"
      />
      <KpiCard
        label="Team Members"
        value={stats.total_members}
        subtitle="Active contributors"
        icon={Users}
        iconColor="var(--color-warning)"
        iconBg="var(--color-warning-light)"
      />
    </div>
  );
}
