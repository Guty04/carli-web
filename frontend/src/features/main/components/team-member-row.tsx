"use client";

import { Input } from "@/shared/components/input";
import { Select } from "@/shared/components/select";
import { Trash2 } from "lucide-react";
import type { FieldErrors, UseFormRegister } from "react-hook-form";
import type { CreateProjectInput } from "../schemas";

interface TeamMemberRowProps {
  index: number;
  register: UseFormRegister<CreateProjectInput>;
  errors: FieldErrors<CreateProjectInput>;
  onRemove: () => void;
}

const roleOptions = [
  { value: "developer", label: "Developer" },
  { value: "maintainer", label: "Maintainer" },
  { value: "reporter", label: "Reporter" },
];

export function TeamMemberRow({
  index,
  register,
  errors,
  onRemove,
}: Readonly<TeamMemberRowProps>) {
  return (
    <div className="flex items-start gap-(--space-3)">
      <div className="flex-1">
        <Input
          placeholder="GitLab username"
          error={errors.members?.[index]?.gitlab_user_name?.message}
          {...register(`members.${index}.gitlab_user_name`)}
        />
      </div>
      <div className="w-35">
        <Select options={roleOptions} {...register(`members.${index}.role`)} />
      </div>
      <button
        type="button"
        onClick={onRemove}
        className="mt-2.5 shrink-0 rounded-full p-2 text-(--color-neutral-500) hover:bg-(--color-error-light) hover:text-(--color-error)"
        aria-label="Remove member"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}
