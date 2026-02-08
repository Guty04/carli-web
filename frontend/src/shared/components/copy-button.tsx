"use client";

import { useCopyToClipboard } from "@/hooks/use-copy-to-clipboard";
import { Check, Copy } from "lucide-react";

interface CopyButtonProps {
  text: string;
  className?: string;
}

export function CopyButton({
  text,
  className = "",
}: Readonly<CopyButtonProps>) {
  const { copied, copy } = useCopyToClipboard();

  return (
    <button
      type="button"
      onClick={() => copy(text)}
      className={`inline-flex items-center justify-center rounded-full p-1 transition-colors hover:bg-(--color-neutral-100) ${className}`}
      aria-label={copied ? "Copied" : "Copy to clipboard"}
      title={copied ? "Copied!" : "Copy"}
    >
      {copied ? (
        <Check size={16} className="text-(--color-brand-accent)" />
      ) : (
        <Copy size={16} className="text-(--color-neutral-500)" />
      )}
    </button>
  );
}
