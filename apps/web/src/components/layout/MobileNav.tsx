import { Menu } from "lucide-react";
import { NavLink } from "react-router-dom";
import { Button } from "../ui/button";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "../ui/sheet";

const navItems = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Inspections", to: "/inspections" },
  { label: "Guidelines", to: "/dashboard#checks" },
];

export function MobileNav() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button aria-label="Open navigation" className="md:hidden" size="icon" variant="ghost">
          <Menu className="size-5" />
        </Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Inspector AI</SheetTitle>
        </SheetHeader>
        <nav className="grid gap-2 pt-4">
          {navItems.map((item) => (
            <SheetClose asChild key={item.label}>
              <NavLink
                className="rounded-2xl px-4 py-3 text-sm font-medium text-ink transition-colors hover:bg-lavender"
                to={item.to}
              >
                {item.label}
              </NavLink>
            </SheetClose>
          ))}
          <SheetClose asChild>
            <Button asChild className="mt-3">
              <NavLink to="/inspection/new">New Inspection</NavLink>
            </Button>
          </SheetClose>
        </nav>
      </SheetContent>
    </Sheet>
  );
}
