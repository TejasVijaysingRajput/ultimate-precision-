import type { Metadata } from "next";
import "../globals.css";
import Header from "@/Components/Header";
import Footer from "@/Components/Footer";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "Ultimate Precision | Violence Detection AI",
  description:
    "Ultimate Precision: An intelligent violence detection system leveraging advanced machine learning to analyze video and image content for violent activities.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="night" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('theme');if(t){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();`,
          }}
        />
      </head>
      <body className="antialiased min-h-screen bg-base-100 text-base-content transition-colors duration-200">
        <Header />
        <Toaster />
        {children}
        <Footer />
      </body>
    </html>
  );
}
