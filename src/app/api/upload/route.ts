import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import { exec } from "child_process";
import { promisify } from "util";
import path from "path";
import dbConfig from "@/app/middleware/db.config";
import Detection from "@/models/Detection";

const execAsync = promisify(exec);

const VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm"];
const IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".bmp"];
const MAX_FILE_SIZE_BYTES = 1024 * 1024 * 1024; // 1GB

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;
    const userId = (formData.get("userId") as string) || "guest";
    const userEmail = (formData.get("userEmail") as string) || "";

    if (!file || typeof file === "string") {
      return NextResponse.json(
        { message: "No media file uploaded" },
        { status: 400 }
      );
    }

    // Validate file size
    if (file.size > MAX_FILE_SIZE_BYTES) {
      return NextResponse.json(
        { message: "File exceeds maximum permitted size of 1GB" },
        { status: 400 }
      );
    }

    // Validate file extension
    const ext = path.extname(file.name).toLowerCase();
    const isVideo = file.type.startsWith("video/") || VIDEO_EXTENSIONS.includes(ext);
    const isImage = file.type.startsWith("image/") || IMAGE_EXTENSIONS.includes(ext);

    if (!isVideo && !isImage) {
      return NextResponse.json(
        {
          message:
            "Invalid file format. Please upload a supported video (.mp4, .mov, .avi, .webm, .mkv) or image (.jpg, .jpeg, .png, .webp).",
        },
        { status: 400 }
      );
    }

    const mediaType: "video" | "image" = isImage ? "image" : "video";
    const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    const safeBaseName = path.basename(file.name, ext).replace(/[^a-zA-Z0-9_-]/g, "_");
    const safeFileName = `${uniqueId}_${safeBaseName}${ext || (isImage ? ".jpg" : ".mp4")}`;

    const data = await file.arrayBuffer();
    const buffer = Buffer.from(data);

    let serverMediaPath = "";
    let webMediaUrl = "";
    let pythonCmd = "";
    const framesDir = path.join(process.cwd(), "public", "uploads", "frames", uniqueId);
    fs.mkdirSync(framesDir, { recursive: true });

    if (mediaType === "image") {
      const uploadsImageDir = path.join(process.cwd(), "public", "uploads", "images");
      fs.mkdirSync(uploadsImageDir, { recursive: true });
      serverMediaPath = path.join(uploadsImageDir, safeFileName);
      fs.writeFileSync(serverMediaPath, buffer);

      webMediaUrl = `/uploads/images/${safeFileName}`;
      const relImagePath = path.relative(process.cwd(), serverMediaPath).replace(/\\/g, "/");
      const relFramesDir = path.relative(process.cwd(), framesDir).replace(/\\/g, "/");

      pythonCmd = `python python/run.py "${relImagePath}" "${relFramesDir}"`;
    } else {
      const uploadsVideoDir = path.join(process.cwd(), "public", "uploads", "videos");
      const clipsDir = path.join(process.cwd(), "public", "uploads", "clips");
      fs.mkdirSync(uploadsVideoDir, { recursive: true });
      fs.mkdirSync(clipsDir, { recursive: true });

      serverMediaPath = path.join(uploadsVideoDir, safeFileName);
      fs.writeFileSync(serverMediaPath, buffer);

      // Compatibility copies for fallback
      try {
        fs.writeFileSync("public/video.mp4", buffer);
        fs.writeFileSync("python/video.mp4", buffer);
      } catch {
        // ignore
      }

      webMediaUrl = `/uploads/videos/${safeFileName}`;
      const serverClipPath = path.join(clipsDir, `${uniqueId}_violent.mp4`);

      const relVideoPath = path.relative(process.cwd(), serverMediaPath).replace(/\\/g, "/");
      const relFramesDir = path.relative(process.cwd(), framesDir).replace(/\\/g, "/");
      const relClipPath = path.relative(process.cwd(), serverClipPath).replace(/\\/g, "/");

      pythonCmd = `python python/run.py "${relVideoPath}" "${relFramesDir}" "${relClipPath}"`;
    }

    // Execute Python AI inference
    const { stdout } = await execAsync(pythonCmd, { maxBuffer: 1024 * 1024 * 20 });

    const startIdx = stdout.indexOf("{");
    const endIdx = stdout.lastIndexOf("}");
    if (startIdx === -1 || endIdx === -1) {
      throw new Error("AI detection did not return valid JSON output: " + stdout);
    }

    const temp = JSON.parse(stdout.substring(startIdx, endIdx + 1));
    console.log("Inference output:", temp);

    const normalizeWebPath = (filePath?: string | null): string | null => {
      if (!filePath) return null;
      const clean = filePath.replace(/\\/g, "/").replace(/^(\.\/)?public\//, "").replace(/^\//, "");
      return `/${clean}`;
    };

    // Build web-accessible URLs
    const webClipUrl =
      temp.output_video && fs.existsSync(temp.output_video)
        ? normalizeWebPath(temp.output_video)
        : null;

    let webFirstFrame: string | null = null;
    let webLastFrame: string | null = null;

    if (temp.first_frame && fs.existsSync(temp.first_frame)) {
      webFirstFrame = normalizeWebPath(temp.first_frame);
    }
    if (temp.last_frame && fs.existsSync(temp.last_frame)) {
      webLastFrame = normalizeWebPath(temp.last_frame);
    }

    // Map detected frames to web URLs
    const rawDetectedFrames = Array.isArray(temp.detected_frames) ? temp.detected_frames : [];
    const mappedDetectedFrames = rawDetectedFrames.map((frame: any) => {
      const cleanImgPath = normalizeWebPath(frame.image_path);
      return {
        frameIdx: frame.frame_idx ?? 0,
        timestampSeconds: frame.timestamp_seconds ?? 0,
        timestamp: frame.timestamp ?? "00:00:00",
        confidence: frame.confidence ?? 0,
        label: frame.label ?? "Violent",
        imageUrl: cleanImgPath || webMediaUrl,
      };
    });

    // Copy clip to public/violent_video.mp4 for original fallback
    if (webClipUrl && fs.existsSync(temp.output_video)) {
      try {
        fs.copyFileSync(temp.output_video, "public/violent_video.mp4");
      } catch {
        // ignore
      }
    }

    // Connect to database and persist the record
    await dbConfig();
    const detectionDoc = await Detection.create({
      userId,
      userEmail,
      filename: file.name,
      mediaType,
      videoUrl: mediaType === "video" ? webMediaUrl : "",
      imageUrl: mediaType === "image" ? webMediaUrl : null,
      fileSize: file.size,
      fileType: file.type || `${mediaType}/${ext.replace(".", "")}`,
      status: "completed",
      result: {
        class: temp.class,
        violencePercentage: temp.violence_percentage,
        violentFrames: temp.violent_frames,
        totalFrames: temp.total_frames,
        fps: temp.fps || 0,
        duration: temp.duration || 0,
        averageConfidence: temp.average_confidence || 0,
        outputVideo: webClipUrl,
        firstFrame: webFirstFrame,
        lastFrame: webLastFrame,
        timeline: temp.timeline || [],
        detectedFrames: mappedDetectedFrames,
        hasBoundingBox: temp.has_bounding_box ?? false,
        note: temp.note ?? null,
      },
    });

    const response = {
      _id: String(detectionDoc._id),
      media_type: mediaType,
      class: temp.class,
      violence_percentage: temp.violence_percentage,
      violent_frames: temp.violent_frames,
      total_frames: temp.total_frames,
      fps: temp.fps || 0,
      duration: temp.duration || 0,
      average_confidence: temp.average_confidence || 0,
      timeline: temp.timeline || [],
      detected_frames: mappedDetectedFrames,
      has_bounding_box: temp.has_bounding_box ?? false,
      note: temp.note ?? null,
      output_video: webClipUrl ? webClipUrl.replace(/^\//, "") : null,
      first_frame: webFirstFrame,
      last_frame: webLastFrame,
      video_url: mediaType === "video" ? webMediaUrl : null,
      image_url: mediaType === "image" ? webMediaUrl : null,
      filename: file.name,
      created_at: detectionDoc.createdAt,
    };

    return NextResponse.json({
      message: "violence detection successfull",
      data: response,
    });
  } catch (error: any) {
    console.error("Upload & AI detection failed:", error);
    return NextResponse.json(
      {
        message: error?.message || "Failed to process media with AI model",
        error: String(error),
      },
      { status: 500 }
    );
  }
}
