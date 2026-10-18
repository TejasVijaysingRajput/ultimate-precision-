"use client";
import axios, { AxiosResponse } from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast from "react-hot-toast";
import SignUp from "./Signup";

const Login: React.FC = () => {
  const [user, setUser] = useState({ email: "", password: "" });
  const router = useRouter();
  const handleLogin = () => {
    if (user.email.length === 0 || user.password.length === 0) {
      toast.error("Please fill all the fields");
      return;
    }
    const response = axios.post("/api/auth/login", {
      ...user,
      email: user.email.trim(),
    });
    toast.promise(response, {
      loading: "Logging In...",
      success: (data: AxiosResponse) => {
        router.push("/user/dashboard");
        const user = data.data.user;
        localStorage.setItem("user", JSON.stringify(user));
        return "Logged In Successfully";
      },
      error: (error: unknown) => {
        if (axios.isAxiosError(error)) {
          return (
            error.response?.data?.message ||
            (typeof error.response?.data === "string"
              ? error.response.data
              : null) ||
            "Unable to log in"
          );
        }
        return "Unable to log in";
      },
    });
  };
  return (
    <dialog id="login" className="modal">
      <div className="modal-box">
        <div className="card w-full max-w-md shadow-lg bg-base-300 p-10 text-base-content min-h-[50vh]">
          <h1 className="text-2xl font-bold text-primary text-center pb-7">
            Login to Ultimate Precision
          </h1>
          <div className="flex flex-col items-center justify-center px-7 py-4 gap-4 w-full border border-base-content rounded-lg">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text">Email</span>
              </div>
              <input
                type="email"
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
                type="password"
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
              Login
            </button>
            <div className="flex justify-center items-center w-full">
              <span className="text-base-content px-2">
                Don&apos;t Have an Account?
              </span>
              <button
                className="btn btn-ghost text-success"
                onClick={() => {
                  (
                    document.getElementById("signup") as HTMLDialogElement
                  ).showModal();
                  (
                    document.getElementById("login") as HTMLDialogElement
                  ).close();
                }}
              >
                SignUp
              </button>
            </div>
          </div>
          <SignUp />
        </div>
      </div>
    </dialog>
  );
};
export default Login;
