from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def generate_chapter_4(styles, PageTarget, target_dir):
    story = []
    PRIMARY = colors.HexColor("#0f172a")
    SECONDARY = colors.HexColor("#1e3a8a")
    CARD_BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f8fafc")

    # =========================================================================
    # CHAPTER 4: SYSTEM DESIGN AND IMPLEMENTATION
    # =========================================================================
    story.append(PageTarget("ch4_start", target_dir))
    story.append(Paragraph("CHAPTER 4", styles['BBTitle24']))
    story.append(Paragraph("SYSTEM DESIGN AND IMPLEMENTATION", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=14))

    # 4.1 Tripartite Architectural Design
    story.append(PageTarget("ch4_1", target_dir))
    story.append(Paragraph("4.1 Full-Stack Tripartite System Architecture", styles['BBSectionHeader']))
    story.append(Paragraph(
        "To transform deep learning algorithms into a robust, enterprise-grade software product, <b>Ultimate Precision AI</b> "
        "is engineered around a high-performance <b>Tripartite Operational Architecture</b>. The system cleanly decouples concerns across "
        "three primary tiers: (1) an interactive <b>Next.js 15 Client Cockpit</b> running React 19, (2) an asynchronous <b>Next.js Server API Layer</b> "
        "handling multipart file ingest, database orchestration, and byte-range video streaming, and (3) a dedicated <b>Python 3.11 Subprocess AI Engine</b> "
        "executing OpenCV video demuxing, TensorFlow inference, and keyframe persistence.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 4.1 Box
    story.append(PageTarget("fig_4_1", target_dir))
    fig41_data = [
        [Paragraph("<b>Figure 4.1: Full-Stack Client-Server-AI Tripartite Operational Architecture</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   +-------------------------------------------------------------------------------------------------+\n"
            "   |                             CLIENT TIER: Next.js 15 / React 19 UI                               |\n"
            "   |  - Responsive Dashboard       - Interactive Forensic Video Player  - Exact Frames Gallery Grid   |\n"
            "   |  - Real-time Threat Gauges    - Sub-200ms Timestamp Seeking        - Certified PDF Export       |\n"
            "   +-------------------------------------------------------------------------------------------------+\n"
            "                 ^                                         ^                              |\n"
            "                 | HTTP 206 Partial Content Stream         | Multipart Upload / REST      | Next-Auth\n"
            "                 v                                         v                              v\n"
            "   +-------------------------------------------------------------------------------------------------+\n"
            "   |                             SERVER TIER: Next.js App Router (Node.js)                           |\n"
            "   |  - POST /api/upload (1GB Ingest)                      - GET /uploads/[...path] (Byte-Range Stream) |\n"
            "   |  - GET /api/user/stats (Analytical Metrics)           - POST /api/pdf/generate (ReportLab Dossier) |\n"
            "   +-------------------------------------------------------------------------------------------------+\n"
            "                 |                                         |                              |\n"
            "                 | Subprocess Child Spawn (stdio JSON)    | Mongoose ODM Drivers         | Local Storage\n"
            "                 v                                         v                              v\n"
            "   +-------------------------------+     +---------------------------------+     +-------------------+\n"
            "   |     AI INFERENCE ENGINE       |     |        DATABASE TIER            |     |   PHYSICAL DISK   |\n"
            "   | - Python 3.11 / TensorFlow    |     | - MongoDB 7.0+ Replica Set      |     | - public/uploads/ |\n"
            "   | - OpenCV Ingestion & Decoding |     | - Detection Document Collection |     |   * source.mp4    |\n"
            "   | - 32-Batch Vectorized Infer   |     | - User Accounts & Audit Trails  |     |   * frame_N.jpg   |\n"
            "   | - Keyframe Extractor & Stitch |     | - Indexed Query Indices         |     |   * highlight.mp4 |\n"
            "   +-------------------------------+     +---------------------------------+     +-------------------+",
            styles['BBCode']
        )]
    ]
    t_fig41 = Table(fig41_data, colWidths=[450])
    t_fig41.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig41)
    story.append(PageBreak())

    # 4.2 Full-Stack Next.js 15 Implementation
    story.append(PageTarget("ch4_2", target_dir))
    story.append(Paragraph("4.2 Full-Stack Next.js 15 Implementation (App Router, Server Actions)", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The application leverages <b>Next.js 15.1.6</b> with the App Router paradigm, capitalizing on React 19 Server Components "
        "and Server Actions. Unlike legacy single-page React apps or detached Express backends, Next.js provides hybrid rendering, "
        "streaming server responses, optimized bundle sizes, and native edge API routes within a unified TypeScript codebase. "
        "Key implementation pillars include:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "• <b>Server Components for Analytical Dashboards:</b> Statistical summary pages and detection audit logs are rendered on the server, "
        "fetching metrics directly from MongoDB without exposing database credentials to client browsers.<br/>"
        "• <b>Client Components for Dynamic Forensic Cockpits:</b> The video scrutiny interface (<code>[result]/page.tsx</code>) is compiled "
        "as an interactive client component utilizing React hooks (<code>useState</code>, <code>useRef</code>, <code>useEffect</code>) "
        "to manage HTML5 video playback, frame seeking, active tab switching, and toast notifications.<br/>"
        "• <b>Subprocess Orchestration via Node.js Child Process:</b> When a video is submitted, Next.js executes the Python engine via "
        "<code>child_process.spawn('python', ['python/run.py', uploadPath, uploadDir])</code>. Standard output streams (<code>stdout</code>) "
        "are captured, parsed into typed JSON objects, and stored directly to MongoDB.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 4.3 Database Architecture & MongoDB Schemas
    story.append(PageTarget("ch4_3", target_dir))
    story.append(Paragraph("4.3 Database Architecture & MongoDB Schemas", styles['BBSectionHeader']))
    story.append(Paragraph(
        "A robust document-oriented database architecture was engineered using <b>MongoDB 7.0+</b> and the <b>Mongoose 8.9.5</b> ODM "
        "(Object Data Modeling) library. MongoDB's flexible BSON document model is ideally suited for storing heterogeneous surveillance "
        "records, nested keyframe arrays, and variable-length incident clustering sequences without requiring expensive relational joins.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # 4.3.1 Detection Collection Schema
    story.append(PageTarget("ch4_3_1", target_dir))
    story.append(Paragraph("4.3.1 Detection Collection Schema & Keyframe Arrays", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "The primary entity in the database is the <code>Detection</code> model. Each detection document encapsulates full analytical "
        "metadata, file locations, overall classification status, confidence metrics, and an embedded array of detected violent frames. "
        "Table 4.2 details the schema structure and type definitions.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # Table 4.2
    story.append(PageTarget("tab_4_2", target_dir))
    story.append(Paragraph("<b>Table 4.2: MongoDB Detection Document Schema Field Definitions and Types</b>", styles['BBSubSectionHeader']))
    tab42_data = [
        [Paragraph("<b>Field Name</b>", styles['BBTableHeader']), Paragraph("<b>BSON Type</b>", styles['BBTableHeader']), Paragraph("<b>Indexing</b>", styles['BBTableHeader']), Paragraph("<b>Functional Description & Purpose</b>", styles['BBTableHeader'])],
        [Paragraph("_id", styles['BBTableCellBold']), Paragraph("ObjectId", styles['BBTableCell']), Paragraph("Primary Key", styles['BBTableCell']), Paragraph("Unique immutable database document identifier", styles['BBTableCell'])],
        [Paragraph("userEmail", styles['BBTableCellBold']), Paragraph("String", styles['BBTableCell']), Paragraph("Indexed", styles['BBTableCell']), Paragraph("Account identifier of security operator conducting analysis", styles['BBTableCell'])],
        [Paragraph("videoUrl", styles['BBTableCellBold']), Paragraph("String", styles['BBTableCell']), Paragraph("None", styles['BBTableCell']), Paragraph("Relative streaming route path to original uploaded video", styles['BBTableCell'])],
        [Paragraph("highlightUrl", styles['BBTableCellBold']), Paragraph("String", styles['BBTableCell']), Paragraph("None", styles['BBTableCell']), Paragraph("Relative streaming route path to stitched highlight MP4", styles['BBTableCell'])],
        [Paragraph("status", styles['BBTableCellBold']), Paragraph("String", styles['BBTableCell']), Paragraph("Indexed", styles['BBTableCell']), Paragraph("Categorical threat flag: 'VIOLENT' or 'NON-VIOLENT'", styles['BBTableCell'])],
        [Paragraph("confidence", styles['BBTableCellBold']), Paragraph("Number (Float)", styles['BBTableCell']), Paragraph("None", styles['BBTableCell']), Paragraph("Aggregated session violence probability score [0.0 - 1.0]", styles['BBTableCell'])],
        [Paragraph("detected_frames", styles['BBTableCellBold']), Paragraph("Array of Objects", styles['BBTableCell']), Paragraph("Embedded", styles['BBTableCell']), Paragraph("List of violent frames containing index, timestamp, and URL", styles['BBTableCell'])],
        [Paragraph("createdAt", styles['BBTableCellBold']), Paragraph("Date", styles['BBTableCell']), Paragraph("Descending", styles['BBTableCell']), Paragraph("System ingestion timestamp for historical timeline ordering", styles['BBTableCell'])],
    ]
    t42 = Table(tab42_data, colWidths=[90, 80, 70, 210])
    t42.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t42)
    story.append(PageBreak())

    # Figure 4.2 Box
    story.append(PageTarget("fig_4_2", target_dir))
    fig42_data = [
        [Paragraph("<b>Figure 4.2: MongoDB Entity-Relationship and Document Schema Hierarchy</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   [ User Account Document ]\n"
            "   ├── _id: ObjectId(\"...\")\n"
            "   ├── email: \"officer@security.mpstme.edu\"\n"
            "   ├── password: \"$2a$10$e8Z...\" (Bcrypt Hash)\n"
            "   ├── role: \"SUPERVISOR\"\n"
            "   └── createdAt: ISODate(\"2027-01-15T08:30:00Z\")\n"
            "          |\n"
            "          | 1 : N Relationship (userEmail)\n"
            "          v\n"
            "   [ Detection Document Collection ]\n"
            "   ├── _id: ObjectId(\"67b5c...\")\n"
            "   ├── userEmail: \"officer@security.mpstme.edu\"\n"
            "   ├── originalName: \"cctv_gate4_incident.mp4\"\n"
            "   ├── videoUrl: \"/uploads/174000123/original.mp4\"\n"
            "   ├── highlightUrl: \"/uploads/174000123/highlight.mp4\"\n"
            "   ├── status: \"VIOLENT\"\n"
            "   ├── confidence: 0.9418\n"
            "   ├── totalFrames: 1450\n"
            "   ├── fps: 30.0\n"
            "   └── detected_frames: [\n"
            "          { frame_index: 150, timestamp: \"00:00:05\", confidence: 0.942, url: \"/uploads/.../frame_150.jpg\" },\n"
            "          { frame_index: 174, timestamp: \"00:00:05\", confidence: 0.961, url: \"/uploads/.../frame_174.jpg\" },\n"
            "          { frame_index: 210, timestamp: \"00:00:07\", confidence: 0.915, url: \"/uploads/.../frame_210.jpg\" }\n"
            "       ]",
            styles['BBCode']
        )]
    ]
    t_fig42 = Table(fig42_data, colWidths=[450])
    t_fig42.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig42)
    story.append(Spacer(1, 12))

    # 4.3.2 User Authentication & Audit Trails
    story.append(PageTarget("ch4_3_2", target_dir))
    story.append(Paragraph("4.3.2 User Authentication & Audit Trails", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "To establish non-repudiation and chain-of-custody compliance for forensic evidence, all access is guarded by <b>NextAuth</b> "
        "and salted <b>Bcrypt password hashing</b>. Every analytical session permanently records the operator's identity, IP address, "
        "and timestamp, ensuring that surveillance assessments can be submitted as verifiable evidence in administrative or legal proceedings.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 4.4 High-Performance Backend API Endpoints
    story.append(PageTarget("ch4_4", target_dir))
    story.append(Paragraph("4.4 High-Performance Backend API Endpoints", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The server layer exposes a clean RESTful API designed for high-concurrency ingestion and rapid client interaction. "
        "Table 4.1 summarizes the core endpoints.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # Table 4.1
    story.append(PageTarget("tab_4_1", target_dir))
    story.append(Paragraph("<b>Table 4.1: RESTful API Endpoints Specification of Ultimate Precision AI</b>", styles['BBSubSectionHeader']))
    tab41_data = [
        [Paragraph("<b>HTTP Method & Route</b>", styles['BBTableHeader']), Paragraph("<b>Payload / Parameters</b>", styles['BBTableHeader']), Paragraph("<b>Response Format</b>", styles['BBTableHeader']), Paragraph("<b>Operational Functionality</b>", styles['BBTableHeader'])],
        [Paragraph("POST /api/upload", styles['BBTableCellBold']), Paragraph("multipart/form-data (video)", styles['BBTableCell']), Paragraph("JSON (Detection Object)", styles['BBTableCell']), Paragraph("Ingests video (up to 1GB), spawns AI inference, saves results", styles['BBTableCell'])],
        [Paragraph("GET /uploads/[...path]", styles['BBTableCellBold']), Paragraph("Range Header (bytes=start-end)", styles['BBTableCell']), Paragraph("Binary (HTTP 206 / 200)", styles['BBTableCell']), Paragraph("Byte-range video streaming & instant frame thumbnail delivery", styles['BBTableCell'])],
        [Paragraph("GET /api/user/stats", styles['BBTableCellBold']), Paragraph("Session Cookie", styles['BBTableCell']), Paragraph("JSON (Analytics)", styles['BBTableCell']), Paragraph("Calculates user scan counts, violence rates, and trends", styles['BBTableCell'])],
        [Paragraph("POST /api/pdf/generate", styles['BBTableCellBold']), Paragraph("JSON (Detection ID)", styles['BBTableCell']), Paragraph("application/pdf", styles['BBTableCell']), Paragraph("Generates certified forensic PDF dossier using ReportLab", styles['BBTableCell'])],
    ]
    t41 = Table(tab41_data, colWidths=[120, 110, 100, 120])
    t41.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t41)
    story.append(PageBreak())

    # 4.4.2 Dynamic HTTP 206 Streaming Route
    story.append(PageTarget("ch4_4_2", target_dir))
    story.append(Paragraph("4.4.2 Dynamic HTTP 206 Byte-Range Video Streaming Route", styles['BBSectionHeader']))
    story.append(Paragraph(
        "A critical engineering obstacle encountered when deploying Next.js in production (<code>next start</code>) is that files "
        "written to the physical <code>public/uploads</code> directory after application build time are not served dynamically by default. "
        "Furthermore, modern HTML5 <code>&lt;video&gt;</code> elements require support for <b>HTTP 206 Partial Content byte-range negotiation</b> "
        "to allow users to scrub forward and backward along the playback scrubber without downloading the entire video file.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "To decisively solve both issues, we implemented a dedicated catch-all dynamic route handler: "
        "<code>src/app/uploads/[...path]/route.ts</code>. When the client browser issues a video streaming request, the handler operates as follows:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "1. <b>Path Normalization & Sanitization:</b> The URL segments are normalized and resolved against <code>process.cwd()/public/uploads</code>, "
        "strictly guarding against directory traversal attacks.<br/>"
        "2. <b>Range Header Parsing:</b> If the browser provides a <code>Range: bytes=start-end</code> header, the server parses the byte offsets. "
        "A chunk size of 1MB ($1,048,576$ bytes) is calculated dynamically.<br/>"
        "3. <b>Targeted File Slicing:</b> A Node.js read stream is opened using <code>fs.createReadStream(filePath, { start, end })</code>, "
        "reading only the requested byte chunk from physical storage.<br/>"
        "4. <b>HTTP 206 Header Assembly:</b> The server returns an HTTP 206 status code with headers:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Content-Range: bytes {start}-{end}/{fileSize}</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Accept-Ranges: bytes</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Content-Length: {chunkSize}</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Content-Type: video/mp4</code><br/>"
        "5. <b>Static Fallback for Thumbnails:</b> Non-video files (such as JPEG keyframe thumbnails) are served with standard HTTP 200 headers "
        "and aggressive client-side caching directives (<code>public, max-age=31536000, immutable</code>).",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 4.3 Box
    story.append(PageTarget("fig_4_3", target_dir))
    fig43_data = [
        [Paragraph("<b>Figure 4.3: Dynamic HTTP 206 Partial Content Video Scrubbing Negotiation Protocol</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   Client Browser (HTML5 Video Player)                 Next.js Streaming Handler (/uploads/[...path])\n"
            "         |                                                                   |\n"
            "         | ---- GET /uploads/session/original.mp4 (Range: bytes=0-) -------->|\n"
            "         |<---- HTTP 206 Partial Content (Content-Range: bytes 0-1048575/Total) --| (Loads Initial 1MB)\n"
            "         |\n"
            "   [ User Clicks Violent Frame at Timestamp 00:00:15 ]\n"
            "         |\n"
            "         | ---- GET /uploads/session/original.mp4 (Range: bytes=15728640-) ->|\n"
            "         |<---- HTTP 206 Partial Content (Content-Range: bytes 15.7M-16.7M) -| (Instant Seek in <150ms!)\n"
            "         |\n"
            "   [ Smooth Instantaneous Video Playback Continues without Waiting for Full File Download ]",
            styles['BBCode']
        )]
    ]
    t_fig43 = Table(fig43_data, colWidths=[450])
    t_fig43.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig43)
    story.append(PageBreak())

    # 4.5 Forensic Cockpit UI & Exact Detected Violent Frames Feature
    story.append(PageTarget("ch4_5", target_dir))
    story.append(Paragraph("4.5 Forensic Cockpit UI & Exact Detected Violent Frames Feature", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The client-side user experience is anchored by the <b>Forensic Scrutiny Cockpit</b> implemented in "
        "<code>src/app/user/dashboard/[result]/page.tsx</code>. This component delivers an evidentiary workspace tailored for rapid "
        "threat verification by security personnel.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # 4.5.1 Exact Frame Gallery Component
    story.append(PageTarget("ch4_5_1", target_dir))
    story.append(Paragraph("4.5.1 Exact Frame Gallery Component with Interactive Video Seek", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "A central requirement of the system is the <b>Exact Detected Violent Frames</b> feature. Unlike conventional systems that "
        "merely show static summary text, our cockpit renders a responsive grid gallery (adapting from 2 columns on mobile devices to "
        "6 columns on high-resolution monitors) displaying genuine extracted keyframe thumbnails. Each thumbnail card features:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "• <b>Timestamp Pill:</b> An overlay badge displaying the exact time formatted as <code>00:00:05</code> with a clock icon.<br/>"
        "• <b>Confidence Metric:</b> An emerald badge showing the model's exact classification confidence (e.g. <code>94.2% Violent</code>).<br/>"
        "• <b>Interactive Timeline Seeking:</b> Clicking any frame card triggers the <code>handleSeekToFrame(timestamp_sec)</code> handler. "
        "The handler automatically switches the video tab from 'Highlight' to 'Original Video', sets the HTML5 video element's "
        "<code>currentTime = timestamp_sec</code>, initiates playback, and scrolls the video player into viewport focus.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # 4.5.3 Empty State
    story.append(PageTarget("ch4_5_3", target_dir))
    story.append(Paragraph("4.5.3 Empty State & Zero-Violence Handling", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "If the uploaded video is evaluated as benign and contains no frames exceeding the threshold ($\\theta_{conf} \\ge 0.50$), "
        "the gallery gracefully renders an affirmative verified empty-state container: "
        "<i>“No violent frames detected in this video. The footage appears entirely non-violent and secure.”</i> with a green security shield icon, "
        "preventing user confusion.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 4.4 Box
    story.append(PageTarget("fig_4_4", target_dir))
    fig44_data = [
        [Paragraph("<b>Figure 4.4: Forensic Cockpit UI: Responsive Gallery with Instant Timestamp Seeking</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   +-------------------------------------------------------------------------------------------------+\n"
            "   |  [< Back to Dashboard]      CCTV Incident Forensic Cockpit: Gate_4_East.mp4    [Export PDF]      |\n"
            "   +-------------------------------------------------------------------------------------------------+\n"
            "   |  +---------------------------------------+  +------------------------------------------------+  |\n"
            "   |  |        HTML5 FORENSIC VIDEO PLAYER    |  |               THREAT SUMMARY MATRIX            |  |\n"
            "   |  |   [ Original Video ] [ Highlight ]    |  |  Status: [ VIOLENT DETECTED ] (Red Badge)      |  |\n"
            "   |  |                                       |  |  Confidence Score: 94.2%                       |  |\n"
            "   |  |      >> Playing at: 00:00:05 <<       |  |  Duration: 48.0s | Processed Frames: 1,440     |  |\n"
            "   |  +---------------------------------------+  +------------------------------------------------+  |\n"
            "   |  =============================================================================================  |\n"
            "   |  EXACT DETECTED VIOLENT FRAMES (Keyframe Evidentiary Verification Gallery)                      |\n"
            "   |  +-------------------+  +-------------------+  +-------------------+  +-------------------+     |\n"
            "   |  | [ Frame Image 1 ] |  | [ Frame Image 2 ] |  | [ Frame Image 3 ] |  | [ Frame Image 4 ] | ... |\n"
            "   |  | Clock: 00:00:05   |  | Clock: 00:00:05   |  | Clock: 00:00:07   |  | Clock: 00:00:08   |     |\n"
            "   |  | Conf: 94.2%       |  | Conf: 96.1%       |  | Conf: 91.5%       |  | Conf: 88.7%       |     |\n"
            "   |  | (Click to Seek)   |  | (Click to Seek)   |  | (Click to Seek)   |  | (Click to Seek)   |     |\n"
            "   |  +-------------------+  +-------------------+  +-------------------+  +-------------------+     |\n"
            "   +-------------------------------------------------------------------------------------------------+",
            styles['BBCode']
        )]
    ]
    t_fig44 = Table(fig44_data, colWidths=[450])
    t_fig44.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig44)
    story.append(PageBreak())

    # 4.6 Forensic Report Generation Engine
    story.append(PageTarget("ch4_6", target_dir))
    story.append(Paragraph("4.6 Forensic Report Generation Engine (Automated Dossier Export)", styles['BBSectionHeader']))
    story.append(Paragraph(
        "In enterprise surveillance, visual detections must often be transmitted to legal authorities, police departments, or "
        "university disciplinary boards. To eliminate manual report writing, our system embeds an automated PDF dossier generator "
        "powered by ReportLab. Upon clicking 'Export Forensic PDF', the system compiles a multi-page evidentiary report containing "
        "case identifiers, analytical metadata, embedded high-resolution keyframe images with timestamps, and digital certification signatures.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 4.7 Security Architecture & Sanitization
    story.append(PageTarget("ch4_7", target_dir))
    story.append(Paragraph("4.7 Security Architecture, Input Sanitization, and Error Boundaries", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The architecture implements multi-tier defensive controls to protect against common web vulnerabilities:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "• <b>MIME-Type & Magic Byte Validation:</b> Uploaded files are inspected for valid video magic bytes (e.g., <code>ftypisom</code>), "
        "rejecting disguised executable payloads.<br/>"
        "• <b>Path Sanitization:</b> File paths passed to disk I/O routines are strictly sanitized using <code>path.normalize()</code>, "
        "preventing directory traversal attacks (<code>../</code>).<br/>"
        "• <b>React Error Boundaries:</b> Client components are wrapped in Error Boundaries and React Suspense fallbacks, ensuring "
        "that individual media decode failures do not crash the primary operational dashboard.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    return story
