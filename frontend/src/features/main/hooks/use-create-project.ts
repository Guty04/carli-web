"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { CreateProjectInput } from "../schemas";
import { createProject } from "../services/project.service";

export function useCreateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateProjectInput) => createProject(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}
