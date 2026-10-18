import dbConfig from "@/app/middleware/db.config";
import User from "@/models/User";
import { hashPassword } from "@/lib/password";
import { NextRequest, NextResponse } from "next/server";

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const name = typeof body?.user?.name === "string" ? body.user.name.trim() : "";
    const email = typeof body?.user?.email === "string" ? body.user.email.trim().toLowerCase() : "";
    const password = typeof body?.user?.password === "string" ? body.user.password : "";
    if (!name || !email || !password) {
      return NextResponse.json({ message: "Name, email, and password are required" }, { status: 400 });
    }
    if (!emailPattern.test(email)) {
      return NextResponse.json({ message: "Enter a valid email address" }, { status: 400 });
    }

    await dbConfig();
    if (await User.findOne({ email })) {
      return NextResponse.json({ message: "An account with this email already exists" }, { status: 409 });
    }

    const newUser = await User.create({ name, email, passwordHash: await hashPassword(password) });
    return NextResponse.json({
      message: "Account created successfully",
      user: { _id: String(newUser._id), id: String(newUser._id), name: newUser.name, email: newUser.email },
    }, { status: 201 });
  } catch (error: unknown) {
    if (error && typeof error === "object" && "code" in error && error.code === 11000) {
      return NextResponse.json({ message: "An account with this email already exists" }, { status: 409 });
    }
    if (error instanceof SyntaxError) {
      return NextResponse.json({ message: "Invalid request body" }, { status: 400 });
    }
    console.error("Account registration failed", error);
    return NextResponse.json({ message: "Unable to create your account right now" }, { status: 500 });
  }
}
