import { PROJECTS, PROJECT_DETAIL } from "@/api/endpoints";
import { get, post } from "@/api/http";
import { z } from "zod";
import {
  projectCreatedSchema,
  projectOverviewSchema,
  type CreateProjectInput,
  type ProjectCreated,
  type ProjectOverview,
} from "../schemas";

export async function listProjects(): Promise<ProjectOverview[]> {
  const data = await get<unknown>(PROJECTS);
  return z.array(projectOverviewSchema).parse(data);
}

export async function getProject(id: string): Promise<ProjectOverview> {
  const data = await get<unknown>(PROJECT_DETAIL(id));
  return projectOverviewSchema.parse(data);
}

export async function createProject(
  input: CreateProjectInput,
): Promise<ProjectCreated> {
  const data = await post<unknown>(PROJECTS, input);
  return projectCreatedSchema.parse(data);
}
