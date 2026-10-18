"use client";

import React, { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";

const ThemeController: React.FC = () => {
  const [theme, setTheme] = useState<string>("night");
  const [mounted, setMounted] = useState<boolean>(false);

  useEffect(() => {
    setMounted(true);
    const savedTheme = localStorage.getItem("theme") || "night";
    setTheme(savedTheme);
    document.documentElement.setAttribute("data-theme", savedTheme);

    const handleThemeChange = (e: CustomEvent<string>) => {
      setTheme(e.detail);
      document.documentElement.setAttribute("data-theme", e.detail);
    };

    window.addEventListener("theme-change" as any, handleThemeChange);
    return () => {
      window.removeEventListener("theme-change" as any, handleThemeChange);
    };
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === "night" ? "corporate" : "night";
    setTheme(nextTheme);
    localStorage.setItem("theme", nextTheme);
    document.documentElement.setAttribute("data-theme", nextTheme);
    window.dispatchEvent(new CustomEvent("theme-change", { detail: nextTheme }));
  };

  if (!mounted) {
    return (
      <button
        aria-label="Toggle Theme"
        className="btn btn-ghost btn-circle btn-sm text-base-content/70"
      >
        <Sun className="w-5 h-5" />
      </button>
    );
  }

  const isDark = theme === "night";

  return (
    <button
      onClick={toggleTheme}
      type="button"
      className="btn btn-ghost btn-circle btn-sm text-base-content hover:bg-base-200 hover:text-primary transition-all duration-200"
      title={`Switch to ${isDark ? "Light Mode" : "Dark Mode"}`}
      aria-label="Toggle color theme"
    >
      {isDark ? (
        <Sun className="w-5 h-5 text-amber-400 transition-transform duration-300 hover:rotate-45" />
      ) : (
        <Moon className="w-5 h-5 text-indigo-500 transition-transform duration-300 hover:-rotate-12" />
      )}
    </button>
  );
};

export default ThemeController;
