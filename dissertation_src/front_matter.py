import os
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def generate_front_matter(styles, page_lookup, PageTarget, target_dir):
    """
    Generates all front matter pages:
    - Cover page (Physical Page 1)
    - Inner Title page (Physical Page 2)
    - Certificate (Physical Page 3 / Roman Page i)
    - Candidate's Declaration (Physical Page 4 / Roman Page ii)
    - Approval Sheet (Physical Page 5 / Roman Page iii)
    - Acknowledgement (Physical Page 6 / Roman Page iv)
    - Abstract (Physical Page 7 / Roman Page v)
    - Table of Contents (Physical Pages 8-10 / Roman Pages vi-viii)
    - List of Figures (Physical Page 11 / Roman Page ix)
    - List of Tables (Physical Page 12 / Roman Page x)
    - List of Abbreviations (Physical Page 13 / Roman Page xi)
    """
    story = []

    PRIMARY = colors.HexColor("#0f172a")
    SECONDARY = colors.HexColor("#1e3a8a")
    CARD_BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f8fafc")

    def get_p(key, default="--"):
        if page_lookup and key in page_lookup:
            return str(page_lookup[key])
        return default

    # =========================================================================
    # PAGE 1: EXTERNAL COVER PAGE
    # =========================================================================
    story.append(PageTarget("cover_page", target_dir))
    story.append(Spacer(1, 20))
    story.append(Paragraph("ULTIMATE PRECISION AI: AUTOMATED VIDEO SURVEILLANCE & VIOLENCE DETECTION SYSTEM", styles['BBTitle24']))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "Submitted in partial fulfillment of the requirement for the award of Degree of<br/>"
        "<b>Bachelor of Technology in Computer Engineering</b>",
        styles['BBSubtitle14']
    ))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Submitted To:</b>", styles['BBCenter12']))
    story.append(Paragraph(
        "<b>SVKM’s NMIMS</b><br/>"
        "<b>Mukesh Patel School of Technology Management & Engineering</b><br/>"
        "Shirpur Campus (M.H.), India",
        styles['BBCenter14Bold']
    ))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Submitted By:</b>", styles['BBCenter12']))
    story.append(Paragraph(
        "<b>TEJAS VIJAYSING RAJPUT</b><br/>"
        "Enrollment No: <b>70012021045</b>",
        styles['BBCenter14Bold']
    ))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Under The Supervision Of:</b>", styles['BBCenter12']))
    story.append(Paragraph(
        "<b>Prof. / Dr. Internal Project Mentor</b><br/>"
        "Assistant Professor, Department of Computer Engineering",
        styles['BBCenter14Bold']
    ))
    story.append(Spacer(1, 35))

    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER ENGINEERING</b>", styles['BBCenter14Bold']))
    story.append(Paragraph("Mukesh Patel School of Technology Management & Engineering, Shirpur", styles['BBCenter12']))
    story.append(Paragraph("<b>ACADEMIC SESSION: 2026-27</b>", styles['BBCenter14Bold']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: INNER TITLE PAGE
    # =========================================================================
    story.append(PageTarget("inner_title_page", target_dir))
    story.append(Spacer(1, 20))
    story.append(Paragraph("ULTIMATE PRECISION AI: AUTOMATED VIDEO SURVEILLANCE & VIOLENCE DETECTION SYSTEM", styles['BBTitle24']))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "A Capstone Project Dissertation Submitted in Partial Fulfillment of the Requirements<br/>"
        "for the Degree of<br/>"
        "<b>BACHELOR OF TECHNOLOGY</b><br/>"
        "IN<br/>"
        "<b>COMPUTER ENGINEERING</b>",
        styles['BBSubtitle14']
    ))
    story.append(Spacer(1, 25))

    story.append(Paragraph("By", styles['BBCenter12']))
    story.append(Paragraph("<b>TEJAS VIJAYSING RAJPUT</b><br/>(Enrollment No: 70012021045)", styles['BBCenter14Bold']))
    story.append(Spacer(1, 25))

    story.append(Paragraph("Under the Guidance of", styles['BBCenter12']))
    story.append(Paragraph("<b>Internal Project Mentor</b><br/>Department of Computer Engineering", styles['BBCenter14Bold']))
    story.append(Spacer(1, 35))

    story.append(Paragraph(
        "<b>DEPARTMENT OF COMPUTER ENGINEERING</b><br/>"
        "<b>MUKESH PATEL SCHOOL OF TECHNOLOGY MANAGEMENT & ENGINEERING</b><br/>"
        "SVKM’s NMIMS (Deemed-to-be University)<br/>"
        "Shirpur Campus, Dist. Dhule, Maharashtra – 425405, India<br/>"
        "<b>MAY 2027</b>",
        styles['BBCenter12']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CERTIFICATE (Page i)
    # =========================================================================
    story.append(PageTarget("certificate_page", target_dir))
    story.append(Paragraph("CERTIFICATE", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=15))

    cert_text = (
        "This is to certify that the Capstone Project report entitled <b>“Ultimate Precision AI: Automated Video Surveillance "
        "& Violence Detection System”</b> has been successfully carried out by <b>Tejas Vijaysing Rajput</b> (Roll No. / Enrollment "
        "No: <b>70012021045</b>) under my guidance and supervision.<br/><br/>"
        "This work is submitted in partial fulfillment of the requirements for the award of the degree of <b>Bachelor of "
        "Technology in Computer Engineering</b> of Mukesh Patel School of Technology Management & Engineering (MPSTME), "
        "SVKM’s NMIMS (Deemed-to-be University), Mumbai / Shirpur Campus (M.H.), India, during the academic session 2026-2027.<br/><br/>"
        "To the best of our knowledge, the matter embodied in this Capstone Project report has not been submitted to any other "
        "University or Institute for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text, styles['BBBodyIndent']))
    story.append(Spacer(1, 40))

    cert_table_data = [
        [
            Paragraph("____________________________<br/><b>Internal Project Mentor</b><br/>Project Mentor & Supervisor<br/>Dept. of Computer Engineering", styles['BBTableCell']),
            Paragraph("____________________________<br/><b>External Examiner</b><br/>Subject Matter Expert<br/>Industry / Academic Nominee", styles['BBTableCell']),
        ],
        [
            Paragraph("<br/><br/><b>Date:</b> ______________<br/><b>Place:</b> Shirpur", styles['BBTableCell']),
            Paragraph("<br/><br/>____________________________<br/><b>Dr. Suresh Kurumbanshi</b><br/>Head of Department (H.O.D.)<br/>Dept. of Computer Engineering", styles['BBTableCell']),
        ]
    ]
    cert_table = Table(cert_table_data, colWidths=[225, 225])
    cert_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(cert_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CANDIDATE'S DECLARATION (Page ii)
    # =========================================================================
    story.append(PageTarget("declaration_page", target_dir))
    story.append(Paragraph("CANDIDATE’S DECLARATION", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=15))

    decl_text = (
        "I hereby declare that the work presented in this Capstone Project Dissertation entitled <b>“Ultimate Precision AI: "
        "Automated Video Surveillance & Violence Detection System”</b> is an authentic record of my own research and engineering "
        "work carried out under the supervision of my Project Mentor, Department of Computer Engineering, Mukesh Patel School of "
        "Technology Management & Engineering (MPSTME), SVKM’s NMIMS Shirpur.<br/><br/>"
        "I have not submitted the matter embodied in this report for the award of any other degree or diploma to any other institute "
        "or university. All figures, algorithms, statistical data, and findings presented herein are based on genuine model execution, "
        "empirical benchmarking, and architectural prototyping conducted within the campus laboratory environments.<br/><br/>"
        "Wherever information has been derived from other research publications, conference proceedings, or open-source software "
        "repositories, full acknowledgment has been explicitly provided in the text and referenced in the exhaustive bibliography."
    )
    story.append(Paragraph(decl_text, styles['BBBodyIndent']))
    story.append(Spacer(1, 50))

    story.append(Paragraph(
        "<b>Date:</b> ______________<br/>"
        "<b>Place:</b> Shirpur, Maharashtra<br/><br/><br/>"
        "____________________________________<br/>"
        "<b>TEJAS VIJAYSING RAJPUT</b><br/>"
        "Enrollment No: 70012021045<br/>"
        "B.Tech Computer Engineering (Final Year)<br/>"
        "MPSTME, SVKM’s NMIMS Shirpur Campus",
        styles['BBBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: APPROVAL SHEET / EVALUATION COMMITTEE (Page iii)
    # =========================================================================
    story.append(PageTarget("approval_page", target_dir))
    story.append(Paragraph("EVALUATION COMMITTEE APPROVAL SHEET", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=15))

    appr_text = (
        "The Capstone Project Report entitled <b>“Ultimate Precision AI: Automated Video Surveillance & Violence Detection System”</b> "
        "authored by <b>Tejas Vijaysing Rajput</b> (Enrollment No. <b>70012021045</b>) is hereby evaluated, approved, and accepted in "
        "partial fulfillment of the requirements for the award of the degree of <b>Bachelor of Technology in Computer Engineering</b>.<br/><br/>"
        "The defense examination and technical demonstration of the software artifact, algorithmic pipeline, and high-throughput "
        "video analytics framework were conducted on the specified date before the undersigned Board of Examiners."
    )
    story.append(Paragraph(appr_text, styles['BBBodyIndent']))
    story.append(Spacer(1, 35))

    board_data = [
        [Paragraph("<b>Role / Designation</b>", styles['BBTableHeader']), Paragraph("<b>Name of Examiner</b>", styles['BBTableHeader']), Paragraph("<b>Signature & Date</b>", styles['BBTableHeader'])],
        [Paragraph("Internal Guide & Supervisor", styles['BBTableCellBold']), Paragraph("Prof. / Dr. Internal Mentor", styles['BBTableCell']), Paragraph("_______________________", styles['BBTableCell'])],
        [Paragraph("External Examiner (Subject Expert)", styles['BBTableCellBold']), Paragraph("____________________________", styles['BBTableCell']), Paragraph("_______________________", styles['BBTableCell'])],
        [Paragraph("Capstone Project Coordinator", styles['BBTableCellBold']), Paragraph("Dr. Durgesh M. Sharma", styles['BBTableCell']), Paragraph("_______________________", styles['BBTableCell'])],
        [Paragraph("Head of Department (HoD)", styles['BBTableCellBold']), Paragraph("Dr. Suresh Kurumbanshi", styles['BBTableCell']), Paragraph("_______________________", styles['BBTableCell'])],
        [Paragraph("Associate Dean", styles['BBTableCellBold']), Paragraph("Dr. Venkatadri Marriboyina", styles['BBTableCell']), Paragraph("_______________________", styles['BBTableCell'])],
    ]
    board_table = Table(board_data, colWidths=[150, 160, 140])
    board_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(board_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ACKNOWLEDGEMENT (Page iv)
    # =========================================================================
    story.append(PageTarget("ack_page", target_dir))
    story.append(Paragraph("ACKNOWLEDGEMENT", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=15))

    ack_text1 = (
        "I would like to express my profound gratitude and indebtedness to my Project Guide and Supervisor, "
        "Department of Computer Engineering, SVKM’S NMIMS, Mukesh Patel School of Technology Management & Engineering "
        "(MPSTME), Shirpur Campus (M.H.), whose constant encouragement, constructive criticism, and technical insights "
        "guided this project from inception to realization. Their patience, availability, and deep expertise in computer "
        "vision and distributed software systems have benefited me beyond expression."
    )
    story.append(Paragraph(ack_text1, styles['BBBodyIndent']))

    ack_text2 = (
        "I express my sincere thanks and deepest gratitude to <b>Dr. Suresh Kurumbanshi</b>, Head of Department, "
        "Department of Computer Engineering, MPSTME Shirpur Campus, for providing state-of-the-art laboratory facilities, "
        "computational infrastructure, and academic support throughout the duration of this Capstone Project."
    )
    story.append(Paragraph(ack_text2, styles['BBBodyIndent']))

    ack_text3 = (
        "I also extend my heartfelt gratitude to <b>Dr. Venkatadri Marriboyina</b>, Associate Dean, MPSTME Shirpur Campus, "
        "for fostering an intellectual environment that prioritizes research excellence and practical innovation."
    )
    story.append(Paragraph(ack_text3, styles['BBBodyIndent']))

    ack_text4 = (
        "A special mention of gratitude goes to our Capstone Project Coordinator, <b>Dr. Durgesh M. Sharma</b>, "
        "Assistant Professor, Department of Computer Engineering, who maintained rigorous progress milestones, provided "
        "systematic rubrics, and guided the formal structure of this Black Book report."
    )
    story.append(Paragraph(ack_text4, styles['BBBodyIndent']))

    ack_text5 = (
        "Finally, I am indebted to all faculty members of the Computer Engineering department, my peers, and my family "
        "whose unwavering moral support and encouragement enabled the successful completion of this degree."
    )
    story.append(Paragraph(ack_text5, styles['BBBodyIndent']))
    story.append(Spacer(1, 30))

    story.append(Paragraph(
        "<b>Tejas Vijaysing Rajput</b><br/>"
        "Enrollment No: 70012021045<br/>"
        "Department of Computer Engineering, MPSTME Shirpur",
        styles['BBBody']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: ABSTRACT (Page v)
    # =========================================================================
    story.append(PageTarget("abstract_page", target_dir))
    story.append(Paragraph("ABSTRACT", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=15))

    abstract_p1 = (
        "Closed-Circuit Television (CCTV) cameras deployed across modern municipal infrastructure, transit hubs, and private "
        "establishments generate astronomical quantities of continuous video surveillance data. However, over 99% of contemporary "
        "surveillance systems operate purely in a reactive capacity, serving merely as post-incident forensic archives rather "
        "than proactive public safety intervention tools. Human security operators monitoring multiple concurrent video feeds suffer "
        "from rapid cognitive fatigue, missing up to 95% of subtle or brief physical security breaches after only twenty minutes of "
        "continuous observation. While recent deep learning research has explored computer vision models for automated violence detection, "
        "existing solutions remain predominantly theoretical benchmarks characterized by prohibitive inference latency, heavy GPU "
        "dependencies, black-box predictions lacking granular evidence, and complete disconnection from operational web cockpits."
    )
    story.append(Paragraph(abstract_p1, styles['BBBodyIndent']))

    abstract_p2 = (
        "To decisively overcome these fundamental bottlenecks, this Capstone Project presents <b>Ultimate Precision AI</b>: an end-to-end, "
        "high-throughput automated video surveillance and violence detection platform. The core computational pipeline introduces a novel "
        "<b>32-frame vectorized batching algorithm</b> coupled with a transfer-learning <b>MobileNetV2</b> deep convolutional neural network. "
        "By replacing slow sequential frame inference with synchronized batched tensor operations, the inference engine achieves an "
        "accelerated throughput of <b>114.9 Frames Per Second (FPS)</b>—delivering a <b>5.6x speedup</b> over conventional pipelines and "
        "enabling real-time multi-stream processing on cost-effective commodity compute hardware without requiring dedicated enterprise GPUs."
    )
    story.append(Paragraph(abstract_p2, styles['BBBodyIndent']))

    abstract_p3 = (
        "Crucially, the system pioneers an evidentiary <b>Exact Detected Violent Frames</b> module that automatically isolates physical "
        "keyframe images corresponding to violent incidents, tags each with an exact millisecond timestamp (e.g., <code>00:00:05</code>) "
        "and confidence percentage, clusters adjacent anomalous frames into cohesive incident intervals, and stitches a forensic highlight reel. "
        "The entire AI backend is married to a responsive <b>Next.js 15 (React 19)</b> full-stack dashboard featuring <b>HTTP 206 Partial "
        "Content byte-range video streaming</b>, interactive timeline seeking, automated forensic PDF dossier export via ReportLab, and MongoDB "
        "audit logging. Extensive empirical validation on real-world benchmark datasets achieves <b>86.8% accuracy</b>, <b>84.2% precision</b>, "
        "and <b>89.1% recall</b>, establishing a new state of the art in production-ready automated public safety intelligence."
    )
    story.append(Paragraph(abstract_p3, styles['BBBodyIndent']))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Keywords:</b> Video Surveillance, Violence Detection, Deep Learning, MobileNetV2, Vectorized Batching, "
        "Computer Vision, Keyframe Extraction, Next.js 15, HTTP 206 Streaming, Forensic Computing.",
        styles['BBCallout']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGES 8-10: TABLE OF CONTENTS (Pages vi, vii, viii)
    # =========================================================================
    story.append(PageTarget("toc_page", target_dir))
    story.append(Paragraph("TABLE OF CONTENTS", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=12))

    toc_items = [
        # Front matter
        ("Certificate", get_p("certificate_page", "i"), True),
        ("Candidate’s Declaration", get_p("declaration_page", "ii"), True),
        ("Evaluation Committee Approval Sheet", get_p("approval_page", "iii"), True),
        ("Acknowledgement", get_p("ack_page", "iv"), True),
        ("Abstract", get_p("abstract_page", "v"), True),
        ("List of Figures", get_p("lof_page", "ix"), True),
        ("List of Tables", get_p("lot_page", "x"), True),
        ("List of Abbreviations & Acronyms", get_p("abbrev_page", "xi"), True),
        
        # Chapter 1
        ("CHAPTER 1: INTRODUCTION", get_p("ch1_start", "1"), True),
        ("   1.1 Background and Societal Context", get_p("ch1_1", "1"), False),
        ("   1.2 The Surveillance Landscape & Smart Urban Infrastructure", get_p("ch1_2", "2"), False),
        ("   1.3 The Human Fatigue Bottleneck in CCTV Monitoring", get_p("ch1_3", "3"), False),
        ("   1.4 Evolution of Video Analytics: From Motion Detection to Deep Learning", get_p("ch1_4", "4"), False),
        ("   1.5 Problem Statement & Research Challenges", get_p("ch1_5", "5"), False),
        ("   1.6 Research Objectives (General & Specific)", get_p("ch1_6", "6"), False),
        ("   1.7 Scope and Operational Boundaries", get_p("ch1_7", "6"), False),
        ("   1.8 Organization of the Dissertation", get_p("ch1_8", "7"), False),
        
        # Chapter 2
        ("CHAPTER 2: LITERATURE SURVEY & THEORETICAL FOUNDATION", get_p("ch2_start", "8"), True),
        ("   2.1 Historical Perspectives in Video Anomaly Detection", get_p("ch2_1", "8"), False),
        ("   2.2 Classical Computer Vision Approaches (STIP, HOF, Optical Flow, SVM)", get_p("ch2_2", "9"), False),
        ("   2.3 Deep Learning Architectures for Violence Recognition", get_p("ch2_3", "10"), False),
        ("       2.3.1 2D Convolutional Neural Networks (2D-CNNs)", get_p("ch2_3_1", "11"), False),
        ("       2.3.2 3D Spatio-Temporal Networks (C3D, I3D, SlowFast)", get_p("ch2_3_2", "12"), False),
        ("       2.3.3 Recurrent & Hybrid Frameworks (CNN-LSTM, ConvLSTM)", get_p("ch2_3_3", "13"), False),
        ("       2.3.4 Vision Transformers & Temporal Attention Mechanisms", get_p("ch2_3_4", "14"), False),
        ("   2.4 Benchmark Video Violence Datasets Analysis", get_p("ch2_4", "14"), False),
        ("   2.5 Comparative Analysis of Existing Systems (Table 2.1)", get_p("ch2_5", "15"), False),
        ("   2.6 Critical Gaps in Contemporary Literature", get_p("ch2_6", "16"), False),
        ("   2.7 Proposed Contributions of Ultimate Precision AI", get_p("ch2_7", "17"), False),
        
        # Chapter 3
        ("CHAPTER 3: METHODOLOGY AND MATHEMATICAL FORMULATION", get_p("ch3_start", "18"), True),
        ("   3.1 Overall System Architecture & Workflow Pipeline", get_p("ch3_1", "18"), False),
        ("   3.2 Video Ingestion, Demuxing, and Decoding via OpenCV", get_p("ch3_2", "19"), False),
        ("   3.3 Spatial Preprocessing, Bicubic Resizing, and Tensor Normalization", get_p("ch3_3", "20"), False),
        ("   3.4 Temporal Vectorized Batch Processing Algorithm", get_p("ch3_4", "21"), False),
        ("       3.4.1 Mathematical Formulation of Batching Efficiency & Speedup", get_p("ch3_4_1", "22"), False),
        ("       3.4.2 Vectorized Tensor Construction & GPU Kernel Execution", get_p("ch3_4_2", "23"), False),
        ("   3.5 Deep Neural Network Architecture: MobileNetV2 Transfer Learning", get_p("ch3_5", "23"), False),
        ("       3.5.1 Inverted Residuals and Linear Bottlenecks", get_p("ch3_5_1", "24"), False),
        ("       3.5.2 Depthwise Separable Convolution vs Standard 2D Convolution", get_p("ch3_5_2", "25"), False),
        ("       3.5.3 Custom Head Classification Layers & Regularization", get_p("ch3_5_3", "26"), False),
        ("   3.6 Classification Confidence, Dynamic Thresholding, and Heuristics", get_p("ch3_6", "26"), False),
        ("   3.7 Temporal Clustering of Continuous Violent Episodes (1.5s Interval Merging)", get_p("ch3_7", "27"), False),
        ("   3.8 Exact Physical Keyframe Extraction & Millisecond Timestamps (00:00:05)", get_p("ch3_8", "27"), False),
        ("   3.9 Automated Violent Highlight Synthesis Pipeline", get_p("ch3_9", "28"), False),

        # Chapter 4
        ("CHAPTER 4: SYSTEM DESIGN AND IMPLEMENTATION", get_p("ch4_start", "29"), True),
        ("   4.1 Full-Stack Tripartite System Architecture", get_p("ch4_1", "29"), False),
        ("   4.2 Full-Stack Next.js 15 Implementation (App Router, Server Actions)", get_p("ch4_2", "30"), False),
        ("   4.3 Database Architecture & MongoDB Schemas", get_p("ch4_3", "31"), False),
        ("       4.3.1 Detection Collection Schema & Keyframe Arrays", get_p("ch4_3_1", "32"), False),
        ("       4.3.2 User Authentication & Audit Trails", get_p("ch4_3_2", "33"), False),
        ("   4.4 High-Performance Backend API Endpoints", get_p("ch4_4", "33"), False),
        ("       4.4.1 Multipart File Upload Pipeline (POST /api/upload)", get_p("ch4_4_1", "34"), False),
        ("       4.4.2 Dynamic HTTP 206 Byte-Range Video Streaming (GET /uploads/[...path])", get_p("ch4_4_2", "35"), False),
        ("       4.4.3 Forensic History & Statistical Reporting APIs", get_p("ch4_4_3", "36"), False),
        ("   4.5 Forensic Cockpit UI & Exact Detected Violent Frames Feature", get_p("ch4_5", "36"), False),
        ("       4.5.1 Exact Frame Gallery Component with Interactive Video Seek", get_p("ch4_5_1", "37"), False),
        ("       4.5.2 Frame Thumbnail Generation & Dynamic Serving", get_p("ch4_5_2", "37"), False),
        ("       4.5.3 Empty State & Zero-Violence Handling", get_p("ch4_5_3", "38"), False),
        ("   4.6 Forensic Report Generation Engine (Automated Dossier Export)", get_p("ch4_6", "38"), False),
        ("   4.7 Security Architecture, Input Sanitization, and Error Boundaries", get_p("ch4_7", "39"), False),

        # Chapter 5
        ("CHAPTER 5: EXPERIMENTAL RESULTS AND PERFORMANCE EVALUATION", get_p("ch5_start", "40"), True),
        ("   5.1 Experimental Setup & Evaluation Testbed Specifications", get_p("ch5_1", "40"), False),
        ("   5.2 Dataset Description & Validation Protocol", get_p("ch5_2", "41"), False),
        ("   5.3 Classification Accuracy, Precision, Recall, and F1-Score", get_p("ch5_3", "42"), False),
        ("   5.4 Confusion Matrix and Error Analysis", get_p("ch5_4", "43"), False),
        ("   5.5 Throughput & Inference Speed Evaluation (Sequential vs 32-Frame Batching)", get_p("ch5_5", "44"), False),
        ("   5.6 Keyframe Extraction Latency & Storage Overhead Analysis", get_p("ch5_6", "45"), False),
        ("   5.7 HTTP 206 Byte-Range Scrubbing Latency vs Traditional Full Download", get_p("ch5_7", "45"), False),
        ("   5.8 Robustness & Sensitivity Analysis (Lighting, Occlusion, Distance)", get_p("ch5_8", "46"), False),
        ("   5.9 Comparative Performance against State-of-the-Art Literature", get_p("ch5_9", "46"), False),

        # Chapter 6
        ("CHAPTER 6: ADVANTAGES, LIMITATIONS, AND PRACTICAL APPLICATIONS", get_p("ch6_start", "47"), True),
        ("   6.1 Key Advantages of Ultimate Precision AI", get_p("ch6_1", "47"), False),
        ("   6.2 Technical Limitations and Boundary Conditions", get_p("ch6_2", "48"), False),
        ("   6.3 Real-World Industrial & Public Safety Applications", get_p("ch6_3", "49"), False),
        ("       6.3.1 Municipal Smart Cities & Law Enforcement Surveillance", get_p("ch6_3_1", "49"), False),
        ("       6.3.2 Educational Institutions and Campus Safety", get_p("ch6_3_2", "50"), False),
        ("       6.3.3 Transit Hubs (Airports, Railway Stations, Metro Terminals)", get_p("ch6_3_3", "50"), False),
        ("       6.3.4 Correctional Facilities and High-Security Compounds", get_p("ch6_3_4", "51"), False),
        ("       6.3.5 Commercial Retail & Banking ATM Kiosks", get_p("ch6_3_5", "51"), False),

        # Chapter 7
        ("CHAPTER 7: CONCLUSION AND FUTURE SCOPE", get_p("ch7_start", "52"), True),
        ("   7.1 Conclusion of the Capstone Project", get_p("ch7_1", "52"), False),
        ("   7.2 Summary of Technical Milestones Achieved", get_p("ch7_2", "53"), False),
        ("   7.3 Future Research Roadmap", get_p("ch7_3", "53"), False),
        ("       7.3.1 Live RTSP / ONVIF IP Camera Stream Ingestion", get_p("ch7_3_1", "53"), False),
        ("       7.3.2 Edge Hardware Optimization via TensorRT / ONNX on NVIDIA Jetson", get_p("ch7_3_2", "54"), False),
        ("       7.3.3 Multi-Modal Audio-Visual Fusion (Acoustic Threat Analysis)", get_p("ch7_3_3", "54"), False),
        ("       7.3.4 Aerial Drone & Mobile Bodycam Video Integration", get_p("ch7_3_4", "54"), False),

        # References & Appendices
        ("REFERENCES", get_p("ref_start", "55"), True),
        ("APPENDIX A: SOURCE CODE IMPLEMENTATION SAMPLES", get_p("app_a_start", "58"), True),
        ("   A.1 High-Throughput Batch Detection Engine (python/run.py)", get_p("app_a_1", "58"), False),
        ("   A.2 HTTP 206 Partial Content Video Streaming Route", get_p("app_a_2", "60"), False),
        ("   A.3 Exact Violent Frame Gallery & Interactive Scrubbing Component", get_p("app_a_3", "61"), False),
        ("APPENDIX B: DEEP NEURAL NETWORK SPECIFICATIONS & DATA SHEETS", get_p("app_b_start", "62"), True),
        ("   B.1 Layer-by-Layer Architectural Breakdown of MobileNetV2", get_p("app_b_1", "62"), False),
        ("   B.2 Mathematical FLOPs Comparison: Standard 2D Conv vs Depthwise Separable", get_p("app_b_2", "63"), False),
        ("APPENDIX C: BILL OF MATERIALS & SYSTEM SPECIFICATIONS", get_p("app_c_start", "64"), True),
        ("   C.1 Detailed Bill of Software Dependencies & Versions", get_p("app_c_1", "64"), False),
        ("   C.2 Hardware Testbed & Recommended Deployment Configuration", get_p("app_c_2", "64"), False),
        ("APPENDIX D: RESEARCH PUBLICATION & CONFERENCE MANUSCRIPT", get_p("app_d_start", "65"), True),
        ("   D.1 Conference Paper Metadata & IEEE Publication Details", get_p("app_d_1", "65"), False),
        ("   D.2 Complete Conference Research Manuscript Draft", get_p("app_d_2", "65"), False),
    ]

    # Split TOC items across 3 pages cleanly
    page1_items = toc_items[:28]
    page2_items = toc_items[28:56]
    page3_items = toc_items[56:]

    for idx, page_group in enumerate([page1_items, page2_items, page3_items]):
        if idx > 0:
            story.append(Paragraph("TABLE OF CONTENTS (Continued)", styles['BBChapterHeader']))
            story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=12))

        group_data = []
        for title, pg, is_bold in page_group:
            style_name = 'BBTableCellBold' if is_bold else 'BBTableCell'
            group_data.append([
                Paragraph(f"<b>{title}</b>" if is_bold else title, styles[style_name]),
                Paragraph(f"<b>{pg}</b>" if is_bold else pg, styles[style_name])
            ])

        toc_table = Table(group_data, colWidths=[390, 60])
        toc_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('LINEBELOW', (0, 0), (-1, -1), 0.2, colors.HexColor("#f1f5f9")),
        ]))
        story.append(toc_table)
        story.append(PageBreak())

    # =========================================================================
    # PAGE 11: LIST OF FIGURES (Page ix)
    # =========================================================================
    story.append(PageTarget("lof_page", target_dir))
    story.append(Paragraph("LIST OF FIGURES", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=12))

    lof_items = [
        ("Figure 1.1", "Cognitive Decline and Error Rate in Continuous CCTV Human Monitoring", get_p("fig_1_1", "3")),
        ("Figure 1.2", "Conceptual Paradigm of Automated Violence Intelligence Ecosystem", get_p("fig_1_2", "4")),
        ("Figure 2.1", "Taxonomy of Video Anomaly and Violence Detection Methodologies", get_p("fig_2_1", "9")),
        ("Figure 2.2", "Structural Comparison: 2D-CNN, 3D-CNN, CNN-LSTM, and Transformer", get_p("fig_2_2", "11")),
        ("Figure 3.1", "End-to-End Computational Architecture of Ultimate Precision AI", get_p("fig_3_1", "19")),
        ("Figure 3.2", "Temporal Vectorized 32-Frame Batch Ingestion and Tensor Formation", get_p("fig_3_2", "22")),
        ("Figure 3.3", "Internal Micro-Architecture of MobileNetV2 Inverted Residual Bottleneck Block", get_p("fig_3_3", "24")),
        ("Figure 3.4", "Depthwise Separable Convolution vs Standard Convolution Decomposition", get_p("fig_3_4", "25")),
        ("Figure 3.5", "Temporal Clustering Algorithm Merging Contiguous Frames within 1.5s Interval", get_p("fig_3_5", "27")),
        ("Figure 4.1", "Full-Stack Client-Server-AI Tripartite Operational Architecture", get_p("fig_4_1", "30")),
        ("Figure 4.2", "MongoDB Entity-Relationship and Document Schema Hierarchy", get_p("fig_4_2", "32")),
        ("Figure 4.3", "Dynamic HTTP 206 Partial Content Video Scrubbing Negotiation Protocol", get_p("fig_4_3", "35")),
        ("Figure 4.4", "Forensic Cockpit UI: Responsive Gallery with Instant Timestamp Seeking", get_p("fig_4_4", "37")),
        ("Figure 5.1", "Normalized Confusion Matrix for Violence Classification on Test Benchmark", get_p("fig_5_1", "43")),
        ("Figure 5.2", "Receiver Operating Characteristic (ROC) Curve and Area Under Curve (AUC)", get_p("fig_5_2", "43")),
        ("Figure 5.3", "Throughput Comparison: Sequential Processing vs 32-Frame Batching (FPS)", get_p("fig_5_3", "44")),
        ("Figure 5.4", "Interactive Scrubbing Latency: HTTP 206 Streaming vs Traditional Full Download", get_p("fig_5_4", "45")),
        ("Figure 7.1", "Architectural Roadmap for Edge AI Jetson Node and Multi-Modal Surveillance", get_p("fig_7_1", "54")),
    ]

    lof_data = [
        [Paragraph("<b>Figure No.</b>", styles['BBTableHeader']), Paragraph("<b>Figure Description / Title</b>", styles['BBTableHeader']), Paragraph("<b>Page</b>", styles['BBTableHeader'])],
    ]
    for num, title, pg in lof_items:
        lof_data.append([
            Paragraph(f"<b>{num}</b>", styles['BBTableCellBold']),
            Paragraph(title, styles['BBTableCell']),
            Paragraph(pg, styles['BBTableCellBold']),
        ])

    lof_table = Table(lof_data, colWidths=[80, 310, 60])
    lof_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(lof_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: LIST OF TABLES (Page x)
    # =========================================================================
    story.append(PageTarget("lot_page", target_dir))
    story.append(Paragraph("LIST OF TABLES", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=12))

    lot_items = [
        ("Table 1.1", "Public Surveillance Ingestion Scale and Computational Demands", get_p("tab_1_1", "2")),
        ("Table 1.2", "Key Research Objectives and Quantifiable Success Criteria", get_p("tab_1_2", "6")),
        ("Table 2.1", "Exhaustive Comparative Literature Analysis of Video Violence Detection", get_p("tab_2_1", "15")),
        ("Table 2.2", "Benchmark Violence Datasets Quantitative Specification Comparison", get_p("tab_2_2", "14")),
        ("Table 3.1", "Mathematical Parameter Notations and Dimension Specifications", get_p("tab_3_1", "21")),
        ("Table 3.2", "Computational Complexity: Standard 2D Conv vs Depthwise Separable Conv", get_p("tab_3_2", "25")),
        ("Table 4.1", "RESTful API Endpoints Specification of Ultimate Precision AI", get_p("tab_4_1", "34")),
        ("Table 4.2", "MongoDB Detection Document Schema Field Definitions and Types", get_p("tab_4_2", "32")),
        ("Table 5.1", "Hardware and Software Environment Testbed Specifications", get_p("tab_5_1", "40")),
        ("Table 5.2", "Comprehensive Classification Performance Metrics on Validation Benchmark", get_p("tab_5_2", "42")),
        ("Table 5.3", "Throughput and Processing Latency Benchmarks across Batch Sizes", get_p("tab_5_3", "44")),
        ("Table 5.4", "State-of-the-Art Comparative Evaluation against Recent Published Works", get_p("tab_5_4", "46")),
        ("Table 6.1", "Domain-Specific Operational Value Matrix for Enterprise Deployment", get_p("tab_6_1", "49")),
        ("Table B.1", "Detailed Layer-by-Layer Architectural Specifications of MobileNetV2", get_p("tab_b_1", "62")),
        ("Table C.1", "Complete Bill of Software Packages, Frameworks, and Runtime Versions", get_p("tab_c_1", "64")),
        ("Table C.2", "Hardware Deployment Sizing: Edge Node vs Enterprise Central Server", get_p("tab_c_2", "64")),
    ]

    lot_data = [
        [Paragraph("<b>Table No.</b>", styles['BBTableHeader']), Paragraph("<b>Table Title / Description</b>", styles['BBTableHeader']), Paragraph("<b>Page</b>", styles['BBTableHeader'])],
    ]
    for num, title, pg in lot_items:
        lot_data.append([
            Paragraph(f"<b>{num}</b>", styles['BBTableCellBold']),
            Paragraph(title, styles['BBTableCell']),
            Paragraph(pg, styles['BBTableCellBold']),
        ])

    lot_table = Table(lot_data, colWidths=[80, 310, 60])
    lot_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(lot_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: LIST OF ABBREVIATIONS AND ACRONYMS (Page xi)
    # =========================================================================
    story.append(PageTarget("abbrev_page", target_dir))
    story.append(Paragraph("LIST OF ABBREVIATIONS & ACRONYMS", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=12))

    abbrev_list = [
        ("AI", "Artificial Intelligence"),
        ("ANN", "Artificial Neural Network"),
        ("API", "Application Programming Interface"),
        ("AUC-ROC", "Area Under the Receiver Operating Characteristic Curve"),
        ("CCTV", "Closed-Circuit Television"),
        ("CNN", "Convolutional Neural Network"),
        ("ConvLSTM", "Convolutional Long Short-Term Memory Network"),
        ("CPU", "Central Processing Unit"),
        ("CUDA", "Compute Unified Device Architecture (NVIDIA)"),
        ("cuDNN", "CUDA Deep Neural Network Library"),
        ("DL", "Deep Learning"),
        ("FLOPs", "Floating-Point Operations"),
        ("FPS", "Frames Per Second"),
        ("FNR", "False Negative Rate (Miss Rate)"),
        ("FPR", "False Positive Rate (Fall-out)"),
        ("GPU", "Graphics Processing Unit"),
        ("HLS", "HTTP Live Streaming"),
        ("HOF", "Histograms of Optical Flow"),
        ("HOG", "Histograms of Oriented Gradients"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("I3D", "Inflated 3D Convolutional Network"),
        ("IEEE", "Institute of Electrical and Electronics Engineers"),
        ("IoT", "Internet of Things"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token"),
        ("LSTM", "Long Short-Term Memory"),
        ("ML", "Machine Learning"),
        ("MPSTME", "Mukesh Patel School of Technology Management & Engineering"),
        ("ODM", "Object Data Modeling"),
        ("ONNX", "Open Neural Network Exchange"),
        ("ONVIF", "Open Network Video Interface Forum"),
        ("OpenCV", "Open Source Computer Vision Library"),
        ("REST", "Representational State Transfer"),
        ("RGB", "Red Green Blue (Color Model)"),
        ("RLVS", "Real-Life Violence Situations Dataset"),
        ("RNN", "Recurrent Neural Network"),
        ("RTSP", "Real-Time Streaming Protocol"),
        ("SSR", "Server-Side Rendering"),
        ("STIP", "Spatio-Temporal Interest Points"),
        ("SVM", "Support Vector Machine"),
        ("TensorRT", "NVIDIA TensorRT High-Performance Inference Optimizer"),
        ("TOC", "Table of Contents"),
        ("TPR", "True Positive Rate (Recall / Sensitivity)"),
        ("UI / UX", "User Interface / User Experience"),
        ("URI / URL", "Uniform Resource Identifier / Uniform Resource Locator"),
        ("VGG", "Visual Geometry Group (Oxford University)"),
        ("YOLO", "You Only Look Once (Real-Time Object Detection)"),
    ]

    abbrev_data = [
        [Paragraph("<b>Acronym</b>", styles['BBTableHeader']), Paragraph("<b>Complete Expanded Terminology</b>", styles['BBTableHeader'])],
    ]
    for acr, exp in abbrev_list:
        abbrev_data.append([
            Paragraph(f"<b>{acr}</b>", styles['BBTableCellBold']),
            Paragraph(exp, styles['BBTableCell']),
        ])

    abbrev_table = Table(abbrev_data, colWidths=[90, 360])
    abbrev_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(abbrev_table)
    story.append(PageBreak())

    return story
