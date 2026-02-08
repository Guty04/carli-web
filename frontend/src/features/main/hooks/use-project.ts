"use client";

import { useQuery } from "@tanstack/react-query";
import { getProject } from "../services/project.service";

export function useProject(id: string) {
  return useQuery({
    queryKey: ["projects", id],
    queryFn: () => getProject(id),
    enabled: !!id,
  });
}
