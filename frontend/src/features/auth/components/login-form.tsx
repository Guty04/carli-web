"use client";

import { ApiError } from "@/api/errors";
import { zodResolver } from "@hookform/resolvers/zod";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useLogin } from "../hooks";
import { loginSchema, type LoginInput } from "../schemas";

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  });

  const [showPassword, setShowPassword] = useState(false);
  const loginMutation = useLogin();

  const onSubmit = (data: LoginInput) => {
    loginMutation.mutate(data);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col gap-(--space-5)"
    >
      <div className="flex flex-col gap-(--space-2)">
        <label
          htmlFor="email"
          className="font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)"
        >
          Email
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          placeholder="your@email.com"
          className={`h-11 rounded-md border px-(--space-4) text-(--color-neutral-950) placeholder:text-(--color-neutral-500) focus:outline-none focus:ring-[3px] ${
            errors.email
              ? "border-(--color-error) focus:ring-error/15"
              : "border-(--color-neutral-200) focus:border-(--color-brand-accent) focus:ring-(--color-brand-accent)/15"
          }`}
          {...register("email")}
        />
        {errors.email && (
          <p className=" text-(--color-error)">{errors.email.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-(--space-2)">
        <label
          htmlFor="password"
          className="font-bold uppercase tracking-[0.05em] text-(--color-neutral-500)"
        >
          Password
        </label>
        <div className="relative">
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            placeholder="********"
            className={`h-11 w-full rounded-md border px-(--space-4) pr-(--space-11) text-(--color-neutral-950) placeholder:text-(--color-neutral-500) focus:outline-none focus:ring-[3px] ${
              errors.password
                ? "border-(--color-error) focus:ring-error/15"
                : "border-(--color-neutral-200) focus:border-(--color-brand-accent) focus:ring-(--color-brand-accent)/15"
            }`}
            {...register("password")}
          />
          <button
            type="button"
            onClick={() => setShowPassword((prev) => !prev)}
            className="absolute inset-y-0 right-0 flex items-center px-(--space-3) text-(--color-neutral-500) hover:text-(--color-neutral-700)"
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
        {errors.password && (
          <p className=" text-(--color-error)">{errors.password.message}</p>
        )}
      </div>

      {loginMutation.isError && (
        <p className="text-center  text-(--color-error)">
          {loginMutation.error instanceof ApiError &&
          loginMutation.error.status === 401
            ? loginMutation.error.message
            : "An error occurred. Please try again."}
        </p>
      )}

      <button
        type="submit"
        disabled={loginMutation.isPending}
        className="flex h-11 items-center justify-center gap-(--space-2) rounded-md bg-(--color-brand-dark) font-medium text-white transition-colors hover:bg-(--color-brand-dark-hover) disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loginMutation.isPending ? (
          <Loader2 size={20} className="animate-spin" />
        ) : (
          "Log in"
        )}
      </button>
    </form>
  );
}
