import { HomeIcon, History as HistoryIcon } from "lucide-react";
import { SideNavItem } from "@/types/types";

export const SIDENAV_ITEMS: SideNavItem[] = [
  {
    title: "Dashboard",
    path: "/user/dashboard",
    icon: <HomeIcon width="24" height="24" />,
  },
  {
    title: "History",
    path: "/user/history",
    icon: <HistoryIcon width="24" height="24" />,
  },
];
