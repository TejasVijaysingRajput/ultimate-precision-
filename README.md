# Ultimate Precision AI: Violence Detection and Surveillance System

![Next.js 15](https://img.shields.io/badge/Next.js-15.1.6-black?style=for-the-badge&logo=next.js)
![React 19](https://img.shields.io/badge/React-19-blue?style=for-the-badge&logo=react)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![Python 3.11](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-DaisyUI-38bdf8?style=for-the-badge&logo=tailwindcss)
![MongoDB](https://img.shields.io/badge/MongoDB-Mongoose-green?style=for-the-badge&logo=mongodb)

An advanced, end-to-end artificial intelligence video and image surveillance platform engineered for real-time violence detection, automated forensic threat classification, and incident report generation.

---

## 🚀 Key Features

- **Deep Learning Neural Classification**: Powered by a custom convolutional neural network (`violence_detection_model.h5`) evaluating video and image frames.
- **High-Capacity Media Uploads**: Supports surveillance video and high-resolution image uploads up to **1 GB** (`.mp4`, `.mov`, `.avi`, `.webm`, `.mkv`, `.jpg`, `.png`, `.webp`).
- **Interactive Custom Video Player**:
  - Precision scrub bar with real-time violence timestamp markers in high-contrast red.
  - Variable playback speed controls (0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x).
  - Audio mute/unmute and volume slider.
  - Native fullscreen and toggle play/pause overlays.
  - Instant switching between the full source video and the AI-extracted violent sequence clip.
- **Keyframe Evidence Gallery**: Chronologically displays all flagged violent frames with exact timestamps and individual model confidence scores. Click any keyframe thumbnail to jump the video directly to that second.
- **Multi-Format Forensic Dossier Export**:
  - **Print / PDF Dossier**: Formatted specifically for printable forensic custody documentation with clean monochrome layout.
  - **Text Summary Report (`.txt`)**: Structured ASCII incident logs for rapid reporting.
  - **Full Raw Data (`.json`)**: Complete payload containing frame coordinates, probabilities, and model parameters.
- **Record Lifecycle Management**: One-click deletion of reports and associated media from both the dashboard and history archive.
- **AI Surveillance Assistant**: An interactive conversational chatbot that guides security operators on system features, threat metrics, and forensic reporting.
- **Adaptive Cyber-Dark Theme**: Seamless theme toggler with a customized, professional surveillance UI palette.

---

## 🛠️ Technology Stack

- **Frontend & Fullstack Framework**: Next.js 15.1.6 (App Router), React 19, TypeScript
- **Styling**: Tailwind CSS, DaisyUI, Lucide React Icons
- **Backend APIs & Database**: Next.js Server Route Handlers, MongoDB, Mongoose
- **Deep Learning Engine**: Python 3.11, TensorFlow / Keras, OpenCV (`cv2`), NumPy, Pillow

---

## 📋 Prerequisites

Before running the application, make sure you have installed:
1. **Node.js** (v18 or higher, recommended v20+)
2. **Python** (v3.10 or v3.11)
3. **MongoDB** (running locally on `mongodb://127.0.0.1:27017` or a remote MongoDB Atlas URI)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/TejasVijaysingRajput/ultimate-precision-.git
cd ultimate-precision-
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Install Python AI Dependencies
Ensure Python 3.11 is installed and available in your environment:
```bash
pip install tensorflow opencv-python numpy pillow
```

### 4. Configure Environment Variables
Copy the example environment configuration:
```bash
cp .env.example .env
```
Ensure your `.env` contains:
```env
MONGO_URI=mongodb://localhost:27017/Ultimate_Pricision
PORT=3000
NODE_ENV=development
```

---

## 🚦 Running the Application

### Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build & Run
```bash
npm run build
npm run start
```

---

## 📁 Project Architecture

```
ultimate-precision/
├── public/                     # Static media and sample surveillance assets
│   ├── sample.mp4              # Demonstration test video
│   ├── sample.jpg              # Demonstration test image
│   └── uploads/                # Dynamic user upload storage
├── python/                     # AI Inference Scripts & Neural Models
│   ├── predict.py              # Video & frame violence classification engine
│   └── violence_detection_model.h5 # Pretrained neural network model
├── src/
│   ├── Components/             # Modular UI components (Navbar, Chatbot, ThemeToggler)
│   ├── app/
│   │   ├── (Home)/             # Public landing page
│   │   ├── api/                # Next.js API endpoints
│   │   │   ├── auth/           # Login and user registration
│   │   │   ├── detections/     # Querying and deleting detection records
│   │   │   ├── upload/         # Media upload & AI inference execution
│   │   │   └── user/stats/     # Dashboard metrics and threat analytics
│   │   ├── user/
│   │   │   ├── dashboard/      # Main upload, analysis, and result interface
│   │   │   └── history/        # Forensic incident archives
│   │   └── globals.css         # Custom surveillance CSS design tokens
│   ├── models/                 # Mongoose database models (User, Detection)
│   └── lib/                    # Shared utility helpers
├── .env.example                # Environment variable blueprint
├── package.json                # Project dependencies and run scripts
└── README.md                   # System documentation
```

---

## 🔒 Security & Privacy Notice
All uploads and model inferences process locally within your configured environment. Ensure appropriate administrative access controls when deploying surveillance forensic feeds to public networks.

---

## 📄 License
MIT License. Created for the **Ultimate Precision AI: Violence Detection and Surveillance System** project.
