"use client";

import { StatusBadge } from "@/shared/components/badge";
import { Card } from "@/shared/components/card";
import { AlertTriangle, ShieldCheck, ShieldX } from "lucide-react";
import type { QualityGate } from "../schemas";
import { formatThreshold, humanizeMetricKey } from "./quality-gate-card.utils";

function StatusIcon({ status }: Readonly<{ status: string }>) {
  if (status === "OK")
    return <ShieldCheck size={18} className="text-(--color-success)" />;
  if (status === "WARN")
    return <AlertTriangle size={18} className="text-(--color-warning)" />;
  return <ShieldX size={18} className="text-(--color-error)" />;
}

function getVariant(status: string) {
  if (status === "OK") return "success" as const;
  if (status === "WARN") return "warning" as const;
  return "error" as const;
}

export function QualityGateCard({
  qualityGate,
}: Readonly<{ qualityGate: QualityGate }>) {
  return (
    <Card className="flex flex-col gap-(--space-4)">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-(--color-neutral-950)">
          Quality Gate
        </h3>
        <StatusBadge variant={getVariant(qualityGate.status)}>
          {qualityGate.status === "OK"
            ? "Passed"
            : qualityGate.status === "WARN"
              ? "Warning"
              : "Failed"}
        </StatusBadge>
      </div>

      <div className="flex flex-col gap-(--space-3)">
        {qualityGate.conditions.map((condition) => (
          <div
            key={condition.metric_key}
            className="flex items-center justify-between gap-(--space-3) border-b border-(--color-neutral-100) pb-(--space-3) last:border-0 last:pb-0"
          >
            <div className="flex items-center gap-(--space-2)">
              <StatusIcon status={condition.status} />
              <span className="text-(--color-neutral-700)">
                {humanizeMetricKey(condition.metric_key)}
              </span>
            </div>
            <div className="flex items-center gap-(--space-3) text-right">
              <span className="font-semibold text-(--color-neutral-950)">
                {condition.actual_value}%
              </span>
              <span className="text-(--color-neutral-500)">
                {formatThreshold(
                  condition.comparator,
                  condition.error_threshold,
                )}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
