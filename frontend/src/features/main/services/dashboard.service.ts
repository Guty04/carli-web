import type { DashboardStats } from "../schemas";

const MOCK_DASHBOARD_STATS: DashboardStats = {
  total_projects: 12,
  in_production: 8,
  quality_gate_pass_rate: 75,
  total_members: 34,
  recent_projects: [
    {
      id: "1",
      name: "carli-web",
      created_at: "2025-12-15T10:30:00Z",
      in_production: true,
      quality_gate_status: "OK",
    },
    {
      id: "2",
      name: "payment-gateway",
      created_at: "2025-12-10T14:00:00Z",
      in_production: true,
      quality_gate_status: "WARN",
    },
    {
      id: "3",
      name: "auth-service",
      created_at: "2025-12-08T09:15:00Z",
      in_production: true,
      quality_gate_status: "OK",
    },
    {
      id: "4",
      name: "notification-hub",
      created_at: "2025-12-05T16:45:00Z",
      in_production: false,
      quality_gate_status: "ERROR",
    },
    {
      id: "5",
      name: "analytics-dashboard",
      created_at: "2025-12-01T11:20:00Z",
      in_production: false,
      quality_gate_status: "NONE",
    },
  ],
  stage_breakdown: [
    { stage: "development", online: 10, total: 12 },
    { stage: "staging", online: 7, total: 12 },
    { stage: "production", online: 8, total: 12 },
  ],
};

export async function getDashboardStats(): Promise<DashboardStats> {
  await new Promise((resolve) => setTimeout(resolve, 800));
  return MOCK_DASHBOARD_STATS;
}
