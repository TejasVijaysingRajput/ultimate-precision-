import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import dbConfig from "@/app/middleware/db.config";
import Detection from "@/models/Detection";

export async function GET(req: NextRequest) {
  try {
    await dbConfig();
    const { searchParams } = new URL(req.url);
    const id = searchParams.get("id");
    const userId = searchParams.get("userId");

    if (id) {
      const detection = await Detection.findById(id).lean();
      if (!detection) {
        return NextResponse.json({ message: "Report not found" }, { status: 404 });
      }
      return NextResponse.json({ detection });
    }

    if (!userId) {
      return NextResponse.json({ message: "userId parameter is required" }, { status: 400 });
    }

    const detections = await Detection.find({ userId })
      .sort({ createdAt: -1 })
      .lean();

    return NextResponse.json({ detections });
  } catch (error: any) {
    console.error("Failed to fetch detections:", error);
    return NextResponse.json(
      { message: "Failed to fetch detections", error: error?.message },
      { status: 500 }
    );
  }
}

export async function DELETE(req: NextRequest) {
  try {
    await dbConfig();
    const { searchParams } = new URL(req.url);
    const id = searchParams.get("id");
    const userId = searchParams.get("userId");

    if (!id) {
      return NextResponse.json({ message: "Detection id is required" }, { status: 400 });
    }

    // Try finding by ID first
    const detection = await Detection.findById(id);
    if (!detection) {
      return NextResponse.json({ message: "Detection record not found" }, { status: 404 });
    }

    // Verify ownership if userId is passed and record has a specific owner
    if (userId && detection.userId && detection.userId !== "guest" && detection.userId !== userId) {
      return NextResponse.json({ message: "Unauthorized to delete this record" }, { status: 403 });
    }

    // Helper to safely delete file from public directory
    const safeDeleteFile = (relUrl?: string | null) => {
      if (!relUrl) return;
      try {
        const cleanRel = relUrl.replace(/^[/\\]+/, "");
        const fullPath = path.join(process.cwd(), "public", cleanRel);
        if (fs.existsSync(fullPath)) {
          fs.unlinkSync(fullPath);
        }
      } catch (err) {
        console.warn("Could not delete file:", relUrl, err);
      }
    };

    // Attempt to remove associated media files
    try {
      safeDeleteFile(detection.videoUrl);
      safeDeleteFile(detection.imageUrl);
      safeDeleteFile(detection.result?.outputVideo);
      safeDeleteFile(detection.result?.firstFrame);
      safeDeleteFile(detection.result?.lastFrame);

      // Clean up extracted frames folder if it exists
      const frames = detection.result?.detectedFrames;
      if (frames && frames.length > 0 && frames[0].imageUrl) {
        const frameRel = frames[0].imageUrl.replace(/^[/\\]+/, "");
        const frameDir = path.dirname(path.join(process.cwd(), "public", frameRel));
        if (fs.existsSync(frameDir) && frameDir.includes(path.join("uploads", "frames"))) {
          fs.rmSync(frameDir, { recursive: true, force: true });
        }
      }
    } catch (fsErr) {
      console.warn("Could not delete some associated files:", fsErr);
    }

    await Detection.deleteOne({ _id: id });

    return NextResponse.json({
      success: true,
      message: "Detection deleted successfully",
      id,
    });
  } catch (error: any) {
    console.error("Failed to delete detection:", error);
    return NextResponse.json(
      { message: "Failed to delete detection", error: error?.message },
      { status: 500 }
    );
  }
}
