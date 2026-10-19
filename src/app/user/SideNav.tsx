"use client";

import ThemeToggler from "@/Components/Header/ThemeToggler";
import SurveillanceChatbot from "@/Components/Chatbot";
import { SideNavItem } from "@/types/types";
import { SIDENAV_ITEMS } from "./constant";
import {
  AlignJustify,
  ChevronDown,
  ChevronRight,
  ShieldAlert,
  User,
  Settings,
  LogOut,
  HelpCircle,
  Film,
  Camera,
} from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import Image from "next/image";

const SideNav = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<{
    name?: string;
    email?: string;
    id?: string;
    _id?: string;
  }>({
    name: "",
    email: "",
  });

  useEffect(() => {
    try {
      const stored = localStorage.getItem("user");
      if (stored) {
        setUser(JSON.parse(stored));
      }
    } catch {
      // ignore
    }
  }, []);

  const router = useRouter();

  const handleLogout = () => {
    try {
      localStorage.removeItem("user");
      sessionStorage.clear();
    } catch {
      // ignore
    }
    router.push("/");
  };

  const pathname = usePathname();
  const pathSegments = pathname.split("/").filter(Boolean);

  return (
    <>
      <div className="drawer lg:drawer-open min-h-screen bg-base-100">
        <input id="my-drawer-3" type="checkbox" className="drawer-toggle" />
        <div className="drawer-content flex flex-col min-h-screen">
          {/* Top Navbar */}
          <header className="navbar justify-between bg-base-200/80 backdrop-blur-md border-b border-base-300 w-full px-4 lg:px-8 h-16 sticky top-0 z-30">
            {/* Breadcrumb Links */}
            <div className="lg:flex items-center space-x-2 hidden text-xs font-medium text-base-content/70">
              <Link href="/user/dashboard" className="hover:text-primary transition font-semibold">
                Home
              </Link>
              {pathSegments.map((segment, index) => (
                <React.Fragment key={index}>
                  <ChevronRight className="w-3.5 h-3.5 text-base-content/40" />
                  <Link href={`/${pathSegments.slice(0, index + 1).join("/")}`}>
                    <span
                      className={`capitalize transition ${
                        index === pathSegments.length - 1
                          ? "text-primary font-bold"
                          : "hover:text-primary"
                      }`}
                    >
                      {segment.replace(/-/g, " ")}
                    </span>
                  </Link>
                </React.Fragment>
              ))}
            </div>

            {/* Mobile Sidebar Toggle Button */}
            <div className="flex-none lg:hidden">
              <label
                htmlFor="my-drawer-3"
                aria-label="open sidebar"
                className="btn btn-square btn-ghost btn-sm"
              >
                <AlignJustify className="h-5 w-5" />
              </label>
            </div>

            {/* Mobile Brand Name */}
            <div className="flex-1 lg:hidden px-2">
              <h1 className="text-base font-extrabold text-base-content flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-primary" />
                Ultimate Precision
              </h1>
            </div>

            {/* Right Header Actions: Theme Toggler & User Profile Dropdown */}
            <div className="flex items-center gap-3">
              <ThemeToggler />

              {/* Profile Dropdown */}
              <div className="dropdown dropdown-end">
                <div
                  tabIndex={0}
                  role="button"
                  className="btn btn-ghost btn-circle avatar border border-base-300 shadow-sm hover:border-primary transition"
                  title="User Profile Menu"
                >
                  <div className="w-9 h-9 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">
                    {user?.name ? user.name.charAt(0).toUpperCase() : "U"}
                  </div>
                </div>

                <div
                  tabIndex={0}
                  className="dropdown-content menu p-3 shadow-2xl bg-base-200 border border-base-300 rounded-3xl z-50 w-72 mt-3 flex flex-col gap-2"
                >
                  {/* User Profile Header */}
                  <div className="flex items-center gap-3 p-2 bg-base-100 rounded-2xl border border-base-300">
                    <div className="w-11 h-11 rounded-full bg-primary text-white flex items-center justify-center font-extrabold text-base shadow-sm">
                      {user?.name ? user.name.charAt(0).toUpperCase() : "U"}
                    </div>
                    <div className="flex flex-col min-w-0">
                      <span className="text-sm font-bold text-base-content truncate">
                        {user?.name || "Security Analyst"}
                      </span>
                      <span className="text-xs text-base-content/60 truncate">
                        {user?.email || "operator@surveillance.ai"}
                      </span>
                      <span className="badge badge-primary badge-xs mt-1 font-semibold text-[10px]">
                        Surveillance Operator
                      </span>
                    </div>
                  </div>

                  <div className="divider my-0"></div>

                  {/* Menu Items */}
                  <div className="flex flex-col gap-1 text-sm font-medium">
                    <Link
                      href="/user/dashboard"
                      className="flex items-center gap-3 px-3 py-2 rounded-xl text-base-content hover:bg-base-100 hover:text-primary transition"
                    >
                      <Film className="w-4 h-4 text-primary" />
                      Dashboard & Detection
                    </Link>

                    <Link
                      href="/user/history"
                      className="flex items-center gap-3 px-3 py-2 rounded-xl text-base-content hover:bg-base-100 hover:text-primary transition"
                    >
                      <Camera className="w-4 h-4 text-secondary" />
                      Footage Archive & Reports
                    </Link>

                    <button
                      onClick={handleLogout}
                      className="flex items-center gap-3 px-3 py-2 rounded-xl text-error hover:bg-error/15 transition text-left mt-1 font-semibold"
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Main Page Area */}
          <main className="flex-1 p-0 overflow-y-auto relative">{children}</main>

          {/* AI Surveillance Assistant Chatbot Widget */}
          <SurveillanceChatbot />
        </div>

        {/* Sidebar Drawer */}
        <div className="drawer-side z-40">
          <label
            htmlFor="my-drawer-3"
            className="drawer-overlay"
            aria-label="close sidebar"
          ></label>
          <div className="menu bg-base-200 border-r border-base-300 text-base-content min-h-full w-72 p-5 flex flex-col justify-between">
            <div>
              {/* Brand Header */}
              <Link
                href="/user/dashboard"
                className="flex items-center gap-3 px-2 py-3 mb-6 border-b border-base-300"
              >
                <div className="w-10 h-10 rounded-2xl bg-primary/20 text-primary flex items-center justify-center border border-primary/40 shadow-sm">
                  <ShieldAlert className="w-6 h-6" />
                </div>
                <div>
                  <div className="font-extrabold text-base text-base-content tracking-tight">
                    Ultimate Precision
                  </div>
                  <div className="text-[11px] text-primary font-semibold tracking-wider uppercase">
                    AI Surveillance System
                  </div>
                </div>
              </Link>

              {/* Navigation Items */}
              <div className="flex flex-col space-y-2">
                {SIDENAV_ITEMS.map((item, idx) => (
                  <MenuItem key={idx} item={item} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default SideNav;

const MenuItem = ({ item }: { item: SideNavItem }) => {
  const pathname = usePathname();
  const [subMenuOpen, setSubMenuOpen] = useState(false);
  const toggleSubMenu = () => {
    setSubMenuOpen(!subMenuOpen);
  };

  const isActive = pathname === item.path || (item.path !== "/user/dashboard" && pathname.startsWith(item.path));

  const baseClasses =
    "flex w-full items-center justify-between rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-200";
  const activeClasses = "bg-primary text-white shadow-md shadow-primary/25";
  const inactiveClasses =
    "text-base-content/80 hover:text-base-content hover:bg-base-100 hover:shadow-sm";

  return (
    <div>
      {item.submenu ? (
        <>
          <button
            onClick={toggleSubMenu}
            className={`${baseClasses} ${isActive ? activeClasses : inactiveClasses}`}
          >
            <div className="flex items-center gap-3">
              {item.icon}
              <span>{item.title}</span>
            </div>

            <div className={`transition-transform duration-200 ${subMenuOpen ? "rotate-180" : ""}`}>
              <ChevronDown className="w-4 h-4" />
            </div>
          </button>

          {subMenuOpen && (
            <div className="my-2 ml-4 flex flex-col space-y-1 border-l-2 border-base-300 pl-3">
              {item.subMenuItems?.map((subItem, idx) => (
                <Link
                  key={idx}
                  href={subItem.path}
                  className={`block rounded-lg px-3 py-2 text-xs font-medium transition ${
                    subItem.path === pathname
                      ? "font-bold text-primary bg-primary/10"
                      : "text-base-content/70 hover:text-base-content hover:bg-base-100"
                  }`}
                >
                  {subItem.title}
                </Link>
              ))}
            </div>
          )}
        </>
      ) : (
        <Link
          href={item.path}
          className={`${baseClasses} ${isActive ? activeClasses : inactiveClasses}`}
        >
          <div className="flex items-center gap-3">
            {item.icon}
            <span>{item.title}</span>
          </div>
        </Link>
      )}
    </div>
  );
};
