import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/Components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        night: {
          ...require("daisyui/src/theming/themes")["night"],
          primary: "#38bdf8",
          secondary: "#818cf8",
          accent: "#2dd4bf",
          "base-100": "#0b0f19",
          "base-200": "#111827",
          "base-300": "#1f2937",
          "base-content": "#f9fafb",
          success: "#10b981",
          error: "#f43f5e",
          warning: "#f59e0b",
        },
      },
      "corporate",
      "dim",
      "forest",
      "dark",
    ],
    darkTheme: "night",
  },
} satisfies Config;
