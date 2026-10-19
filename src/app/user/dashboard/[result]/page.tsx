"use client";

import React, { useEffect, useRef, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import axios from "axios";
import Link from "next/link";
import toast from "react-hot-toast";
import {
  ShieldAlert,
  ShieldCheck,
  Clock,
  Film,
  Calendar,
  Layers,
  Activity,
  ArrowLeft,
  CheckCircle2,
  Play,
  Pause,
  Volume2,
  VolumeX,
  Maximize,
  Minimize,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  ImageIcon,
  Sparkles,
  Info,
  Download,
  Printer,
  FileCode,
  FileText,
  Share2,
  Trash2,
} from "lucide-react";

interface DetectedFrame {
  frameIdx: number;
  timestampSeconds: number;
  timestamp: string;
  confidence: number;
  label: string;
  imageUrl: string;
}

interface TimelineItem {
  start: string;
  end: string;
  startSeconds: number;
  endSeconds: number;
  confidence: number;
  frameCount: number;
}

interface ReportData {
  _id?: string;
  filename?: string;
  media_type?: "video" | "image";
  class: string;
  violence_percentage: number | string;
  violent_frames: number | string;
  total_frames: number | string;
  fps?: number | string;
  duration?: number | string;
  average_confidence?: number | string;
  timeline?: TimelineItem[];
  detected_frames?: DetectedFrame[];
  has_bounding_box?: boolean;
  note?: string | null;
  output_video?: string | null;
  first_frame?: string | null;
  last_frame?: string | null;
  video_url?: string | null;
  image_url?: string | null;
  created_at?: string;
}

const Result = () => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const reportId = searchParams.get("id");

  const [response, setResponse] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"clip" | "original">("original");

  // Video Player Controls State
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const playerContainerRef = useRef<HTMLDivElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activeFrameTime, setActiveFrameTime] = useState<number | null>(null);

  // Image Zoom & Viewer State
  const [imageZoom, setImageZoom] = useState(1);
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);

  useEffect(() => {
    const loadReport = async () => {
      // 1. Try to fetch from backend if reportId is provided
      if (reportId) {
        try {
          const res = await axios.get(`/api/detections?id=${encodeURIComponent(reportId)}`);
          if (res.data?.detection) {
            const d = res.data.detection;
            const mediaType = d.mediaType || (d.imageUrl ? "image" : "video");
            setResponse({
              _id: d._id,
              filename: d.filename,
              media_type: mediaType,
              class: d.result?.class || "Unknown",
              violence_percentage: d.result?.violencePercentage || 0,
              violent_frames: d.result?.violentFrames || 0,
              total_frames: d.result?.totalFrames || 0,
              fps: d.result?.fps || 30,
              duration: d.result?.duration || 0,
              average_confidence: d.result?.averageConfidence || 0,
              timeline: d.result?.timeline || [],
              detected_frames: (d.result?.detectedFrames || (d.result as any)?.detected_frames || []).map((f: any) => ({
                frameIdx: f.frameIdx ?? f.frame_idx ?? 0,
                timestampSeconds: typeof f.timestampSeconds === "number" ? f.timestampSeconds : (typeof f.timestamp_seconds === "number" ? f.timestamp_seconds : 0),
                timestamp: formatExactTimestamp(f.timestampSeconds ?? f.timestamp_seconds, f.timestamp),
                confidence: typeof f.confidence === "number" ? f.confidence : 0,
                label: f.label || "Violent",
                imageUrl: f.imageUrl || f.image_path || "",
              })),
              has_bounding_box: d.result?.hasBoundingBox ?? false,
              note: d.result?.note ?? null,
              output_video: d.result?.outputVideo ? d.result.outputVideo.replace(/^\//, "") : null,
              first_frame: d.result?.firstFrame,
              last_frame: d.result?.lastFrame,
              video_url: d.videoUrl,
              image_url: d.imageUrl,
              created_at: d.createdAt,
            });
            setLoading(false);
            return;
          }
        } catch (err) {
          console.warn("Could not fetch detection by ID, falling back to session storage:", err);
        }
      }

      // 2. Fallback to sessionStorage
      try {
        const stored = sessionStorage.getItem("videoAnalysisResult");
        if (stored) {
          const parsed = JSON.parse(stored);
          const rawFrames = parsed.detected_frames || parsed.detectedFrames || [];
          const mappedFrames = rawFrames.map((f: any) => ({
            frameIdx: f.frameIdx ?? f.frame_idx ?? 0,
            timestampSeconds: typeof f.timestampSeconds === "number" ? f.timestampSeconds : (typeof f.timestamp_seconds === "number" ? f.timestamp_seconds : 0),
            timestamp: formatExactTimestamp(f.timestampSeconds ?? f.timestamp_seconds, f.timestamp),
            confidence: typeof f.confidence === "number" ? f.confidence : 0,
            label: f.label || "Violent",
            imageUrl: f.imageUrl || f.image_path || "",
          }));

          setResponse({
            ...parsed,
            media_type: parsed.media_type || (parsed.image_url ? "image" : "video"),
            detected_frames: mappedFrames,
          });
          setLoading(false);
          return;
        }
      } catch (err) {
        console.error("Failed to parse sessionStorage videoAnalysisResult:", err);
      }

      setLoading(false);
    };

    loadReport();
  }, [reportId]);

  // Exact timestamp formatting helper (HH:MM:SS format, e.g. 00:00:05)
  const formatExactTimestamp = (timestampSeconds?: number, timestampStr?: string) => {
    if (timestampStr && timestampStr.split(":").length === 3) {
      return timestampStr;
    }
    const s = Math.max(0, Math.floor(timestampSeconds || 0));
    const hours = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const remSecs = s % 60;
    return `${hours < 10 ? "0" : ""}${hours}:${mins < 10 ? "0" : ""}${mins}:${remSecs < 10 ? "0" : ""}${remSecs}`;
  };

  // Video time formatting helper (MM:SS)
  const formatTime = (secs: number) => {
    if (!secs || isNaN(secs)) return "00:00";
    const mins = Math.floor(secs / 60);
    const remSecs = Math.floor(secs % 60);
    return `${mins < 10 ? "0" : ""}${mins}:${remSecs < 10 ? "0" : ""}${remSecs}`;
  };

  // Video Player Event Handlers
  const togglePlayPause = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused || videoRef.current.ended) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  const handleTimeUpdate = () => {
    if (!videoRef.current) return;
    const current = videoRef.current.currentTime;
    setCurrentTime(current);

    if (response?.detected_frames && response.detected_frames.length > 0) {
      const match = response.detected_frames.find(
        (f) => Math.abs(f.timestampSeconds - current) < 0.5
      );
      setActiveFrameTime(match ? match.timestampSeconds : null);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration || 0);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVol = parseFloat(e.target.value);
    setVolume(newVol);
    if (videoRef.current) {
      videoRef.current.volume = newVol;
      videoRef.current.muted = newVol === 0;
      setIsMuted(newVol === 0);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    const targetMute = !isMuted;
    videoRef.current.muted = targetMute;
    setIsMuted(targetMute);
    if (targetMute) {
      videoRef.current.volume = 0;
    } else {
      videoRef.current.volume = volume > 0 ? volume : 1;
      setVolume(volume > 0 ? volume : 1);
    }
  };

  const handlePlaybackRateChange = (rate: number) => {
    setPlaybackRate(rate);
    if (videoRef.current) {
      videoRef.current.playbackRate = rate;
    }
  };

  const toggleFullscreen = () => {
    if (!playerContainerRef.current) return;
    if (!document.fullscreenElement) {
      playerContainerRef.current.requestFullscreen().catch((err) => {
        console.error("Fullscreen error:", err);
      });
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch((err) => {
        console.error("Exit fullscreen error:", err);
      });
      setIsFullscreen(false);
    }
  };

  const handleSeekToFrame = (timestampSeconds: number) => {
    if (activeTab !== "original") {
      setActiveTab("original");
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.currentTime = Math.max(0, timestampSeconds);
          videoRef.current.play().catch(() => {});
          setIsPlaying(true);
          setActiveFrameTime(timestampSeconds);
        }
      }, 100);
    } else {
      if (videoRef.current) {
        videoRef.current.currentTime = Math.max(0, timestampSeconds);
        videoRef.current.play().catch(() => {});
        setIsPlaying(true);
        setActiveFrameTime(timestampSeconds);
      }
    }
    playerContainerRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  // Delete Report Handler
  const [isDeleting, setIsDeleting] = useState(false);
  const handleDeleteReport = async () => {
    if (!response || !response._id) return;
    if (
      !confirm(
        `Are you sure you want to permanently delete this incident report for "${response.filename || "this media"}"? This action cannot be undone.`
      )
    ) {
      return;
    }
    setIsDeleting(true);
    try {
      const stored = localStorage.getItem("user");
      let uid = "";
      if (stored) {
        const u = JSON.parse(stored);
        uid = u._id || u.id || "";
      }
      await axios.delete(
        `/api/detections?id=${encodeURIComponent(response._id)}${uid ? `&userId=${encodeURIComponent(uid)}` : ""}`
      );
      toast.success("Incident report deleted successfully");
      sessionStorage.removeItem("videoAnalysisResult");
      router.push("/user/dashboard");
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Failed to delete report");
      setIsDeleting(false);
    }
  };

  // Report Download Handlers
  const handlePrint = () => {
    window.print();
  };

  const handleDownloadJSON = () => {
    if (!response) return;
    const blob = new Blob([JSON.stringify(response, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `forensic_report_${response._id || "detection"}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Full JSON report downloaded!");
  };

  const handleDownloadSummary = () => {
    if (!response) return;
    const isImg = response.media_type === "image";
    const vPct = Number(response.violence_percentage || 0).toFixed(1);
    const aConf = Number(response.average_confidence || vPct).toFixed(1);

    const summaryText = `========================================================================
ULTIMATE PRECISION AI - FORENSIC INCIDENT INVESTIGATION REPORT
========================================================================
Report ID          : ${response._id || "N/A"}
Timestamp          : ${response.created_at ? new Date(response.created_at).toLocaleString() : new Date().toLocaleString()}
Media Filename     : ${response.filename || "Uploaded Media"}
Media Type         : ${isImg ? "Static Image" : "Surveillance Video"}
Primary Verdict    : ${response.class.toUpperCase()}
Violence Probability: ${vPct}%
Model Confidence   : ${aConf}%
Total Examined     : ${response.total_frames || 0} frames
Flagged Frames     : ${response.violent_frames || 0} frames
Footage Duration   : ${response.duration ? `${response.duration}s` : "N/A"}
Processing Rate    : ${response.fps ? `${response.fps} fps` : "30 fps"}
AI Architecture    : Convolutional Neural Network (violence_detection_model.h5)
------------------------------------------------------------------------
INCIDENT TIMELINE INTERVALS:
${
  response.timeline && response.timeline.length > 0
    ? response.timeline
        .map(
          (t, i) =>
            `[${i + 1}] ${t.start} - ${t.end} | Flagged Frames: ${t.frameCount} | Confidence: ${t.confidence}%`
        )
        .join("\n")
    : "No high-risk violent intervals flagged."
}
------------------------------------------------------------------------
FLAGGED KEYFRAMES (${detectedFrames.length} IDENTIFIED):
${
  detectedFrames.length > 0
    ? detectedFrames
        .map(
          (f) =>
            `• Frame #${f.frameIdx} at ${f.timestamp} (${f.timestampSeconds}s) - Verdict: ${f.label} - Confidence: ${f.confidence}%`
        )
        .join("\n")
    : "No individual violent frames detected."
}
========================================================================
Certified by Ultimate Precision Surveillance AI Neural Engine
========================================================================`;

    const blob = new Blob([summaryText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `incident_summary_${response._id || "detection"}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Incident summary downloaded!");
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[85vh] p-8">
        <span className="loading loading-spinner loading-lg text-primary"></span>
        <p className="mt-4 text-base-content/70 font-medium">Loading AI detection report...</p>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[85vh] p-8 text-center">
        <ShieldAlert className="w-16 h-16 text-warning mb-4" />
        <h2 className="text-2xl font-bold text-base-content mb-2">No Detection Report Found</h2>
        <p className="text-base-content/70 max-w-md mb-6 text-sm">
          Please upload a video or image from the dashboard to generate and view real-time incident reports.
        </p>
        <button onClick={() => router.push("/user/dashboard")} className="btn btn-primary">
          Back to Dashboard
        </button>
      </div>
    );
  }

  const isImage = response.media_type === "image";
  const isViolent = response.class === "Violent";
  const violencePct = Number(response.violence_percentage || 0).toFixed(1);
  const avgConf = Number(response.average_confidence || violencePct).toFixed(1);
  const totalFrames = Number(response.total_frames || 0);
  const violentFrames = Number(response.violent_frames || 0);
  const durationText = response.duration ? `${response.duration}s` : isImage ? "Single Frame" : "N/A";
  const fpsText = response.fps ? `${response.fps} fps` : isImage ? "Static Image" : "30 fps";

  const clipVideoSrc = response.output_video
    ? response.output_video.startsWith("/")
      ? response.output_video
      : `/${response.output_video}`
    : "/violent_video.mp4";

  const originalVideoSrc = response.video_url
    ? response.video_url.startsWith("/")
      ? response.video_url
      : `/${response.video_url}`
    : "/video.mp4";

  const currentVideoSrc = activeTab === "clip" && response.output_video ? clipVideoSrc : originalVideoSrc;

  const imageSrc = response.image_url
    ? response.image_url.startsWith("/")
      ? response.image_url
      : `/${response.image_url}`
    : response.first_frame || "/sample.jpg";

  const detectedFrames = response.detected_frames || [];

  return (
    <div className="min-h-[88vh] bg-base-100 p-6 md:p-10 max-w-6xl mx-auto w-full flex flex-col gap-8 report-container">
      {/* Header & Breadcrumb - Hidden in Print */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 no-print">
        <div className="flex items-center gap-3">
          <Link href="/user/dashboard" className="btn btn-circle btn-ghost btn-sm">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-extrabold text-base-content flex items-center gap-2">
              Incident Detection Report
              {isImage ? (
                <span className="badge badge-outline badge-primary text-xs font-semibold uppercase">Image</span>
              ) : (
                <span className="badge badge-outline badge-secondary text-xs font-semibold uppercase">Video</span>
              )}
            </h1>
            <p className="text-xs text-base-content/60 mt-0.5">
              File: <span className="font-semibold text-primary">{response.filename || "Uploaded Media"}</span>
              {response.created_at && (
                <> • Analyzed on {new Date(response.created_at).toLocaleString()}</>
              )}
            </p>
          </div>
        </div>

        {/* Action Buttons: Download Report, History, New Detection */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Download Dropdown */}
          <div className="dropdown dropdown-end">
            <div
              tabIndex={0}
              role="button"
              className="btn btn-primary btn-sm gap-2 shadow-sm"
              title="Download Incident Report"
            >
              <Download className="w-4 h-4" />
              Download Report
            </div>
            <ul
              tabIndex={0}
              className="dropdown-content z-30 menu p-2 shadow-2xl bg-base-200 border border-base-300 rounded-2xl w-56 text-xs gap-1 mt-1"
            >
              <li>
                <button onClick={handlePrint} className="flex items-center gap-2.5 py-2 font-semibold">
                  <Printer className="w-4 h-4 text-primary" />
                  Print / Save as PDF
                </button>
              </li>
              <li>
                <button onClick={handleDownloadSummary} className="flex items-center gap-2.5 py-2 font-semibold">
                  <FileText className="w-4 h-4 text-secondary" />
                  Incident Summary (TXT)
                </button>
              </li>
              <li>
                <button onClick={handleDownloadJSON} className="flex items-center gap-2.5 py-2 font-semibold">
                  <FileCode className="w-4 h-4 text-accent" />
                  Full Forensic Data (JSON)
                </button>
              </li>
            </ul>
          </div>

          <Link href="/user/history" className="btn btn-outline btn-sm gap-2">
            <Clock className="w-4 h-4" />
            Archive
          </Link>
          <Link href="/user/dashboard" className="btn btn-ghost btn-sm">
            New Detection
          </Link>
          <button
            onClick={handleDeleteReport}
            disabled={isDeleting}
            className="btn btn-outline btn-error btn-sm gap-1.5"
            title="Delete this incident report"
          >
            {isDeleting ? (
              <span className="loading loading-spinner loading-xs"></span>
            ) : (
              <Trash2 className="w-4 h-4" />
            )}
            Delete
          </button>
        </div>
      </div>

      {/* Official Forensic Header for Print View */}
      <div className="hidden print-only border-b-2 border-slate-900 pb-4 mb-4">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-black text-slate-900 uppercase tracking-tight">
              Ultimate Precision AI — Forensic Incident Dossier
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Automated Deep-Learning Video Surveillance & Violence Classification System
            </p>
          </div>
          <div className="text-right text-xs text-slate-700">
            <div><strong>Report ID:</strong> {response._id || "N/A"}</div>
            <div><strong>Date:</strong> {new Date().toLocaleString()}</div>
          </div>
        </div>
      </div>

      {/* Main Status Verdict Banner */}
      <div
        className={`p-6 rounded-3xl border shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6 ${
          isViolent
            ? "bg-rose-500/10 border-rose-500/30 text-rose-400"
            : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
        }`}
      >
        <div className="flex items-center gap-4">
          <div
            className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 ${
              isViolent ? "bg-rose-500 text-white" : "bg-emerald-500 text-white"
            }`}
          >
            {isViolent ? <ShieldAlert className="w-8 h-8" /> : <ShieldCheck className="w-8 h-8" />}
          </div>
          <div>
            <div className="text-xs uppercase font-extrabold tracking-widest opacity-80">
              Primary AI Verdict
            </div>
            <div className="text-2xl font-black">
              {isViolent ? "VIOLENT ACTIVITY IDENTIFIED" : "SAFE / NO VIOLENCE DETECTED"}
            </div>
            <p className="text-xs text-base-content/80 mt-1">
              {isViolent
                ? isImage
                  ? "Violent behavior, physical aggression, or altercation detected in uploaded image."
                  : "Physical altercation, aggressive interaction, or violent behavior detected in footage."
                : isImage
                ? "The uploaded image has been classified as safe/peaceful by the neural network."
                : "The video footage has been analyzed across all frames and classified as non-violent."}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-base-100/90 px-6 py-3 rounded-2xl border border-base-300 text-base-content">
          <div className="text-center">
            <div className="text-xs uppercase text-base-content/60 font-bold">Violence Score</div>
            <div className={`text-2xl font-black ${isViolent ? "text-rose-500" : "text-emerald-500"}`}>
              {violencePct}%
            </div>
          </div>
          <div className="divider divider-horizontal m-0"></div>
          <div className="text-center">
            <div className="text-xs uppercase text-base-content/60 font-bold">Confidence</div>
            <div className="text-2xl font-black text-primary">{avgConf}%</div>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/60 text-xs font-bold uppercase mb-1">
            <span>Violent Frames</span>
            <Layers className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-2xl font-black text-base-content">{violentFrames}</div>
          <div className="text-xs text-base-content/60 mt-1">Flagged above threshold</div>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/60 text-xs font-bold uppercase mb-1">
            <span>Total Examined</span>
            <Film className="w-4 h-4 text-primary" />
          </div>
          <div className="text-2xl font-black text-base-content">{totalFrames}</div>
          <div className="text-xs text-base-content/60 mt-1">
            {isImage ? "Analyzed image frame" : "Total video frames"}
          </div>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/60 text-xs font-bold uppercase mb-1">
            <span>Duration</span>
            <Clock className="w-4 h-4 text-accent" />
          </div>
          <div className="text-2xl font-black text-base-content">{durationText}</div>
          <div className="text-xs text-base-content/60 mt-1">Footage length</div>
        </div>

        <div className="bg-base-200 border border-base-300 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between text-base-content/60 text-xs font-bold uppercase mb-1">
            <span>Frame Sampling</span>
            <Activity className="w-4 h-4 text-secondary" />
          </div>
          <div className="text-2xl font-black text-base-content">{fpsText}</div>
          <div className="text-xs text-base-content/60 mt-1">AI processing rate</div>
        </div>
      </div>

      {/* Media Playback / Preview & Detection Section */}
      {isImage ? (
        /* Image Detection & Interactive Preview Section */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-base-200 border border-base-300 rounded-3xl p-6 shadow-md flex flex-col gap-4">
            <div className="flex justify-between items-center no-print">
              <h2 className="text-lg font-bold text-base-content flex items-center gap-2">
                <ImageIcon className="w-5 h-5 text-primary" />
                Image Preview & Region Inspection
              </h2>

              {/* Zoom Toolbar */}
              <div className="flex items-center gap-2 bg-base-100 px-3 py-1.5 rounded-xl border border-base-300">
                <button
                  onClick={() => setImageZoom((prev) => Math.max(0.5, prev - 0.25))}
                  className="btn btn-ghost btn-xs btn-square"
                  title="Zoom Out"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <span className="text-xs font-mono font-bold w-12 text-center">
                  {Math.round(imageZoom * 100)}%
                </span>
                <button
                  onClick={() => setImageZoom((prev) => Math.min(3, prev + 0.25))}
                  className="btn btn-ghost btn-xs btn-square"
                  title="Zoom In"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setImageZoom(1)}
                  className="btn btn-ghost btn-xs btn-square"
                  title="Reset Zoom"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Interactive Image Container */}
            <div className="rounded-2xl overflow-hidden bg-black/90 min-h-[380px] flex items-center justify-center relative border border-base-300 p-2">
              <div className="overflow-auto max-h-[550px] w-full flex items-center justify-center">
                <img
                  src={imageSrc}
                  alt={response.filename || "Uploaded Analysis Image"}
                  style={{ transform: `scale(${imageZoom})`, transformOrigin: "center center" }}
                  className="transition-transform duration-200 max-h-[500px] object-contain rounded-lg shadow-lg cursor-zoom-in"
                  onClick={() => setIsImageModalOpen(true)}
                />
              </div>
              <div className="absolute bottom-3 right-3 bg-base-900/80 text-white text-[11px] px-2.5 py-1 rounded-md backdrop-blur-sm pointer-events-none no-print">
                Click image for full preview
              </div>
            </div>

            <div className="flex items-center justify-between text-xs text-base-content/60">
              <span>Original uploaded image passed to deep learning classifier</span>
              <span className="font-mono text-primary font-semibold">{response.filename}</span>
            </div>
          </div>

          {/* Right Column: Image Analysis Details */}
          <div className="flex flex-col gap-6">
            <div className="bg-base-200 border border-base-300 rounded-3xl p-6 shadow-sm flex flex-col gap-4">
              <h3 className="text-base font-bold text-base-content flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                Model Classification Details
              </h3>

              <div className="space-y-3">
                <div className="p-4 bg-base-100 rounded-2xl border border-base-300 flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-base-content/70 font-semibold">Classification</span>
                    {isViolent ? (
                      <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30">
                        <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
                        Violent
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                        Non-Violent
                      </span>
                    )}
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-base-content/70 font-semibold">Predicted Probability</span>
                    <span className="text-xs font-mono font-bold text-primary">{violencePct}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-base-content/70 font-semibold">Model Confidence</span>
                    <span className="text-xs font-mono font-bold text-secondary">{avgConf}%</span>
                  </div>
                </div>

                <div className="p-4 bg-base-100 rounded-2xl border border-base-300 flex items-start gap-3">
                  <Info className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div className="text-xs text-base-content/80 leading-relaxed">
                    <span className="font-bold block text-base-content mb-1">Architecture Specification</span>
                    The active deep-learning model (<code className="text-primary font-mono text-[11px]">violence_detection_model.h5</code>) evaluates whole-frame features without synthetic bounding boxes.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Video Player & Frame Analysis Section */
        <div className="flex flex-col gap-8">
          {/* Custom Video Player */}
          <div
            ref={playerContainerRef}
            className="w-full bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-md flex flex-col gap-4"
          >
            <div className="flex justify-between items-center no-print">
              <h2 className="text-lg font-bold text-base-content flex items-center gap-2">
                <Film className="w-5 h-5 text-primary" />
                Interactive Video Player
              </h2>

              {/* Video Selector Tabs */}
              {response.output_video && (
                <div className="join">
                  <button
                    onClick={() => {
                      setActiveTab("original");
                      setIsPlaying(false);
                    }}
                    className={`join-item btn btn-xs ${
                      activeTab === "original" ? "btn-primary" : "btn-ghost"
                    }`}
                  >
                    Full Video
                  </button>
                  <button
                    onClick={() => {
                      setActiveTab("clip");
                      setIsPlaying(false);
                    }}
                    className={`join-item btn btn-xs ${
                      activeTab === "clip" ? "btn-primary" : "btn-ghost"
                    }`}
                  >
                    Violent Highlight Clip
                  </button>
                </div>
              )}
            </div>

            {/* Video Element Screen */}
            <div
              onClick={togglePlayPause}
              className="rounded-2xl overflow-hidden bg-black aspect-video max-h-[580px] flex items-center justify-center relative shadow-inner cursor-pointer group"
            >
              <video
                ref={videoRef}
                key={currentVideoSrc}
                src={currentVideoSrc}
                onTimeUpdate={handleTimeUpdate}
                onLoadedMetadata={handleLoadedMetadata}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
                className="w-full h-full object-contain"
                playsInline
              />

              {/* Play/Pause Overlay indicator */}
              {!isPlaying && (
                <div className="absolute inset-0 bg-black/35 flex items-center justify-center transition-opacity no-print">
                  <div className="w-16 h-16 rounded-full bg-primary/90 text-white flex items-center justify-center shadow-2xl transform hover:scale-110 transition">
                    <Play className="w-8 h-8 ml-1" />
                  </div>
                </div>
              )}
            </div>

            {/* Custom Player Controls Toolbar - Hidden in Print */}
            <div className="flex flex-col gap-3 bg-base-100 p-4 rounded-2xl border border-base-300 shadow-sm no-print">
              {/* Timeline Seek Bar with Detected Violence Markers */}
              <div className="flex flex-col gap-1.5">
                <div className="relative w-full h-4 flex items-center">
                  <div className="absolute inset-x-0 h-2 bg-base-300 rounded-full overflow-hidden">
                    {duration > 0 &&
                      detectedFrames.map((frame, idx) => (
                        <div
                          key={idx}
                          className="absolute top-0 bottom-0 bg-rose-500/80 w-1 pointer-events-none"
                          style={{
                            left: `${(frame.timestampSeconds / duration) * 100}%`,
                          }}
                          title={`Flagged frame at ${frame.timestamp} (${frame.confidence}%)`}
                        />
                      ))}
                    <div
                      className="h-full bg-primary rounded-full transition-all duration-75 pointer-events-none"
                      style={{
                        width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%`,
                      }}
                    />
                  </div>

                  <input
                    type="range"
                    min={0}
                    max={duration || 100}
                    step={0.05}
                    value={currentTime}
                    onChange={handleSeek}
                    className="absolute inset-x-0 w-full opacity-0 hover:opacity-100 cursor-pointer h-4 z-10"
                    title="Seek video position"
                  />
                </div>

                <div className="flex justify-between items-center text-[11px] font-mono text-base-content/70 px-1">
                  <span>{formatTime(currentTime)}</span>
                  <span className="text-xs text-rose-400 font-sans font-semibold">
                    {detectedFrames.length > 0
                      ? `● ${detectedFrames.length} flagged moments marked in red`
                      : "No flagged intervals"}
                  </span>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>

              {/* Bottom Controls Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-base-200">
                <div className="flex items-center gap-2">
                  <button
                    onClick={togglePlayPause}
                    className="btn btn-circle btn-primary btn-sm"
                    title={isPlaying ? "Pause (Space)" : "Play (Space)"}
                  >
                    {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
                  </button>

                  <div className="flex items-center gap-1.5 ml-2">
                    <button
                      onClick={toggleMute}
                      className="btn btn-ghost btn-circle btn-sm"
                      title={isMuted ? "Unmute" : "Mute"}
                    >
                      {isMuted || volume === 0 ? (
                        <VolumeX className="w-4 h-4 text-rose-500" />
                      ) : (
                        <Volume2 className="w-4 h-4" />
                      )}
                    </button>
                    <input
                      type="range"
                      min={0}
                      max={1}
                      step={0.05}
                      value={isMuted ? 0 : volume}
                      onChange={handleVolumeChange}
                      className="range range-xs range-primary w-20"
                      title="Adjust volume"
                    />
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="dropdown dropdown-top dropdown-end">
                    <div
                      tabIndex={0}
                      role="button"
                      className="btn btn-xs btn-outline font-mono gap-1"
                    >
                      Speed: {playbackRate}x
                    </div>
                    <ul
                      tabIndex={0}
                      className="dropdown-content z-20 menu p-1 shadow-lg bg-base-200 rounded-box w-28 text-xs"
                    >
                      {[0.5, 0.75, 1.0, 1.25, 1.5, 2.0].map((rate) => (
                        <li key={rate}>
                          <button
                            onClick={() => handlePlaybackRateChange(rate)}
                            className={`py-1 ${playbackRate === rate ? "active font-bold" : ""}`}
                          >
                            {rate}x Speed
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <button
                    onClick={toggleFullscreen}
                    className="btn btn-ghost btn-circle btn-sm"
                    title={isFullscreen ? "Exit Fullscreen (F)" : "Fullscreen (F)"}
                  >
                    {isFullscreen ? (
                      <Minimize className="w-4 h-4" />
                    ) : (
                      <Maximize className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            <div className="text-xs text-base-content/60 flex items-center justify-between">
              <span>
                Viewing:{" "}
                <strong className="text-base-content">
                  {activeTab === "clip" && response.output_video
                    ? "Extracted Violent Sequence Clip"
                    : "Full Uploaded Source Video"}
                </strong>
              </span>
              <span className="font-mono text-primary font-semibold">{durationText}</span>
            </div>
          </div>

          {/* Chronological Detected Frames Gallery */}
          <div className="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-sm flex flex-col gap-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div>
                <h3 className="text-xl font-extrabold text-base-content flex items-center gap-2">
                  <Layers className="w-6 h-6 text-primary" />
                  Exact Detected Violent Frames
                </h3>
                <p className="text-xs text-base-content/70 mt-1">
                  Chronological keyframes flagged by the deep-learning model. Click any frame to seek the player to that timestamp.
                </p>
              </div>
              <span className="badge badge-primary badge-outline text-xs font-bold">
                {detectedFrames.length} Frames Identified
              </span>
            </div>

            {detectedFrames.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {detectedFrames.map((frame, index) => {
                  const exactTimestamp = formatExactTimestamp(frame.timestampSeconds, frame.timestamp);
                  const isActive =
                    activeFrameTime !== null &&
                    Math.abs(activeFrameTime - frame.timestampSeconds) < 0.5;

                  return (
                    <div
                      key={index}
                      onClick={() => handleSeekToFrame(frame.timestampSeconds)}
                      className={`group cursor-pointer rounded-2xl overflow-hidden border transition-all duration-200 bg-base-100 flex flex-col shadow-sm hover:shadow-xl hover:-translate-y-1 ${
                        isActive
                          ? "border-primary ring-2 ring-primary/40 shadow-primary/20 scale-[1.02]"
                          : "border-base-300 hover:border-primary/60"
                      }`}
                      title={`Click to jump video to ${exactTimestamp} (${frame.confidence}% Confidence)`}
                    >
                      {/* Image Thumbnail with Overlay */}
                      <div className="relative aspect-video bg-black overflow-hidden">
                        <img
                          src={frame.imageUrl}
                          alt={`Violent frame at ${exactTimestamp}`}
                          className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                          loading="lazy"
                        />
                        {/* Exact Timestamp badge: e.g. 00:00:05 */}
                        <div className="absolute top-2 left-2 bg-black/80 text-white text-[10px] font-mono px-2 py-0.5 rounded-md backdrop-blur-sm flex items-center gap-1 shadow-sm">
                          <Clock className="w-3 h-3 text-primary" />
                          {exactTimestamp}
                        </div>
                        {/* Play overlay icon on hover */}
                        <div className="absolute inset-0 bg-primary/20 opacity-0 group-hover:opacity-100 flex items-center justify-center transition no-print">
                          <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center shadow-lg">
                            <Play className="w-4 h-4 ml-0.5" />
                          </div>
                        </div>
                      </div>

                      {/* Card Meta */}
                      <div className="p-2.5 flex flex-col gap-1">
                        <div className="flex items-center justify-between">
                          <span
                            className="badge badge-xs font-semibold badge-error text-white"
                            title={`AI Confidence: ${frame.confidence}%`}
                          >
                            {frame.confidence}% Conf.
                          </span>
                          <span className="text-[10px] text-base-content/60 font-mono">
                            #{frame.frameIdx}
                          </span>
                        </div>
                        <div className="text-[11px] font-bold text-rose-400 truncate">
                          {frame.label}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-8 bg-base-100 rounded-2xl border border-base-300 text-center text-sm text-base-content/70">
                <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
                No violent frames detected in this video.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Fullscreen Image Preview Modal */}
      {isImageModalOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 cursor-pointer no-print"
          onClick={() => setIsImageModalOpen(false)}
        >
          <div className="relative max-w-5xl max-h-[90vh] flex flex-col items-center">
            <img
              src={imageSrc}
              alt="Full Preview"
              className="max-h-[85vh] max-w-full object-contain rounded-2xl shadow-2xl"
            />
            <div className="mt-3 text-white text-xs opacity-75">
              Click anywhere to close preview
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Result;
