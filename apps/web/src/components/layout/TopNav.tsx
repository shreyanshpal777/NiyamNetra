import { ScanLine } from "lucide-react";
import { NavLink } from "react-router-dom";
import { cn } from "../../lib/utils";
import { Button } from "../ui/button";
import { MobileNav } from "./MobileNav";

const navItems = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Inspections", to: "/inspections" },
  { label: "Guidelines", to: "/dashboard#checks" },
];

export function TopNav() {
  return (
    <header className="flex items-center justify-between px-5 py-5 sm:px-8 lg:px-10">
      <NavLink className="flex items-center gap-2 text-sm font-semibold text-ink" to="/dashboard">
        <span className="flex size-7 items-center justify-center rounded-full bg-plum text-white">
          <ScanLine className="size-4" />
        </span>
        Inspector AI
      </NavLink>

      <nav className="hidden items-center gap-8 text-xs font-medium text-muted md:flex">
        {navItems.map((item) => (
          <NavLink
            className={({ isActive }) =>
              cn("transition-colors hover:text-ink", isActive && "text-ink")
            }
            key={item.label}
            to={item.to}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="hidden md:block">
        <Button asChild size="sm">
          <NavLink to="/inspection/new">New Inspection</NavLink>
        </Button>
      </div>
      <MobileNav />
    </header>
  );
}
