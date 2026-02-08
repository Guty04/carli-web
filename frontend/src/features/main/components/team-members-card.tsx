import { Avatar } from "@/shared/components/avatar";
import { Card } from "@/shared/components/card";
import { StatusDot } from "@/shared/components/status-dot";
import type { GitLabMember } from "../schemas";
import { mapAccessLevelToRole } from "./team-members-card.utils";

export function TeamMembersCard({
  members,
}: Readonly<{ members: GitLabMember[] }>) {
  return (
    <Card className="flex flex-col gap-(--space-4)">
      <h3 className="font-semibold text-(--color-neutral-950)">Team Members</h3>

      {/* Mobile: card list */}
      <div className="flex flex-col gap-(--space-3) md:hidden">
        {members.map((member) => (
          <div
            key={member.id}
            className="flex items-center gap-(--space-3) border-b border-(--color-neutral-100) pb-(--space-3) last:border-0 last:pb-0"
          >
            <Avatar name={member.name || member.username} size={32} />
            <div className="min-w-0 flex-1">
              <p className="font-medium text-(--color-neutral-950)">
                {member.name || "\u2014"}
              </p>
              <p className="text-(--color-neutral-500)">
                @{member.username} &middot;{" "}
                {mapAccessLevelToRole(member.access_level)}
              </p>
            </div>
            <StatusDot
              color={member.state === "active" ? "success" : "error"}
            />
          </div>
        ))}
      </div>

      {/* Desktop: table */}
      <div className="hidden overflow-x-auto md:block">
        <table className="w-full">
          <thead>
            <tr className="border-b border-(--color-neutral-100)">
              <th className="pb-(--space-3) text-left font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
                Name
              </th>
              <th className="pb-(--space-3) text-left font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
                Username
              </th>
              <th className="pb-(--space-3) text-left font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
                Role
              </th>
              <th className="pb-(--space-3) text-left font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {members.map((member) => (
              <tr
                key={member.id}
                className="border-b border-(--color-neutral-100) last:border-0"
              >
                <td className="py-(--space-3) text-(--color-neutral-700)">
                  {member.name || "\u2014"}
                </td>
                <td className="py-(--space-3) text-(--color-neutral-500)">
                  @{member.username}
                </td>
                <td className="py-(--space-3) text-(--color-neutral-700)">
                  {mapAccessLevelToRole(member.access_level)}
                </td>
                <td className="py-(--space-3)">
                  <div className="flex items-center gap-(--space-2)">
                    <StatusDot
                      color={member.state === "active" ? "success" : "error"}
                    />
                    <span className="capitalize text-(--color-neutral-700)">
                      {member.state}
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
