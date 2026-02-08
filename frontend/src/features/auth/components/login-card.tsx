"use client";

import * as m from "motion/react-client";
import { LoginForm } from "./login-form";

export function LoginCard({
  expiredMessage,
}: Readonly<{ expiredMessage?: boolean }>) {
  return (
    <m.div
      initial={{ opacity: 0, y: 20, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="w-full max-w-105 rounded-(--radius-xl) bg-white p-(--space-6) shadow-(--shadow-lg) md:p-(--space-8)"
    >
      <div className="mb-(--space-8) flex flex-col items-center gap-(--space-2)">
        <m.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{
            delay: 0.2,
            type: "spring",
            stiffness: 300,
            damping: 20,
          }}
          className="flex h-10 w-10 items-center justify-center rounded-md bg-(--color-brand-primary)"
        >
          <span className="text-lg font-bold text-white">C</span>
        </m.div>
        <h1 className="font-semibold text-(--color-neutral-950)">Carli</h1>
        <p className="text-(--color-neutral-500)">Sign in to your account</p>
      </div>

      {expiredMessage && (
        <m.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-(--space-4) text-center  text-(--color-error)"
        >
          Session expired. Please log in again.
        </m.p>
      )}

      <LoginForm />
    </m.div>
  );
}
