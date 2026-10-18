"use client";

import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import Link from "next/link";
import {
  UploadCloud,
  FileVideo,
  ImageIcon,
  ShieldAlert,
  ShieldCheck,
  Clock,
  Film,
  AlertCircle,
  ExternalLink,
  Loader2,
  X,
  Play,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  Trash2,
} from "lucide-react";

interface UserStats {
  totalVideos: number;
  completedDetections: number;
  failedDetections: number;
  pendingDetections: number;
  violentDetections: number;
  nonViolentDetections: number;
}

interface RecentItem {
  _id: string;
  filename: string;
  status: string;
  class: string;
  violencePercentage: number;
  createdAt: string;
}

const VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm"];
const IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".bmp"];
const MAX_UPLOAD_SIZE_BYTES = 1024 * 1024 * 1024; // 1GB (1024 MB)

const Dashboard = () => {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [user, setUser] = useState<{ _id?: string; id?: string; name?: string; email?: string } | null>(null);
  const [stats, setStats] = useState<UserStats>({
    totalVideos: 0,
    completedDetections: 0,
    failedDetections: 0,
    pendingDetections: 0,
    violentDetections: 0,
    nonViolentDetections: 0,
  });
  const [recentDetections, setRecentDetections] = useState<RecentItem[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);

  // Upload state
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileCategory, setFileCategory] = useState<"video" | "image">("video");
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStage, setProcessingStage] = useState<"idle" | "uploading" | "analyzing">("idle");
  const [uploadProgress, setUploadProgress] = useState(0);

  const loadStats = async (uid: string) => {
    if (!uid) {
      setLoadingStats(false);
      return;
    }
    try {
      const res = await axios.get(`/api/user/stats?userId=${encodeURIComponent(uid)}`);
      if (res.data?.stats) {
        setStats(res.data.stats);
      }
      if (res.data?.recentDetections) {
        setRecentDetections(res.data.recentDetections);
      }
    } catch (err) {
      console.error("Failed to load user stats:", err);
    } finally {
      setLoadingStats(false);
    }
  };

  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleDelete = async (id: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete the detection report for "${filename}"?`)) {
      return;
    }
    setDeletingId(id);
    try {
      const uid = user?._id || user?.id || "";
      await axios.delete(
        `/api/detections?id=${encodeURIComponent(id)}${uid ? `&userId=${encodeURIComponent(uid)}` : ""}`
      );
      toast.success("Detection report deleted successfully");
      setRecentDetections((prev) => prev.filter((d) => d._id !== id));
      if (uid) {
        loadStats(uid);
      }
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Failed to delete report");
    } finally {
      setDeletingId(null);
    }
  };

  useEffect(() => {
    try {
      const stored = localStorage.getItem("user");
      if (stored) {
        const u = JSON.parse(stored);
        setUser(u);
        const uid = u._id || u.id || "";
        loadStats(uid);
      } else {
        setLoadingStats(false);
      }
    } catch {
      setLoadingStats(false);
    }
  }, []);

  // Cleanup object URL
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleSelectClick = () => {
    if (!isProcessing && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const validateAndSetFile = (file: File) => {
    const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    const isVideo = file.type.startsWith("video/") || VIDEO_EXTENSIONS.includes(ext);
    const isImage = file.type.startsWith("image/") || IMAGE_EXTENSIONS.includes(ext);

    if (!isVideo && !isImage) {
      toast.error("Invalid format. Please select a video (.mp4, .mov, .avi, .webm) or image (.jpg, .png, .webp)");
      return false;
    }

    if (file.size > MAX_UPLOAD_SIZE_BYTES) {
      toast.error("File is too large. Maximum supported size is 1GB (1024MB)");
      return false;
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    const newUrl = URL.createObjectURL(file);
    setPreviewUrl(newUrl);
    setSelectedFile(file);
    setFileCategory(isImage ? "image" : "video");
    return true;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      validateAndSetFile(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (isProcessing) return;
    const file = e.dataTransfer.files?.[0];
    if (file) {
      validateAndSetFile(file);
    }
  };

  const handleClearFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleStartUploadAndInference = async () => {
    if (!selectedFile) {
      toast.error("Please select a video or image file first");
      return;
    }

    setIsProcessing(true);
    setProcessingStage("uploading");
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("userId", user?._id || user?.id || "guest");
    formData.append("userEmail", user?.email || "");

    try {
      const res = await axios.post("/api/upload", formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(percent);
            if (percent >= 100) {
              setProcessingStage("analyzing");
            }
          }
        },
        timeout: 300000, // 5 minutes for large files
      });

      if (res.data?.data) {
        toast.success(`${fileCategory === "image" ? "Image" : "Video"} analyzed successfully!`);
        sessionStorage.setItem("videoAnalysisResult", JSON.stringify(res.data.data));
        const reportId = res.data.data._id;
        router.push(reportId ? `/user/dashboard/result?id=${reportId}` : "/user/dashboard/result");
      } else {
        throw new Error("No analysis data returned by server");
      }
    } catch (err: any) {
      console.error("Upload error:", err);
      const msg = err.response?.data?.message || err.message || "Failed to analyze media. Please try again.";
      toast.error(msg);
      setIsProcessing(false);
      setProcessingStage("idle");
    }
  };

  return (
    <div className="flex flex-col min-h-[89vh] bg-base-100 p-6 md:p-10 max-w-6xl mx-auto w-full gap-8">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-base-200 p-6 md:p-8 rounded-3xl shadow-sm border border-base-300">
        <div>
          <h1 className="text-3xl font-extrabold text-primary">
            Welcome back, {user?.name || "Security Analyst"}!
          </h1>
          <p className="text-base-content/75 text-sm mt-1">
            Ultimate Precision AI Violence Detection Platform. Upload surveillance footage or incident images up to 1GB for deep-learning analysis.
          </p>
        </div>
        <Link href="/user/history" className="btn btn-outline btn-sm gap-2">
          <Clock className="w-4 h-4" />
          View History
        </Link>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/70 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Total Uploads</span>
            <Film className="w-5 h-5 text-primary" />
          </div>
          <div className="text-3xl font-extrabold text-base-content">
            {loadingStats ? "..." : stats.totalVideos}
          </div>
          <p className="text-xs text-base-content/60 mt-1">Footage analyzed</p>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/70 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Completed</span>
            <ShieldCheck className="w-5 h-5 text-success" />
          </div>
          <div className="text-3xl font-extrabold text-success">
            {loadingStats ? "..." : stats.completedDetections}
          </div>
          <p className="text-xs text-base-content/60 mt-1">Processed successfully</p>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/70 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Violent Detected</span>
            <ShieldAlert className="w-5 h-5 text-rose-500" />
          </div>
          <div className="text-3xl font-extrabold text-rose-500">
            {loadingStats ? "..." : stats.violentDetections}
          </div>
          <p className="text-xs text-base-content/60 mt-1">Incidents flagged</p>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/70 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider">Safe Media</span>
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">
            {loadingStats ? "..." : stats.nonViolentDetections}
          </div>
          <p className="text-xs text-base-content/60 mt-1">Non-violent files</p>
        </div>
      </div>

      {/* Upload & Preview Section */}
      <div className="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-md">
        <h2 className="text-xl font-bold text-base-content mb-2 flex items-center gap-2">
          <UploadCloud className="w-6 h-6 text-primary" />
          Upload Footage for Incident Detection
        </h2>
        <p className="text-sm text-base-content/70 mb-6">
          Supported formats: Videos (MP4, MOV, AVI, WEBM, MKV) and Images (JPG, PNG, WEBP) <strong className="text-primary font-semibold">up to 1GB</strong>. The deep learning neural network inspects each frame for physical violence.
        </p>

        {/* Dropzone & Preview Box */}
        <div
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={handleSelectClick}
          className={`border-2 border-dashed rounded-2xl p-6 md:p-8 text-center cursor-pointer transition duration-200 flex flex-col items-center justify-center relative ${
            isProcessing
              ? "border-primary/40 bg-base-300/40 cursor-not-allowed"
              : selectedFile
              ? "border-primary bg-primary/5 hover:bg-primary/10"
              : "border-base-content/20 hover:border-primary/60 hover:bg-base-300/30"
          }`}
        >
          <input
            type="file"
            accept="video/*,image/*,.mp4,.mov,.avi,.mkv,.webm,.jpg,.jpeg,.png,.webp"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            disabled={isProcessing}
          />

          {isProcessing ? (
            <div className="flex flex-col items-center gap-3 py-6">
              <Loader2 className="w-12 h-12 text-primary animate-spin" />
              <p className="text-lg font-bold text-base-content">
                {processingStage === "uploading"
                  ? `Uploading ${fileCategory === "image" ? "Image" : "Footage"} (${uploadProgress}%)...`
                  : "Running Deep Learning Violence Detection..."}
              </p>
              <p className="text-xs text-base-content/60 max-w-md">
                {processingStage === "uploading"
                  ? "Transferring bytes to AI processing backend..."
                  : "Convolutional neural network is analyzing frames, computing confidence probabilities, and mapping timeline..."}
              </p>
              {processingStage === "uploading" && (
                <div className="w-64 bg-base-300 rounded-full h-2.5 overflow-hidden mt-2">
                  <div
                    className="bg-primary h-2.5 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
              )}
            </div>
          ) : selectedFile && previewUrl ? (
            <div className="flex flex-col items-center gap-4 w-full max-w-md">
              <div className="relative w-full rounded-2xl overflow-hidden border border-base-300 shadow-md bg-black">
                {fileCategory === "image" ? (
                  <img
                    src={previewUrl}
                    alt="Uploaded Preview"
                    className="w-full max-h-64 object-contain"
                  />
                ) : (
                  <video
                    src={previewUrl}
                    controls
                    className="w-full max-h-64 object-contain"
                  />
                )}
                <button
                  onClick={handleClearFile}
                  className="btn btn-circle btn-xs btn-error text-white absolute top-2 right-2 shadow-md"
                  title="Remove file"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="text-center">
                <div className="flex items-center justify-center gap-2">
                  {fileCategory === "image" ? (
                    <ImageIcon className="w-4 h-4 text-primary" />
                  ) : (
                    <FileVideo className="w-4 h-4 text-primary" />
                  )}
                  <p className="text-sm font-bold text-base-content truncate max-w-xs">
                    {selectedFile.name}
                  </p>
                </div>
                <p className="text-xs text-base-content/60 mt-0.5">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Click to replace file
                </p>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2 py-6">
              <UploadCloud className="w-12 h-12 text-base-content/40" />
              <p className="text-base font-semibold text-base-content">
                Drag and drop your video or image file here, or{" "}
                <span className="text-primary underline">browse</span>
              </p>
              <p className="text-xs text-base-content/50">
                MP4, MOV, AVI, WEBM, JPG, PNG <strong className="text-primary font-bold">up to 1GB</strong>
              </p>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-base-content/60 flex items-center gap-1.5">
            <AlertCircle className="w-4 h-4 text-primary shrink-0" />
            AI violence detection model executes frame-by-frame analysis with real-time confidence scores.
          </div>
          <button
            onClick={handleStartUploadAndInference}
            disabled={!selectedFile || isProcessing}
            className="btn btn-primary px-8 w-full sm:w-auto shadow-sm"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Processing AI...
              </>
            ) : (
              "Start AI Detection"
            )}
          </button>
        </div>
      </div>

      {/* Recent Detection Reports Table (Replacing poor contrast layout) */}
      <div className="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-sm flex flex-col gap-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-bold text-base-content flex items-center gap-2">
              <Clock className="w-5 h-5 text-primary" />
              Recent Video & Image Reports
            </h3>
            <p className="text-xs text-base-content/60 mt-0.5">
              Latest incident detections and violence classification logs
            </p>
          </div>
          <Link href="/user/history" className="btn btn-ghost btn-xs text-primary font-bold gap-1">
            View All History <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {recentDetections.length === 0 ? (
          <div className="p-8 bg-base-100 rounded-2xl border border-base-300 text-center text-xs text-base-content/60">
            No detection reports yet. Upload a media file above to run your first analysis.
          </div>
        ) : (
          <div className="bg-base-100/70 border border-base-300 rounded-2xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="table w-full">
                <thead>
                  <tr className="bg-base-300/50 text-base-content/80 text-xs uppercase font-extrabold tracking-wider border-b border-base-300">
                    <th className="py-3.5 pl-5">Media Filename</th>
                    <th>Date</th>
                    <th>Classification</th>
                    <th>Violence %</th>
                    <th className="text-right pr-5">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-base-300/50">
                  {recentDetections.slice(0, 5).map((item) => {
                    const isViolent = item.class === "Violent";
                    return (
                      <tr key={item._id} className="hover:bg-base-200/50 transition duration-150">
                        {/* Filename with high contrast */}
                        <td className="py-3.5 pl-5">
                          <div className="flex items-center gap-2.5">
                            <FileVideo className="w-4 h-4 text-primary shrink-0" />
                            <span
                              className="font-bold text-base-content text-sm max-w-xs md:max-w-md truncate"
                              title={item.filename}
                            >
                              {item.filename}
                            </span>
                          </div>
                        </td>

                        {/* Date */}
                        <td className="text-xs text-base-content/75 font-medium whitespace-nowrap">
                          {new Date(item.createdAt).toLocaleDateString()}
                        </td>

                        {/* Classification Badge - Neat & Non-wrapping */}
                        <td>
                          {isViolent ? (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap bg-rose-500/15 text-rose-400 border border-rose-500/30 shadow-sm">
                              <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse shrink-0"></span>
                              Violent Incident
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shadow-sm">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0"></span>
                              Non-Violent
                            </span>
                          )}
                        </td>

                        {/* Violence % */}
                        <td className="font-mono text-sm font-bold">
                          <span className={isViolent ? "text-rose-400" : "text-emerald-400"}>
                            {Number(item.violencePercentage || 0).toFixed(1)}%
                          </span>
                        </td>

                        {/* Action Link & Delete Button */}
                        <td className="text-right pr-5">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => router.push(`/user/dashboard/result?id=${item._id}`)}
                              className="btn btn-xs btn-outline btn-primary rounded-lg font-bold gap-1"
                              title="View Report"
                            >
                              <ExternalLink className="w-3 h-3" />
                              Report
                            </button>
                            <button
                              onClick={() => handleDelete(item._id, item.filename)}
                              disabled={deletingId === item._id}
                              className="btn btn-xs btn-ghost btn-circle text-error hover:bg-error/15 transition"
                              title="Delete Report"
                            >
                              {deletingId === item._id ? (
                                <span className="loading loading-spinner loading-xs text-error"></span>
                              ) : (
                                <Trash2 className="w-3.5 h-3.5" />
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
    </div>
  );
};

export default Dashboard;
