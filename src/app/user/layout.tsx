import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import { Toaster } from "react-hot-toast";
import SideNav from "./SideNav";

const inter = Inter({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ultimate Precision | Violence Detection AI Surveillance",
  description:
    "Ultimate Precision: An intelligent violence detection system leveraging advanced machine learning to analyze video and image content for violent activities.",
};

export default function UserLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="night" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('theme');if(t){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();`,
          }}
        />
      </head>
      <body className={`antialiased min-h-screen bg-base-100 text-base-content transition-colors duration-200 ${inter.className}`}>
        <Toaster />
        <SideNav>{children}</SideNav>
      </body>
    </html>
  );
}
