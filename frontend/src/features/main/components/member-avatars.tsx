import { Avatar } from "@/shared/components/avatar";
import type { GitLabMember } from "../schemas";

const MAX_VISIBLE = 3;

export function MemberAvatars({
  members,
}: Readonly<{ members: GitLabMember[] }>) {
  const visible = members.slice(0, MAX_VISIBLE);
  const remaining = members.length - MAX_VISIBLE;

  return (
    <div className="flex items-center -space-x-2">
      {visible.map((member) => (
        <Avatar
          key={member.id}
          name={member.name}
          size={28}
          className="border-2 border-white"
        />
      ))}
      {remaining > 0 && (
        <div
          className="inline-flex shrink-0 items-center justify-center rounded-full border-2 border-white bg-(--color-neutral-100) text-(--color-neutral-700)"
          style={{ width: 28, height: 28, fontSize: 11 }}
          title={members
            .slice(MAX_VISIBLE)
            .map((m) => m.name)
            .join(", ")}
        >
          +{remaining}
        </div>
      )}
    </div>
  );
}
