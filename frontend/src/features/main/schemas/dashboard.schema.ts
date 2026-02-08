import { z } from "zod";

export const stageBreakdownSchema = z.object({
  stage: z.enum(["development", "staging", "production"]),
  online: z.number(),
  total: z.number(),
});

export type StageBreakdown = z.infer<typeof stageBreakdownSchema>;

export const recentProjectSchema = z.object({
  id: z.string(),
  name: z.string(),
  created_at: z.string(),
  in_production: z.boolean(),
  quality_gate_status: z.enum(["OK", "WARN", "ERROR", "NONE"]),
});

export type RecentProject = z.infer<typeof recentProjectSchema>;

export const dashboardStatsSchema = z.object({
  total_projects: z.number(),
  in_production: z.number(),
  quality_gate_pass_rate: z.number(),
  total_members: z.number(),
  recent_projects: z.array(recentProjectSchema),
  stage_breakdown: z.array(stageBreakdownSchema),
});

export type DashboardStats = z.infer<typeof dashboardStatsSchema>;
