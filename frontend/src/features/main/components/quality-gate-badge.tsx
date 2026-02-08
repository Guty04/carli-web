import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  type LucideIcon,
} from "lucide-react";

type QualityGateStatus = "OK" | "WARN" | "ERROR" | "NONE";

const config: Record<
  QualityGateStatus,
  { label: string; icon: LucideIcon; classes: string }
> = {
  OK: {
    label: "Passed",
    icon: CheckCircle2,
    classes:
      "bg-(--color-success-light) text-[#15803D] border-(--color-success)",
  },
  WARN: {
    label: "Warning",
    icon: AlertTriangle,
    classes:
      "bg-(--color-warning-light) text-[#92400E] border-(--color-warning)",
  },
  ERROR: {
    label: "Failed",
    icon: XCircle,
    classes: "bg-(--color-error-light) text-[#B91C1C] border-(--color-error)",
  },
  NONE: {
    label: "Not Set",
    icon: HelpCircle,
    classes:
      "bg-(--color-neutral-100) text-(--color-neutral-500) border-(--color-neutral-300)",
  },
};

export function QualityGateBadge({
  status,
}: Readonly<{ status: QualityGateStatus }>) {
  const { label, icon: Icon, classes } = config[status];

  return (
    <span
      className={`inline-flex items-center gap-(--space-1) rounded-(--radius-sm) border px-2 py-0.5 text-(--text-small) font-medium ${classes}`}
    >
      <Icon size={12} />
      {label}
    </span>
  );
}
