import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-(--color-neutral-50) p-(--space-4)">
      <h1 className="text-[72px] font-bold text-(--color-neutral-300)">
        404
      </h1>
      <h2 className="mt-(--space-2) text-(--text-heading) font-semibold text-(--color-neutral-950)">
        Page not found
      </h2>
      <p className="mt-(--space-2) text-(--text-body) text-(--color-neutral-500)">
        The page you are looking for does not exist.
      </p>
      <Link
        href="/projects"
        className="mt-(--space-6) inline-flex min-h-11 items-center justify-center rounded-(--radius-full) bg-(--color-brand-dark) px-6 py-2.5 text-(--text-body-medium) font-medium text-white transition-colors hover:bg-(--color-brand-dark-hover)"
      >
        Go to Projects
      </Link>
    </div>
  );
}
