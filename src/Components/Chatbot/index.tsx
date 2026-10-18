"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  MessageSquare,
  X,
  Send,
  Sparkles,
  Bot,
  User,
  HelpCircle,
  FileText,
  UploadCloud,
  ShieldAlert,
  ChevronDown,
  Minimize2,
  Maximize2,
} from "lucide-react";

interface Message {
  id: string;
  sender: "bot" | "user";
  text: string;
  timestamp: string;
}

const INITIAL_PROMPTS = [
  "🚀 How do I upload a video or image?",
  "🔍 What do violence % and confidence mean?",
  "⏱️ How to jump to exact violent frames?",
  "📄 How do I download or print a report?",
  "📦 What are the supported formats & 1GB limit?",
];

const KNOWLEDGE_BASE: Record<string, string> = {
  upload: `### 🚀 Uploading Footage for Detection:
1. Navigate to the **Dashboard** from the sidebar.
2. Drag and drop any video or image into the upload dropzone, or click **browse**.
3. You can preview your media directly inside the dropzone before processing.
4. Click **Start AI Detection**. The deep-learning neural network will analyze each frame and redirect you to the comprehensive incident report once ready!`,

  confidence: `### 🔍 Understanding Detection Metrics:
- **Violence Score (%)**: Represents the percentage of examined frames that exceeded the violence threshold.
- **Model Confidence (%)**: The statistical probability calculated by the convolutional neural network (\`violence_detection_model.h5\`).
- **Classification Verdict**: 
  - **Violent**: Altercation, physical aggression, or violent movement identified.
  - **Safe / Non-Violent**: Normal, peaceful activity verified across all frames.`,

  frames: `### ⏱️ Seeking to Exact Violent Moments:
1. In the **Incident Detection Report**, scroll to the **"Exact Detected Violent Frames"** gallery.
2. Every flagged frame is displayed with its exact timestamp (e.g., \`00:03\`), frame index, and confidence score.
3. **Click any frame thumbnail** — the video player will immediately jump to that timestamp and start playing so you can inspect that exact moment!
4. The timeline seek bar also shows red highlight markers for all violent intervals.`,

  download: `### 📄 Downloading & Exporting Incident Reports:
1. Open any detection report from the Dashboard or History.
2. Click the **"Download Report"** button in the top action bar.
3. You can choose:
   - **Print / Save as PDF**: Opens a pre-formatted forensic incident dossier suitable for official documentation.
   - **Export JSON**: Downloads full machine-readable detection data including all timestamp intervals.
   - **Download Summary (TXT)**: Downloads a clean plain-text incident summary.`,

  formats: `### 📦 Supported Formats & File Limits:
- **File Size**: Uploads of up to **1GB (1024 MB)** are supported!
- **Video Formats**: MP4, MOV, AVI, WEBM, MKV.
- **Image Formats**: JPG, JPEG, PNG, WEBP, BMP.
- All uploads are securely stored in the database archive and accessible anytime from your **History** tab.`,
};

export default function SurveillanceChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      sender: "bot",
      text: "👋 **Welcome to Ultimate Precision AI!**\n\nI am your surveillance assistant. I can help you with video/image analysis (up to 1GB), frame-by-frame timestamps, and forensic report downloads. How can I assist you today?",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const generateAnswer = (userQuery: string): string => {
    const q = userQuery.toLowerCase();
    if (q.includes("upload") || q.includes("start") || q.includes("how to use") || q.includes("drag")) {
      return KNOWLEDGE_BASE.upload;
    }
    if (q.includes("confidence") || q.includes("score") || q.includes("percentage") || q.includes("verdict") || q.includes("accuracy")) {
      return KNOWLEDGE_BASE.confidence;
    }
    if (q.includes("frame") || q.includes("timestamp") || q.includes("seek") || q.includes("jump") || q.includes("moment")) {
      return KNOWLEDGE_BASE.frames;
    }
    if (q.includes("download") || q.includes("pdf") || q.includes("report") || q.includes("print") || q.includes("export")) {
      return KNOWLEDGE_BASE.download;
    }
    if (q.includes("size") || q.includes("limit") || q.includes("format") || q.includes("1gb") || q.includes("image") || q.includes("video")) {
      return KNOWLEDGE_BASE.formats;
    }
    if (q.includes("history") || q.includes("delete") || q.includes("archive")) {
      return `### 📁 Detection History & Archive:
Visit the **History** tab from the left sidebar to review all past analyses. You can:
- Click the **Media Thumbnail** to open a quick video/image preview modal.
- Click **Report** to open the full interactive report with frame scrubber.
- Click the **Trash icon** to permanently delete records and associated files.`;
    }
    if (q.includes("theme") || q.includes("dark") || q.includes("light")) {
      return `### 🎨 Theme Customization:
Click the **Sun / Moon icon** in the top navigation bar to toggle between **Sleek Cyber Dark (Night)** and **Executive Light (Corporate)** modes. Your preference is saved automatically!`;
    }
    return `### 🤖 Ultimate Precision AI Assistant:
I understand you are asking about *"__${userQuery}__"*. 

Here are the key system features:
- **Footage Uploads**: Support for video and image files up to **1GB**.
- **Frame-by-Frame AI**: Identifies exact timestamps of violent incidents with real model confidence.
- **Interactive Player**: Scrub timeline, adjust speed (0.5x–2x), and click thumbnails to jump to moments.
- **Forensic Reports**: Print/Save as PDF or export raw data.

Try selecting one of the suggested quick prompts below, or feel free to rephrase your question!`;
  };

  const handleSend = (textToSend?: string) => {
    const query = textToSend || input.trim();
    if (!query) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    setTimeout(() => {
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: generateAnswer(query),
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botResponse]);
      setIsTyping(false);
    }, 450);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <div className="fixed bottom-6 right-6 z-40 no-print">
        {!isOpen && (
          <button
            onClick={() => setIsOpen(true)}
            className="btn btn-primary shadow-2xl rounded-full px-5 py-3 gap-2.5 hover:scale-105 transition-all duration-300 border border-primary/40 flex items-center group"
            aria-label="Open AI Surveillance Assistant"
          >
            <div className="relative">
              <Bot className="w-5 h-5 text-white" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full" />
            </div>
            <span className="font-bold text-sm tracking-wide text-white">AI Assistant</span>
          </button>
        )}
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[92vw] sm:w-[420px] h-[580px] max-h-[85vh] bg-base-100 border border-base-300 rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-200 no-print">
          {/* Header */}
          <div className="bg-base-200 px-5 py-4 border-b border-base-300 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-primary/20 text-primary flex items-center justify-center border border-primary/30">
                <Bot className="w-6 h-6" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-base-content flex items-center gap-2">
                  Surveillance AI Assistant
                  <span className="badge badge-xs badge-success gap-1 text-[10px] text-white">Online</span>
                </h4>
                <p className="text-[11px] text-base-content/60">Ultimate Precision System Guide</p>
              </div>
            </div>

            <button
              onClick={() => setIsOpen(false)}
              className="btn btn-ghost btn-circle btn-sm text-base-content/70 hover:text-base-content"
              aria-label="Close Chat"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-2.5 ${msg.sender === "user" ? "flex-row-reverse" : "flex-row"}`}
              >
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs shrink-0 mt-0.5 ${
                    msg.sender === "user"
                      ? "bg-primary text-white"
                      : "bg-base-300 text-primary border border-base-content/10"
                  }`}
                >
                  {msg.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                <div className={`flex flex-col max-w-[82%] ${msg.sender === "user" ? "items-end" : "items-start"}`}>
                  <div
                    className={`px-4 py-2.5 rounded-2xl text-xs leading-relaxed ${
                      msg.sender === "user"
                        ? "bg-primary text-white rounded-tr-none font-medium shadow-sm"
                        : "bg-base-200 text-base-content rounded-tl-none border border-base-300 shadow-sm"
                    }`}
                  >
                    <div className="whitespace-pre-line space-y-1.5">{msg.text}</div>
                  </div>
                  <span className="text-[10px] text-base-content/50 mt-1 px-1">{msg.timestamp}</span>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex items-center gap-2 text-xs text-base-content/60 py-1 px-2">
                <Bot className="w-4 h-4 text-primary animate-bounce" />
                <span>AI Assistant is analyzing...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompt Chips */}
          <div className="px-4 py-2 border-t border-base-300/60 bg-base-200/50 flex gap-1.5 overflow-x-auto scrollbar-none">
            {INITIAL_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(prompt)}
                className="btn btn-xs btn-outline rounded-full text-[10px] font-normal whitespace-nowrap hover:btn-primary"
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Input Footer */}
          <div className="p-3 bg-base-200 border-t border-base-300 flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about surveillance AI, uploads, or reports..."
              className="input input-sm input-bordered w-full rounded-xl bg-base-100 text-xs focus:border-primary focus:outline-none"
            />
            <button
              onClick={() => handleSend()}
              disabled={!input.trim()}
              className="btn btn-primary btn-sm btn-circle shrink-0"
              aria-label="Send message"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
