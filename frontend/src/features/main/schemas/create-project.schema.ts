import { z } from "zod";

export const createProjectSchema = z.object({
  name: z
    .string()
    .min(1, "Project name is required")
    .regex(
      /^[a-zA-Z0-9-\s]+$/,
      "Only alphanumeric characters, hyphens, and spaces are allowed",
    ),
  description: z.string().max(500, "Max 500 characters"),
  project_type: z.enum(["backend", "frontend"], {
    message: "Project type is required",
  }),
  members: z.array(
    z.object({
      gitlab_user_name: z.string().min(1, "Username is required"),
      role: z.enum(["developer", "maintainer", "reporter"]),
    }),
  ),
});

export type CreateProjectInput = z.infer<typeof createProjectSchema>;
