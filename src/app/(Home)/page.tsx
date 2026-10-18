"use client";

import Login from "@/Components/Dialogs/Login";
import SignUp from "@/Components/Dialogs/Signup";

export default function Home() {
  return (
    <div className="hero bg-base-300 min-h-[57vh] flex items-center justify-center">
      <div className="hero-content text-center w-[90%] lg:w-[50vw]">
        <div className="w-full">
          {/* Hero Heading */}
          <h1 className="text-5xl font-bold text-primary">
            Welcome to Ultimate Precision
          </h1>

          {/* Tagline */}
          <p className="py-6 text-base-content text-lg">
            Empowering safety with intelligent vision. Detect violence, report
            incidents, and take action with cutting-edge AI technology. Join us
            in creating a safer and smarter world through innovation!
          </p>

          {/* CTA Button */}
          <button
            className="btn btn-primary hover:btn-secondary"
            onClick={() => {
              (
                document.getElementById("signup") as HTMLDialogElement
              ).showModal();
            }}
          >
            Get Started Now
          </button>
        </div>
      </div>

      {/* Login Dialog */}
      <Login />
      <SignUp />
    </div>
  );
}
