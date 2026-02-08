"use client";

import { Sidebar } from "@/features/main/components/sidebar";
import { AuthGuard } from "@/shared/components/auth-guard";
import { useState } from "react";

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <AuthGuard>
      <div className="flex min-h-screen">
        <Sidebar
          mobileOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
        <div className="flex flex-1 flex-col">
          {/* Mobile top bar — hamburger + branding */}
          <div className="flex h-14 items-center gap-(--space-2) border-b border-(--color-neutral-200) bg-white px-(--space-4) md:hidden">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-full p-2 text-(--color-neutral-700) hover:bg-(--color-neutral-100)"
              aria-label="Open menu"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
            </button>
            <div className="flex h-8 w-8 items-center justify-center rounded-(--radius-md) bg-(--color-brand-primary)">
              <span className="text-sm font-bold text-white">C</span>
            </div>
            <span className="text-(--text-subheading) font-semibold text-(--color-neutral-950)">
              Carli
            </span>
          </div>
          <main className="flex-1 px-(--space-4) py-(--space-4) md:px-(--space-6) lg:px-(--space-6) lg:py-(--space-8)">
            <div className="mx-auto max-w-[1440px]">{children}</div>
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}
