"use client"; // This is now a client component

import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Define auth routes where Sidebar should be hidden
  const authRoutes = ["/login", "/register", "/reset-password", "/forgot-password", "/verify"];
  const isAuthPage = authRoutes.includes(pathname);

  return !isAuthPage ? <Sidebar>{children}</Sidebar> : children;
}
