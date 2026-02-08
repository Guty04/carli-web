import { z } from "zod";

export const projectSummarySchema = z.object({
  id: z.string(),
  name: z.string(),
  url_repository: z.string(),
  created_at: z.string(),
});

export type ProjectSummary = z.infer<typeof projectSummarySchema>;

export const qualityGateConditionSchema = z.object({
  status: z.enum(["OK", "WARN", "ERROR"]),
  metric_key: z.string(),
  comparator: z.enum(["LT", "GT"]),
  error_threshold: z.string(),
  actual_value: z.string(),
});

export type QualityGateCondition = z.infer<typeof qualityGateConditionSchema>;

export const qualityGateSchema = z.object({
  status: z.enum(["OK", "WARN", "ERROR", "NONE"]),
  conditions: z.array(qualityGateConditionSchema),
});

export type QualityGate = z.infer<typeof qualityGateSchema>;

export const gitlabMemberSchema = z.object({
  id: z.number(),
  username: z.string(),
  name: z.string(),
  state: z.string(),
  access_level: z.number(),
});

export type GitLabMember = z.infer<typeof gitlabMemberSchema>;

export const stageStatusSchema = z.object({
  stage: z.enum(["development", "staging", "production"]),
  is_ready: z.boolean(),
});

export type StageStatus = z.infer<typeof stageStatusSchema>;

export const projectOverviewSchema = z.object({
  id: z.string(),
  name: z.string(),
  url_repository: z.string(),
  created_at: z.string(),
  quality_gate: qualityGateSchema.nullable().optional(),
  members: z
    .array(gitlabMemberSchema)
    .optional()
    .default([
      {
        id: 1,
        username: "Guty04",
        name: "Ezequiel",
        state: "active",
        access_level: 10,
      },
    ]),
  stages: z
    .array(stageStatusSchema)
    .optional()
    .default([
      { stage: "development", is_ready: false },
      { stage: "staging", is_ready: false },
      { stage: "production", is_ready: false },
    ]),
});

export type ProjectOverview = z.infer<typeof projectOverviewSchema>;

export const projectCreatedSchema = z.object({
  repo_url: z.string(),
  project_id: z.string(),
});

export type ProjectCreated = z.infer<typeof projectCreatedSchema>;
