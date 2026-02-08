"use client";

import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react";
import { Toast, type ToastVariant } from "./toast";

interface ToastItem {
  id: number;
  message: string;
  title?: string;
  variant: ToastVariant;
}

interface ToastContextValue {
  toast: (opts: {
    message: string;
    title?: string;
    variant?: ToastVariant;
  }) => void;
  success: (message: string, title?: string) => void;
  error: (message: string, title?: string) => void;
  warning: (message: string, title?: string) => void;
  info: (message: string, title?: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

let nextId = 0;

export function ToastProvider({ children }: Readonly<{ children: ReactNode }>) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const addToast = useCallback(
    ({
      message,
      title,
      variant = "info",
    }: {
      message: string;
      title?: string;
      variant?: ToastVariant;
    }) => {
      const id = nextId++;
      setToasts((prev) => [...prev, { id, message, title, variant }]);
    },
    [],
  );

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const value: ToastContextValue = {
    toast: addToast,
    success: (message, title) =>
      addToast({ message, title, variant: "success" }),
    error: (message, title) => addToast({ message, title, variant: "error" }),
    warning: (message, title) =>
      addToast({ message, title, variant: "warning" }),
    info: (message, title) => addToast({ message, title, variant: "info" }),
  };

  return (
    <ToastContext value={value}>
      {children}
      <div className="fixed bottom-(--space-4) left-1/2 z-50 flex -translate-x-1/2 flex-col gap-(--space-2)">
        {toasts.map((t) => (
          <Toast
            key={t.id}
            variant={t.variant}
            title={t.title}
            message={t.message}
            onClose={() => removeToast(t.id)}
          />
        ))}
      </div>
    </ToastContext>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}
