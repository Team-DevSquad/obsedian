'use client';
import React, { useState } from 'react';
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Bell,
  ChevronDown,
  ChevronRight,
  BugIcon,
  CircleUser,
  ClipboardMinus,
  CodeSquare,
  FileText,
  Home,
  Menu,
  ShieldAlert,
  ShieldCheck,
  CrossIcon,
  Settings2Icon,
  ShieldEllipsisIcon,
  AlertCircleIcon,
  UserCircleIcon
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ModeToggle } from "@/components/ui/mode-toggle";
import AdminSearch from "@/components/features/admin-search";
import AnalysisPage from '@/app/analysis/page';
import withAuth from '@/utils/withAuth';
import NotificationsPopover from './NotificationsPopover';


export default withAuth(function Sidebar({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState(pathname);
  const [isAnalysisOpen, setIsAnalysisOpen] = useState(false);

  const handleTabClick = (tab: string) => {
    setActiveTab(tab);
  };
  const handleLogout = () => {
    // Clear localStorage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userEmail');

    // Redirect to login page
    router.push('/login');
  };
  const ProfileMenuItem = ({ icon: Icon, children, onClick }: {
    icon: React.ElementType;
    children: React.ReactNode;
    onClick?: () => void;
  }) => (
    <DropdownMenuItem
      onClick={onClick}
      className="flex items-center gap-2 cursor-pointer text-sm px-4 py-2 hover:bg-primary/10 dark:hover:bg-primary/20"
    >
      <Icon className="h-4 w-4" />
      {children}
    </DropdownMenuItem>
  );
  const NavLink = ({ href, icon: Icon, children }: { href: string; icon: React.ElementType; children: React.ReactNode }) => {
    const isActive = activeTab === href;
    return (
      <Link
        href={href}
        onClick={() => handleTabClick(href)}
        className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all hover:bg-primary/10 active:bg-primary/15 ${isActive
          ? 'bg-primary/15 text-primary dark:bg-primary/25 dark:text-primary-foreground'
          : 'text-muted-foreground hover:text-primary'
          }`}
      >
        <Icon className={`h-4 w-4 transition-colors ${isActive ? 'text-primary dark:text-primary-foreground' : 'text-muted-foreground group-hover:text-primary'
          }`} />
        {children}
      </Link>
    );
  };

  return (
    <div className="flex min-h-screen w-full">
      {/* Fixed Sidebar */}
      <div className="fixed hidden h-screen w-[240px] lg:w-[280px] border-r bg-card dark:bg-card/95 md:block">
        <div className="flex h-full flex-col">
          {/* Header - Fixed */}
          <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
            <Link href="/" className="flex items-center gap-2 font-semibold">
              <ShieldCheck className="h-6 w-6 text-primary" />
              <span className="text-lg font-bold tracking-tight">Obsedian</span>
            </Link>
            <Button variant="ghost" size="icon" className="ml-auto h-8 w-8 rounded-full">
              <NotificationsPopover />
            </Button>
          </div>

          {/* Navigation - Scrollable */}
          <div className="flex flex-col flex-grow overflow-y-auto">
            <nav className="grid items-start px-2 text-sm font-medium lg:px-4 py-2">
              <NavLink href="/" icon={Home}>Dashboard</NavLink>

              <div className="relative">
                <button
                  onClick={() => setIsAnalysisOpen(!isAnalysisOpen)}
                  className={`group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all hover:bg-primary/10 ${activeTab.includes('analysis') ? 'text-primary' : 'text-muted-foreground hover:text-primary'
                    }`}
                >
                  <FileText className="h-4 w-4" />
                  <span>Analysis</span>
                  {isAnalysisOpen ? (
                    <ChevronDown className="ml-auto h-4 w-4" />
                  ) : (
                    <ChevronRight className="ml-auto h-4 w-4" />
                  )}
                </button>
                {isAnalysisOpen && (
                  <div className="ml-4 mt-1 grid gap-1 pl-4 border-l">
                    {/* give option for create analysis */}
                    <NavLink href="/analysis" icon={CrossIcon}>
                      Create Analysis
                    </NavLink>

                    <NavLink href="/dynamic-analysis" icon={BugIcon}>
                      Dynamic Analysis
                    </NavLink>
                    <NavLink href="/static-analysis" icon={CodeSquare}>
                      Static Analysis
                    </NavLink>
                  </div>
                )}
              </div>

              <NavLink href="/vulnerability" icon={ShieldAlert}>
                Vulnerabilities
              </NavLink>
              <NavLink href="/reports" icon={ClipboardMinus}>
                Reports
              </NavLink>
              <NavLink href="/security-policies" icon={ShieldEllipsisIcon}>
                Security Policies
              </NavLink>
              <NavLink href="/access-control" icon={UserCircleIcon}>
                User Access Control
              </NavLink>
              <NavLink href="/sercurity-alerts" icon={AlertCircleIcon}>
                Security Alerts
              </NavLink>
              <NavLink href="/settings" icon={Settings2Icon}>
                Settings
              </NavLink>

            </nav>

            {/* Upgrade Card - Fixed at bottom */}
            <div className="mt-auto flex flex-col items-center">
              <Card className="bg-background/90 border border-border shadow-lg backdrop-blur-md rounded-2xl">
                <CardHeader className="p-6 pb-3">
                  <CardTitle className="text-lg font-semibold text-primary">🚀 Developed by DevSquad</CardTitle>
                  <CardDescription className="text-sm text-muted-foreground">
                    This application is in <strong>BETA</strong> and not available for public use.
                  </CardDescription>
                </CardHeader>
                <CardFooter className="p-4 pt-2 flex w-full">
                  <Button
                    size="sm"
                    className="w-full transition-all duration-300 
          bg-green-500 text-black dark:bg-neon-green-400 dark:text-white 
          hover:bg-green-600 dark:hover:bg-neon-green-500"
                  >
                    Learn More
                  </Button>
                </CardFooter>
              </Card>
            </div>


          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 flex-col md:ml-[240px] lg:ml-[280px]">
        {/* Fixed Header */}
        <header className="sticky top-0 z-10 flex h-14 items-center gap-4 border-b bg-card/50 px-4 backdrop-blur-sm lg:h-[60px] lg:px-6">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="shrink-0 md:hidden">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle navigation menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-72">
              <div className="flex h-full flex-col">
                <div className="flex items-center gap-2 py-4">
                  <ShieldCheck className="h-6 w-6 text-primary" />
                  <span className="text-lg font-bold">Obsedian</span>
                </div>
                <nav className="grid gap-2 text-sm">
                  <NavLink href="/" icon={Home}>Dashboard</NavLink>
                  <NavLink href="/analysis" icon={CrossIcon}>
                    Create Analysis
                  </NavLink>
                  <NavLink href="/dynamic-analysis" icon={BugIcon}>
                    Dynamic Analysis
                  </NavLink>
                  <NavLink href="/static-analysis" icon={CodeSquare}>
                    Static Analysis
                  </NavLink>
                  <NavLink href="/vulnerability" icon={ShieldAlert}>
                    Vulnerabilities
                  </NavLink>
                  <NavLink href="/reports" icon={ClipboardMinus}>
                    Reports
                  </NavLink>

                  <NavLink href="/security-policies" icon={ShieldEllipsisIcon}>
                    Security Policies
                  </NavLink>
                  <NavLink href="/access-control" icon={UserCircleIcon}>
                    User Access Control
                  </NavLink>
                  <NavLink href="/security-alerts" icon={AlertCircleIcon}>
                    Security Alerts
                  </NavLink>
                  <NavLink href="/settings" icon={Settings2Icon}>
                    Settings
                  </NavLink>
                </nav>
                <div className="mt-auto flex flex-col items-center">
                  <Card className="bg-background/90 border border-border shadow-lg backdrop-blur-md rounded-2xl">
                    <CardHeader className="p-6 pb-3">
                      <CardTitle className="text-lg font-semibold text-primary">🚀 Developed by DevSquad</CardTitle>
                      <CardDescription className="text-sm text-muted-foreground">
                        This application is in <strong>BETA</strong> and not available for public use.
                      </CardDescription>
                    </CardHeader>
                    <CardFooter className="p-4 pt-2 flex w-full">
                      <Button
                        size="sm"
                        className="w-full transition-all duration-300 
          bg-green-500 text-black dark:bg-neon-green-400 dark:text-white 
          hover:bg-green-600 dark:hover:bg-neon-green-500"
                      >
                        Learn More
                      </Button>
                    </CardFooter>
                  </Card>
                </div>


              </div>
            </SheetContent>
          </Sheet>

          <div className="w-full flex-1">
            <AdminSearch />
          </div>
          <ModeToggle />
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full">
                <CircleUser className="h-5 w-5" />
                <span className="sr-only">Toggle user menu</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {/* on My Account click go to the /account page */}
              <DropdownMenuLabel onClick={() => router.push('/account')}>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => router.push('/settings')}>Settings</DropdownMenuItem>
              <DropdownMenuItem onClick={() => router.push('/support')} >Support</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-500 dark:text-red-400" onClick={handleLogout}>Logout</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </header>

        {/* Scrollable Main Content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  );
});