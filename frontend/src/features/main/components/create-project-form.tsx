"use client";

import { Button } from "@/shared/components/button";
import { Input } from "@/shared/components/input";
import { Select } from "@/shared/components/select";
import { Textarea } from "@/shared/components/textarea";
import { zodResolver } from "@hookform/resolvers/zod";
import { PlusCircle } from "lucide-react";
import { useFieldArray, useForm } from "react-hook-form";
import { createProjectSchema, type CreateProjectInput } from "../schemas";
import { TeamMemberRow } from "./team-member-row";

interface CreateProjectFormProps {
  onSubmit: (data: CreateProjectInput) => void;
  isPending: boolean;
  defaultValues?: Partial<CreateProjectInput>;
}

const projectTypeOptions = [
  { value: "backend", label: "Backend" },
  { value: "frontend", label: "Frontend" },
];

export function CreateProjectForm({
  onSubmit,
  isPending,
  defaultValues,
}: Readonly<CreateProjectFormProps>) {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<CreateProjectInput>({
    resolver: zodResolver(createProjectSchema),
    defaultValues: {
      name: "",
      description: "",
      project_type: undefined,
      members: [],
      ...defaultValues,
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "members",
  });

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex max-w-160 flex-col gap-(--space-6)"
    >
      <Input
        label="Project Name"
        placeholder="my-project"
        error={errors.name?.message}
        {...register("name")}
      />

      <Textarea
        label="Description"
        placeholder="Brief project description (optional)"
        helperText="Max 500 characters"
        error={errors.description?.message}
        {...register("description")}
      />

      <Select
        label="Project Type"
        placeholder="Select type..."
        options={projectTypeOptions}
        error={errors.project_type?.message}
        {...register("project_type")}
      />

      <div className="flex flex-col gap-(--space-3)">
        <p className="font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
          Team Members
        </p>

        {fields.map((field, index) => (
          <TeamMemberRow
            key={field.id}
            index={index}
            register={register}
            errors={errors}
            onRemove={() => remove(index)}
          />
        ))}

        <button
          type="button"
          onClick={() => append({ gitlab_user_name: "", role: "developer" })}
          className="flex items-center gap-(--space-2) self-start text-(--color-brand-accent) hover:text-(--color-brand-accent-hover)"
        >
          <PlusCircle size={16} />
          Add Member
        </button>
      </div>

      <Button type="submit" variant="primary-dark" loading={isPending}>
        Create Project
      </Button>
    </form>
  );
}
