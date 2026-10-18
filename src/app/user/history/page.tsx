"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import {
  Trash2,
  ExternalLink,
  RefreshCw,
  Clock,
  Video,
  ImageIcon,
  Play,
  Eye,
  X,
  FileText,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

interface TimelineItem {
  start: string;
  end: string;
  startSeconds: number;
  endSeconds: number;
  confidence: number;
  frameCount: number;
}

interface DetectedFrame {
  frameIdx: number;
  timestampSeconds: number;
  timestamp: string;
  confidence: number;
  label: string;
  imageUrl: string;
}

interface DetectionItem {
  _id: string;
  filename: string;
  mediaType?: "video" | "image";
  videoUrl?: string;
  imageUrl?: string;
  fileSize: number;
  status: "pending" | "processing" | "completed" | "failed";
  createdAt: string;
  result?: {
    class: string;
    violencePercentage: number;
    violentFrames: number;
    totalFrames: number;
    fps: number;
    duration: number;
    averageConfidence: number;
    timeline?: TimelineItem[];
    detectedFrames?: DetectedFrame[];
    firstFrame?: string;
    lastFrame?: string;
    outputVideo?: string;
    hasBoundingBox?: boolean;
    note?: string;
  };
}

export default function HistoryPage() {
  const router = useRouter();
  const [detections, setDetections] = useState<DetectionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<string>("");

  // Quick Media Preview Modal State
  const [previewMedia, setPreviewMedia] = useState<{
    url: string;
    type: "video" | "image";
    title: string;
  } | null>(null);

  const fetchHistory = async (uid: string) => {
    if (!uid) {
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(`/api/detections?userId=${encodeURIComponent(uid)}`);
      setDetections(res.data.detections || []);
    } catch (err: any) {
      console.error("Failed to load history:", err);
      toast.error(err.response?.data?.message || "Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    try {
      const stored = localStorage.getItem("user");
      if (stored) {
        const u = JSON.parse(stored);
        const uid = u._id || u.id || "";
        setUserId(uid);
        fetchHistory(uid);
      } else {
        setLoading(false);
      }
    } catch {
      setLoading(false);
    }
  }, []);

  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Are you sure you want to delete the detection report for "${name}"?`)) {
      return;
    }
    setDeletingId(id);
    try {
      await axios.delete(
        `/api/detections?id=${encodeURIComponent(id)}${userId ? `&userId=${encodeURIComponent(userId)}` : ""}`
      );
      toast.success("Detection record deleted successfully");
      setDetections((prev) => prev.filter((d) => d._id !== id));
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Failed to delete record");
    } finally {
      setDeletingId(null);
    }
  };

  const handleOpenReport = (item: DetectionItem) => {
    const isImage = item.mediaType === "image" || Boolean(item.imageUrl);
    if (item.result) {
      sessionStorage.setItem(
        "videoAnalysisResult",
        JSON.stringify({
          _id: item._id,
          media_type: isImage ? "image" : "video",
          class: item.result.class,
          violence_percentage: item.result.violencePercentage,
          violent_frames: item.result.violentFrames,
          total_frames: item.result.totalFrames,
          fps: item.result.fps,
          duration: item.result.duration,
          average_confidence: item.result.averageConfidence,
          timeline: item.result.timeline,
          detected_frames: item.result.detectedFrames || [],
          filename: item.filename,
          video_url: item.videoUrl,
          image_url: item.imageUrl,
          output_video: item.result.outputVideo,
          first_frame: item.result.firstFrame,
          last_frame: item.result.lastFrame,
          created_at: item.createdAt,
        })
      );
    }
    router.push(`/user/dashboard/result?id=${item._id}`);
  };

  const handleOpenQuickPreview = (item: DetectionItem) => {
    const isImage = item.mediaType === "image" || Boolean(item.imageUrl);
    const mediaUrl = isImage
      ? item.imageUrl || item.result?.firstFrame || ""
      : item.videoUrl || "/video.mp4";

    setPreviewMedia({
      url: mediaUrl,
      type: isImage ? "image" : "video",
      title: item.filename,
    });
  };

  return (
    <div className="min-h-[88vh] bg-base-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto flex flex-col gap-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-base-200 p-6 rounded-3xl border border-base-300 shadow-sm">
          <div>
            <h1 className="text-3xl font-extrabold text-primary flex items-center gap-3">
              <Clock className="w-8 h-8 text-primary" />
              Detection History & Archive
            </h1>
            <p className="text-base-content/75 text-sm mt-1">
              Complete archive of surveillance videos and images analyzed by the Ultimate Precision neural network.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => fetchHistory(userId)}
              className="btn btn-outline btn-sm gap-2"
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </button>
            <Link href="/user/dashboard" className="btn btn-primary btn-sm gap-2 shadow-sm">
              <Video className="w-4 h-4" />
              New Detection
            </Link>
          </div>
        </div>

        {/* Content Table */}
        {loading ? (
          <div className="flex flex-col items-center justify-center p-20 bg-base-200 rounded-3xl border border-base-300">
            <span className="loading loading-spinner loading-lg text-primary"></span>
            <p className="mt-4 text-base-content/70 font-medium">Loading detection records from database...</p>
          </div>
        ) : detections.length === 0 ? (
          <div className="text-center p-16 bg-base-200 rounded-3xl shadow-sm border border-base-300">
            <Video className="w-16 h-16 mx-auto text-base-content/40 mb-4" />
            <h3 className="text-xl font-bold text-base-content mb-2">No Detection History Yet</h3>
            <p className="text-base-content/70 max-w-md mx-auto mb-6 text-sm">
              You haven&apos;t uploaded any media yet. Upload a video or image (up to 1GB) on the Dashboard to run the AI violence detection model and save your first report.
            </p>
            <Link href="/user/dashboard" className="btn btn-primary">
              Upload Media Now
            </Link>
          </div>
        ) : (
          <div className="bg-base-200 rounded-3xl shadow-md border border-base-300 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="table w-full">
                <thead>
                  <tr className="bg-base-300/60 text-base-content/80 text-xs uppercase font-extrabold tracking-wider border-b border-base-300">
                    <th className="py-4 pl-6">Preview</th>
                    <th>Date & Time</th>
                    <th>Media Filename</th>
                    <th>Type</th>
                    <th>Classification</th>
                    <th>Violence %</th>
                    <th>Flagged / Total</th>
                    <th>Duration</th>
                    <th className="text-center pr-6">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-base-300/50">
                  {detections.map((item) => {
                    const isImage = item.mediaType === "image" || Boolean(item.imageUrl);
                    const isViolent = item.result?.class === "Violent";
                    const thumbnailSrc = isImage
                      ? item.imageUrl || item.result?.firstFrame || "/sample.jpg"
                      : item.result?.firstFrame || "/sample.jpg";

                    return (
                      <tr key={item._id} className="hover:bg-base-100/50 transition duration-150">
                        {/* Media Thumbnail */}
                        <td className="py-3 pl-6">
                          <div
                            onClick={() => handleOpenQuickPreview(item)}
                            className="relative w-14 h-10 rounded-xl overflow-hidden bg-black cursor-pointer group border border-base-300 shadow-sm"
                            title="Click to view media preview"
                          >
                            <img
                              src={thumbnailSrc}
                              alt="Media Preview"
                              className="w-full h-full object-cover group-hover:scale-110 transition duration-200"
                            />
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition">
                              {isImage ? (
                                <Eye className="w-3.5 h-3.5 text-white" />
                              ) : (
                                <Play className="w-3.5 h-3.5 text-white" />
                              )}
                            </div>
                          </div>
                        </td>

                        {/* Date & Time */}
                        <td className="text-xs text-base-content/75 whitespace-nowrap font-medium">
                          <div>{new Date(item.createdAt).toLocaleDateString()}</div>
                          <div className="text-[11px] text-base-content/50 font-mono">
                            {new Date(item.createdAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
                          </div>
                        </td>

                        {/* Filename */}
                        <td className="font-bold text-base-content max-w-xs truncate" title={item.filename}>
                          {item.filename}
                        </td>

                        {/* Media Type */}
                        <td>
                          {isImage ? (
                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-primary/10 text-primary border border-primary/20">
                              <ImageIcon className="w-3 h-3" />
                              Image
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-secondary/10 text-secondary border border-secondary/20">
                              <Video className="w-3 h-3" />
                              Video
                            </span>
                          )}
                        </td>

                        {/* Classification Badge - Neat, Professional, Non-wrapping */}
                        <td>
                          {isViolent ? (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap bg-rose-500/15 text-rose-400 border border-rose-500/30 shadow-sm">
                              <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse shrink-0"></span>
                              Violent Incident
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shadow-sm">
                              <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0"></span>
                              Non-Violent
                            </span>
                          )}
                        </td>

                        {/* Violence % */}
                        <td className="font-mono text-sm font-bold">
                          <span className={isViolent ? "text-rose-400" : "text-emerald-400"}>
                            {Number(item.result?.averageConfidence || item.result?.violencePercentage || 0).toFixed(1)}%
                          </span>
                        </td>

                        {/* Frames */}
                        <td className="text-xs font-mono text-base-content/80">
                          {isImage ? "1 / 1" : `${item.result?.violentFrames || 0} / ${item.result?.totalFrames || 0}`}
                        </td>

                        {/* Duration */}
                        <td className="text-xs font-mono text-base-content/80">
                          {item.result?.duration ? `${item.result.duration}s` : isImage ? "Image" : "N/A"}
                        </td>

                        {/* Actions */}
                        <td className="pr-6">
                          <div className="flex items-center justify-center gap-2">
                            <button
                              onClick={() => handleOpenReport(item)}
                              className="btn btn-sm btn-outline btn-primary rounded-xl gap-1.5 font-bold hover:shadow-md transition"
                              title="Open Detection Report"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                              Report
                            </button>
                            <button
                              onClick={() => handleDelete(item._id, item.filename)}
                              disabled={deletingId === item._id}
                              className="btn btn-sm btn-ghost btn-circle text-error hover:bg-error/15 transition"
                              title="Delete Record"
                            >
                              {deletingId === item._id ? (
                                <span className="loading loading-spinner loading-xs text-error"></span>
                              ) : (
                                <Trash2 className="w-4 h-4" />
                              )}
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Quick Media Preview Modal */}
      {previewMedia && (
        <div
          className="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150"
          onClick={() => setPreviewMedia(null)}
        >
          <div
            className="relative bg-base-200 border border-base-300 rounded-3xl p-6 max-w-3xl w-full flex flex-col gap-4 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold text-base-content truncate pr-4">
                Media Preview: {previewMedia.title}
              </h3>
              <button
                onClick={() => setPreviewMedia(null)}
                className="btn btn-circle btn-sm btn-ghost"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="rounded-2xl overflow-hidden bg-black aspect-video flex items-center justify-center">
              {previewMedia.type === "image" ? (
                <img
                  src={previewMedia.url}
                  alt={previewMedia.title}
                  className="w-full h-full object-contain"
                />
              ) : (
                <video
                  src={previewMedia.url}
                  controls
                  autoPlay
                  className="w-full h-full object-contain"
                />
              )}
            </div>

            <div className="flex justify-end gap-2">
              <button onClick={() => setPreviewMedia(null)} className="btn btn-sm btn-outline rounded-xl">
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
