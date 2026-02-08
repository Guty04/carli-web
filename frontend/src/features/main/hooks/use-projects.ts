"use client";

import { useQuery } from "@tanstack/react-query";
import { listProjects } from "../services/project.service";

export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: listProjects,
  });
}
