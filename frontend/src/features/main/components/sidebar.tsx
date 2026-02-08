"use client";

import { useLogout, useUser } from "@/features/auth/hooks";
import { Avatar } from "@/shared/components/avatar";
import { FolderKanban, LayoutDashboard, LogOut, Plus } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
  mobileOpen: boolean;
  onClose: () => void;
}

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/projects", label: "Projects", icon: FolderKanban },
  { href: "/projects/new", label: "New Project", icon: Plus },
];

export function Sidebar({ mobileOpen, onClose }: Readonly<SidebarProps>) {
  const pathname = usePathname();
  const logoutMutation = useLogout();
  const user = useUser();

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed top-0 left-0 z-50 flex h-full flex-col border-r border-(--color-neutral-200) bg-white transition-transform duration-200 md:static md:translate-x-0 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        } w-70 md:w-16 lg:w-60`}
      >
        {/* User info */}
        <div className="flex items-center gap-(--space-3) p-(--space-4) md:justify-center lg:justify-start">
          <Avatar name={user?.name ?? ""} size={32} />
          <div className="md:hidden lg:block">
            <p className="font-semibold text-(--color-neutral-950)">
              {user?.name ?? ""}
            </p>
            <p className="capitalize tracking-[0.05em] text-(--color-neutral-500)">
              {user?.role ?? ""}
            </p>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-(--space-2)">
          <ul className="flex flex-col gap-(--space-1)">
            {navItems.map((item) => {
              const isActive =
                pathname === item.href || pathname.startsWith(item.href + "/");
              const Icon = item.icon;
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    onClick={onClose}
                    className={`flex items-center gap-(--space-3) rounded-md px-(--space-3) py-(--space-3) text-(--text-body) transition-colors md:justify-center lg:justify-start ${
                      isActive
                        ? "bg-(--color-neutral-50) font-medium text-(--color-brand-primary)"
                        : "text-(--color-neutral-700) hover:bg-(--color-neutral-100)"
                    }`}
                  >
                    <Icon
                      size={20}
                      className={
                        isActive
                          ? "text-(--color-brand-primary)"
                          : "text-(--color-neutral-500)"
                      }
                    />
                    <span className="md:hidden lg:inline">{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Logout — bottom */}
        <div className="border-t border-(--color-neutral-200) p-(--space-2)">
          <button
            onClick={() => logoutMutation.mutate()}
            className="flex w-full items-center gap-(--space-3) rounded-md px-(--space-3) py-(--space-3) text-(--color-neutral-700) transition-colors hover:bg-(--color-error-light) hover:text-(--color-error) md:justify-center lg:justify-start"
          >
            <LogOut size={20} />
            <span className="md:hidden lg:inline">Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
