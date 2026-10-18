"use client";
import axios from "axios";
import Link from "next/link";
import { useState } from "react";
import toast from "react-hot-toast";

const SignUp: React.FC = () => {
  const [user, setUser] = useState({ name: "", email: "", password: "" });
  const handleLogin = () => {
    if (
      user.email.length === 0 ||
      user.password.length === 0 ||
      user.name.length === 0
    ) {
      toast.error("Please fill all the fields");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email.trim())) {
      toast.error("Enter a valid email address");
      return;
    }
    // Password should have one Capital letter, one small letter, one number and one special symbol and it should be of 8 character
    if (
      !user.password.match(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
      )
    ) {
      toast.error(
        "Password should have one Capital letter, one small letter, one number, one special symbol, and be at least 8 characters long"
      );
      return;
    }

    const response = axios.post("/api/auth/signup", {
      user: { ...user, name: user.name.trim(), email: user.email.trim() },
    });
    toast.promise(response, {
      loading: "Creating Account...",
      success: () => {
        (document.getElementById("signup") as HTMLDialogElement).close();
        (document.getElementById("login") as HTMLDialogElement).showModal();
        return "Account Created Successfully";
      },
      error: (error: unknown) => {
        if (axios.isAxiosError(error)) {
          return (
            error.response?.data?.message ||
            (typeof error.response?.data === "string"
              ? error.response.data
              : null) ||
            "Unable to create your account"
          );
        }
        return "Unable to create your account";
      },
    });
  };
  return (
    <dialog id="signup" className="modal">
      <div className="modal-box">
        <div className="card w-full max-w-md shadow-lg bg-base-300 p-10 text-base-content">
          <h1 className="text-2xl font-bold text-primary text-center pb-7">
            Sign Up to Ultimate Precision
          </h1>
          <div className="flex flex-col items-center justify-center px-7 py-4 gap-4 w-full border border-base-content rounded-lg">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text">Full Name</span>
              </div>
              <input
                type="email"
                placeholder="Enter Your Name"
                className="input input-bordered input-primary w-full max-w-xs"
                value={user.name}
                onChange={(e) => setUser({ ...user, name: e.target.value })}
              />
            </label>
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text">Email</span>
              </div>
              <input
                type="password"
                placeholder="Enter Your Email"
                className="input input-bordered input-primary w-full max-w-xs"
                value={user.email}
                onChange={(e) => setUser({ ...user, email: e.target.value })}
              />
            </label>

            {/* Password Field */}
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text">Password</span>
              </div>
              <input
                type="text"
                placeholder="Enter Your Password"
                className="input input-bordered input-primary w-full max-w-xs"
                value={user.password}
                onChange={(e) => setUser({ ...user, password: e.target.value })}
              />
            </label>
            <div className="flex justify-around items-center w-full">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="checkbox checkbox-primary" />
                <span className="label-text">Remember Me</span>
              </label>
              <Link
                href="/forgot-password"
                className="text-sm text-primary hover:underline"
              >
                Forgot Password?
              </Link>
            </div>

            {/* Submit Button */}
            <button className="btn btn-primary w-full" onClick={handleLogin}>
              Create Account
            </button>
            <div className="flex justify-center items-center w-full">
              <span className="text-base-content px-2">
                Already Have an Account?
              </span>
              <button
                className="btn btn-ghost text-success"
                onClick={() => {
                  (
                    document.getElementById("login") as HTMLDialogElement
                  ).showModal();
                  (
                    document.getElementById("signup") as HTMLDialogElement
                  ).close();
                }}
              >
                Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </dialog>
  );
};
export default SignUp;
