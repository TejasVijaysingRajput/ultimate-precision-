import mongoose, { Schema } from "mongoose";

export interface ITimelineItem {
  start: string;
  end: string;
  startSeconds: number;
  endSeconds: number;
  confidence: number;
  frameCount: number;
}

export interface IDetectedFrame {
  frameIdx: number;
  timestampSeconds: number;
  timestamp: string;
  confidence: number;
  label: string;
  imageUrl: string;
}

export interface IDetectionResult {
  class: string;
  violencePercentage: number;
  violentFrames: number;
  totalFrames: number;
  fps: number;
  duration: number;
  averageConfidence: number;
  outputVideo?: string | null;
  firstFrame?: string | null;
  lastFrame?: string | null;
  timeline?: ITimelineItem[];
  detectedFrames?: IDetectedFrame[];
  hasBoundingBox?: boolean;
  note?: string | null;
}

export interface IDetection extends mongoose.Document {
  userId: string;
  userEmail?: string;
  filename: string;
  mediaType: "video" | "image";
  videoUrl?: string;
  imageUrl?: string;
  fileSize: number;
  fileType: string;
  status: "pending" | "processing" | "completed" | "failed";
  errorMessage?: string | null;
  result?: IDetectionResult;
  createdAt: Date;
  updatedAt: Date;
}

const DetectionSchema = new Schema<IDetection>(
  {
    userId: {
      type: String,
      required: true,
      index: true,
    },
    userEmail: {
      type: String,
      default: "",
    },
    filename: {
      type: String,
      required: true,
    },
    mediaType: {
      type: String,
      enum: ["video", "image"],
      default: "video",
    },
    videoUrl: {
      type: String,
      default: "",
    },
    imageUrl: {
      type: String,
      default: null,
    },
    fileSize: {
      type: Number,
      default: 0,
    },
    fileType: {
      type: String,
      default: "video/mp4",
    },
    status: {
      type: String,
      enum: ["pending", "processing", "completed", "failed"],
      default: "completed",
      index: true,
    },
    errorMessage: {
      type: String,
      default: null,
    },
    result: {
      class: {
        type: String,
        default: "Non-Violent",
      },
      violencePercentage: {
        type: Number,
        default: 0,
      },
      violentFrames: {
        type: Number,
        default: 0,
      },
      totalFrames: {
        type: Number,
        default: 0,
      },
      fps: {
        type: Number,
        default: 30,
      },
      duration: {
        type: Number,
        default: 0,
      },
      averageConfidence: {
        type: Number,
        default: 0,
      },
      outputVideo: {
        type: String,
        default: null,
      },
      firstFrame: {
        type: String,
        default: null,
      },
      lastFrame: {
        type: String,
        default: null,
      },
      timeline: [
        {
          start: String,
          end: String,
          startSeconds: Number,
          endSeconds: Number,
          confidence: Number,
          frameCount: Number,
        },
      ],
      detectedFrames: [
        {
          frameIdx: Number,
          timestampSeconds: Number,
          timestamp: String,
          confidence: Number,
          label: String,
          imageUrl: String,
        },
      ],
      hasBoundingBox: {
        type: Boolean,
        default: false,
      },
      note: {
        type: String,
        default: null,
      },
    },
  },
  {
    timestamps: true,
  }
);

const Detection =
  mongoose.models.Detection ||
  mongoose.model<IDetection>("Detection", DetectionSchema);

export default Detection;
