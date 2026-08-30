import { Outlet } from "react-router-dom";
import { TopNav } from "./TopNav";

export function AppShell() {
  return (
    <div className="min-h-screen px-0 py-0 sm:px-6 sm:py-8 lg:px-8 lg:py-12">
      <div className="glass-canvas mx-auto min-h-[calc(100vh-6rem)] max-w-[1220px] overflow-hidden rounded-none sm:rounded-[2rem]">
        <TopNav />
        <Outlet />
      </div>
    </div>
  );
}
