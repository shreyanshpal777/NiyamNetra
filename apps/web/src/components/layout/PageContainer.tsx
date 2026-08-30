import type { PropsWithChildren } from "react";
import { cn } from "../../lib/utils";

interface PageContainerProps extends PropsWithChildren {
  className?: string;
}

export function PageContainer({ children, className }: PageContainerProps) {
  return <main className={cn("px-5 pb-10 sm:px-8 lg:px-10", className)}>{children}</main>;
}
