"use client";

import { ValidationError } from "@/api/errors";
import { useToast } from "@/shared/components/toast-provider";
import { useCallback, useState } from "react";
import { useCreateProject } from "../hooks";
import type { CreateProjectInput, ProjectCreated } from "../schemas";
import { CreateProjectError } from "./create-project-error";
import { CreateProjectForm } from "./create-project-form";
import { CreateProjectLoading } from "./create-project-loading";
import { CreateProjectSuccess } from "./create-project-success";

type ViewState = "idle" | "loading" | "success" | "error";

export function CreateProjectView() {
  const [viewState, setViewState] = useState<ViewState>("idle");
  const [result, setResult] = useState<ProjectCreated | null>(null);
  const [lastInput, setLastInput] = useState<CreateProjectInput | null>(null);
  const createMutation = useCreateProject();
  const { error: toastError } = useToast();

  const handleSubmit = useCallback(
    (data: CreateProjectInput) => {
      setLastInput(data);
      setViewState("loading");
      createMutation.mutate(data, {
        onSuccess: (res) => {
          setResult(res);
          setViewState("success");
        },
        onError: (err) => {
          setViewState("error");
          if (err instanceof ValidationError) {
            toastError("Please check your form inputs.");
            setViewState("idle");
          }
        },
      });
    },
    [createMutation, toastError],
  );

  const handleRetry = useCallback(() => {
    if (lastInput) {
      setViewState("idle");
    }
  }, [lastInput]);

  const handleCreateAnother = useCallback(() => {
    setResult(null);
    setLastInput(null);
    setViewState("idle");
  }, []);

  if (viewState === "loading") return <CreateProjectLoading />;

  if (viewState === "success" && result) {
    return (
      <CreateProjectSuccess
        result={result}
        onCreateAnother={handleCreateAnother}
      />
    );
  }

  if (viewState === "error") {
    return <CreateProjectError onRetry={handleRetry} />;
  }

  return (
    <CreateProjectForm
      onSubmit={handleSubmit}
      isPending={createMutation.isPending}
      defaultValues={lastInput ?? undefined}
    />
  );
}
