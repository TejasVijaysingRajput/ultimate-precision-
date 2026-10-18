import dbConfig from "@/app/middleware/db.config";
import User from "@/models/User";
import { hashPassword, verifyPassword } from "@/lib/password";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const email = typeof body?.email === "string" ? body.email.trim().toLowerCase() : "";
    const password = typeof body?.password === "string" ? body.password : "";
    if (!email || !password) {
      return NextResponse.json({ message: "Email and password are required" }, { status: 400 });
    }

    await dbConfig();
    const user = await User.findOne({ email }).select("+password +passwordHash");
    if (!user) {
      return NextResponse.json({ message: "Invalid email or password" }, { status: 401 });
    }

    const passwordMatches = user.passwordHash
      ? await verifyPassword(password, user.passwordHash)
      : user.password === password;
    if (!passwordMatches) {
      return NextResponse.json({ message: "Invalid email or password" }, { status: 401 });
    }

    if (!user.passwordHash && user.password) {
      await User.collection.updateOne(
        { _id: user._id },
        { $set: { passwordHash: await hashPassword(password) }, $unset: { password: "" } }
      );
    }

    return NextResponse.json({
      message: "Login successful",
      user: { _id: String(user._id), id: String(user._id), name: user.name, email: user.email },
    });
  } catch (error: unknown) {
    if (error instanceof SyntaxError) {
      return NextResponse.json({ message: "Invalid request body" }, { status: 400 });
    }
    console.error("Login failed", error);
    return NextResponse.json({ message: "Unable to log in right now" }, { status: 500 });
  }
}
