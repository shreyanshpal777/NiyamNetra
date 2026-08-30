import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  variant?: "light" | "dark";
  className?: string;
}

export function FeatureCard({
  title,
  description,
  icon,
  variant = "light",
  className,
}: FeatureCardProps) {
  const dark = variant === "dark";
  return (
    <article
      className={cn(
        "min-h-56 rounded-3xl p-6 sm:p-7",
        dark ? "bg-plum text-white" : "bg-lavender text-ink",
        className,
      )}
    >
      <div
        className={cn(
          "mb-12 flex size-10 items-center justify-center rounded-full",
          dark ? "bg-white/12 text-white" : "bg-white text-plum",
        )}
      >
        {icon}
      </div>
      <h3 className="text-2xl font-semibold leading-tight">{title}</h3>
      <p className={cn("mt-4 max-w-xs text-sm leading-6", dark ? "text-white/70" : "text-muted")}>
        {description}
      </p>
    </article>
  );
}
