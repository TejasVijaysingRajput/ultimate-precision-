import { NextRequest, NextResponse } from "next/server";
import dbConfig from "@/app/middleware/db.config";
import Detection from "@/models/Detection";

export async function GET(req: NextRequest) {
  try {
    await dbConfig();
    const { searchParams } = new URL(req.url);
    const userId = searchParams.get("userId");

    if (!userId) {
      return NextResponse.json({ message: "userId parameter is required" }, { status: 400 });
    }

    const detections = await Detection.find({ userId }).sort({ createdAt: -1 }).lean();

    const totalVideos = detections.length;
    const completedDetections = detections.filter((d: any) => d.status === "completed").length;
    const failedDetections = detections.filter((d: any) => d.status === "failed").length;
    const pendingDetections = detections.filter((d: any) => d.status === "pending" || d.status === "processing").length;
    const violentDetections = detections.filter(
      (d: any) => d.status === "completed" && d.result?.class === "Violent"
    ).length;
    const nonViolentDetections = detections.filter(
      (d: any) => d.status === "completed" && d.result?.class === "Non-Violent"
    ).length;

    const recentDetections = detections.slice(0, 5).map((d: any) => ({
      _id: String(d._id),
      filename: d.filename,
      status: d.status,
      class: d.result?.class || "Unknown",
      violencePercentage: d.result?.violencePercentage || 0,
      createdAt: d.createdAt,
    }));

    return NextResponse.json({
      stats: {
        totalVideos,
        completedDetections,
        failedDetections,
        pendingDetections,
        violentDetections,
        nonViolentDetections,
      },
      recentDetections,
    });
  } catch (error: any) {
    console.error("Failed to fetch user stats:", error);
    return NextResponse.json(
      { message: "Failed to fetch user stats", error: error?.message },
      { status: 500 }
    );
  }
}
