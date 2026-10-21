from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def generate_chapter_1(styles, PageTarget, target_dir):
    story = []
    PRIMARY = colors.HexColor("#0f172a")
    SECONDARY = colors.HexColor("#1e3a8a")
    CARD_BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f8fafc")

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(PageTarget("ch1_start", target_dir))
    story.append(Paragraph("CHAPTER 1", styles['BBTitle24']))
    story.append(Paragraph("INTRODUCTION", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=14))

    # 1.1 Background and Societal Context
    story.append(PageTarget("ch1_1", target_dir))
    story.append(Paragraph("1.1 Background and Societal Context", styles['BBSectionHeader']))
    story.append(Paragraph(
        "In the contemporary era of rapid urbanization, population expansion, and smart city modernization, ensuring public "
        "safety and physical security has emerged as one of the paramount socio-technical challenges confronting municipal "
        "administrations, law enforcement agencies, transit operators, and educational institutions worldwide. Physical violence, "
        "violent assaults, street brawls, armed robberies, gang confrontations, and public disturbances inflict profound physical, "
        "psychological, and economic trauma on human communities. According to reports published by global public health organizations "
        "and criminal justice institutes, inter-personal violence accounts for hundreds of thousands of avoidable casualties annually, "
        "generating billions of dollars in medical costs, infrastructure damage, and policing overhead.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "To deter criminality, enhance situational awareness, and protect civilian populations, public authorities and private "
        "enterprises have invested heavily in large-scale visual surveillance infrastructure. Modern metropolitan areas are now "
        "blanketed by dense networks of Closed-Circuit Television (CCTV) cameras, smart IP dome cameras, high-definition panoramic "
        "optical sensors, and traffic monitoring equipment. These cameras maintain 24/7 vigil across streets, public squares, metro "
        "stations, bus terminals, airport concourses, school corridors, university campuses, shopping malls, and industrial complexes. "
        "The ubiquity of these optical feeds guarantees that an overwhelming majority of violent crimes and antisocial disruptions "
        "occur directly within the field of view of one or more surveillance cameras.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 1.2 The Surveillance Landscape & Smart Urban Infrastructure
    story.append(PageTarget("ch1_2", target_dir))
    story.append(Paragraph("1.2 The Surveillance Landscape & Smart Urban Infrastructure", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Despite the omnipresence of recording hardware, modern surveillance systems exhibit a fundamental structural paradox: "
        "<b>an abundance of visual data accompanied by a severe deficit of actionable real-time intelligence</b>. Modern municipal "
        "camera installations stream thousands of concurrent video channels into Central Command and Control Centers (CCCCs). "
        "A tier-1 metropolitan smart city may maintain between 20,000 and 100,000 active CCTV feeds, continuously ingesting video "
        "at 25 to 30 frames per second (FPS).",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "This data deluge results in an astronomical volume of video material that easily overwhelms classical compute and human storage "
        "paradigms. Table 1.1 illustrates the sheer mathematical scale of visual ingestion confronting modern urban surveillance networks.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Table 1.1
    story.append(PageTarget("tab_1_1", target_dir))
    story.append(Paragraph("<b>Table 1.1: Public Surveillance Ingestion Scale and Computational Demands</b>", styles['BBSubSectionHeader']))
    tab1_data = [
        [Paragraph("<b>Surveillance Scale Profile</b>", styles['BBTableHeader']), Paragraph("<b>Active Cameras</b>", styles['BBTableHeader']), Paragraph("<b>Daily Ingestion (Hours)</b>", styles['BBTableHeader']), Paragraph("<b>Daily Data Footprint (TB)</b>", styles['BBTableHeader']), Paragraph("<b>Human Operators Needed</b>", styles['BBTableHeader'])],
        [Paragraph("Educational Campus / Mall", styles['BBTableCellBold']), Paragraph("150 - 300", styles['BBTableCell']), Paragraph("3,600 - 7,200", styles['BBTableCell']), Paragraph("18 - 36 TB", styles['BBTableCell']), Paragraph("12 - 25", styles['BBTableCell'])],
        [Paragraph("Transit Hub (Metro / Airport)", styles['BBTableCellBold']), Paragraph("500 - 1,500", styles['BBTableCell']), Paragraph("12,000 - 36,000", styles['BBTableCell']), Paragraph("60 - 180 TB", styles['BBTableCell']), Paragraph("40 - 100", styles['BBTableCell'])],
        [Paragraph("Tier-2 Municipal Smart City", styles['BBTableCellBold']), Paragraph("3,000 - 8,000", styles['BBTableCell']), Paragraph("72,000 - 192,000", styles['BBTableCell']), Paragraph("360 - 960 TB", styles['BBTableCell']), Paragraph("200 - 500", styles['BBTableCell'])],
        [Paragraph("Tier-1 Megacity Metropolis", styles['BBTableCellBold']), Paragraph("25,000 - 100,000+", styles['BBTableCell']), Paragraph("600,000 - 2,400,000+", styles['BBTableCell']), Paragraph("3,000 - 12,000 TB", styles['BBTableCell']), Paragraph("1,500 - 6,000+", styles['BBTableCell'])],
    ]
    t1 = Table(tab1_data, colWidths=[110, 75, 95, 95, 75])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))
    story.append(t1)
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "As formalized in Table 1.1, continuously storing and manually supervising even a moderately sized campus deployment "
        "generates petabytes of unstructured visual artifacts. The current operating reality is that over <b>99.4% of recorded "
        "surveillance footage is never inspected in real time</b>; instead, it is cyclically overwritten on Network Video Recorders "
        "(NVRs) or archived into cold storage, serving only as post-incident forensic evidence after an assault, robbery, or tragic "
        "loss of life has already transpired.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    # 1.3 The Human Fatigue Bottleneck in CCTV Monitoring
    story.append(PageTarget("ch1_3", target_dir))
    story.append(Paragraph("1.3 The Human Fatigue Bottleneck in CCTV Monitoring", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Historically, the responsibility of identifying hostile aggression, brawls, weapon drawing, or panic in surveillance feeds "
        "has rested entirely upon human security guards seated before multi-screen video walls. However, extensive ergonomic and "
        "psychological research into human visual attention confirms that the human brain is physiologically ill-equipped for passive, "
        "sustained vigilance across dense visual matrices.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "Controlled behavioral studies conducted by security science laboratories demonstrate that an operator assigned to monitor "
        "more than four simultaneous video monitors experiences a severe deterioration in cognitive vigilance within minutes. Specifically: "
        "<br/>1. <b>Rapid Attentional Fatigue:</b> After 20 minutes of continuous observation, the average operator's attention spans "
        "plummet below 50% of baseline capacity.<br/>"
        "2. <b>Critical Miss Rates:</b> After 40 minutes of uninterrupted screen observation, human guards fail to detect up to <b>95% of subtle, "
        "fleeting, or peripheral anomalous events</b>, including physical pushes, weapon brandishing, and purse snatching.<br/>"
        "3. <b>Change Blindness & Cognitive Overload:</b> When managing split-screen video walls displaying 16 to 64 tiles, the human visual "
        "cortex suffers from severe change blindness, rendering simultaneous spatial tracking practically impossible.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # Figure 1.1 Box
    story.append(PageTarget("fig_1_1", target_dir))
    fig1_data = [
        [Paragraph("<b>Figure 1.1: Cognitive Decline and Detection Failure Rate in Continuous CCTV Human Monitoring</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "[ Operational Vigilance Degradation Curve ]<br/>"
            "-----------------------------------------------------------------------------------------------------------------------<br/>"
            "Elapsed Time (Minutes)    |   Operator Attentional Focus (%)   |   Undetected Security Breaches (%)<br/>"
            "00 - 10 mins (Baseline)  |   [||||||||||||||||||||]  100%     |   [||]                  10% (Normal False Negatives)<br/>"
            "10 - 20 mins             |   [|||||||||||||||     ]   78%     |   [|||||]               26% Missed Threats<br/>"
            "20 - 30 mins             |   [||||||||||          ]   52%     |   [|||||||||||]         58% Missed Threats<br/>"
            "30 - 45 mins             |   [|||||               ]   26%     |   [|||||||||||||||||]   84% Missed Threats<br/>"
            "45 - 60+ mins            |   [||                  ]   11%     |   [|||||||||||||||||||] 95% Threat Blindness<br/>"
            "-----------------------------------------------------------------------------------------------------------------------<br/>"
            "<i>Empirical finding: Human-only surveillance monitoring guarantees severe blind spots during prolonged operational shifts.</i>",
            styles['BBCode']
        )]
    ]
    t_fig1 = Table(fig1_data, colWidths=[450])
    t_fig1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_fig1)
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Consequently, relying solely on human personnel to perceive sudden acts of violence across municipal camera arrays is "
        "inherently unscalable and prone to catastrophic failure. There exists a mandatory imperative for autonomous, algorithmic "
        "surveillance systems capable of continuously scrutinizing video streams, filtering benign activities, and raising instant alerts.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    # 1.4 Evolution of Video Analytics: From Motion Detection to Deep Learning
    story.append(PageTarget("ch1_4", target_dir))
    story.append(Paragraph("1.4 Evolution of Video Analytics: From Motion Detection to Deep Learning", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The computer vision community has long sought to automate video anomaly detection. The evolution of video analytics can "
        "be categorized into three distinct historical eras:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Era 1: Pixel Differencing and Background Subtraction (1995-2005):</b> Early surveillance analytics utilized basic background "
        "subtraction algorithms such as Gaussian Mixture Models (GMM) and frame differencing to identify motion. However, these systems "
        "could not discern the semantic nature of movement. Leaves swaying in the wind, passing vehicles, shadows, and camera jitter "
        "triggered rampant false alarms, rendering them unusable for public violence recognition.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Era 2: Handcrafted Spatio-Temporal Feature Descriptors (2006-2014):</b> Researchers developed sophisticated mathematical "
        "descriptors including Histograms of Oriented Gradients (HOG), Histograms of Optical Flow (HOF), and Spatio-Temporal Interest Points "
        "(STIP). Paired with Support Vector Machines (SVM), these algorithms attempted to quantify violent motion. However, handcrafted "
        "features lacked generalization: changes in illumination, camera angle, crowd density, or clothing textures caused catastrophic "
        "performance degradation.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Era 3: Deep Convolutional Neural Networks and Transfer Learning (2015-Present):</b> The advent of Deep Learning (DL) has "
        "revolutionized video understanding. Deep Convolutional Neural Networks (CNNs) automatically extract hierarchical spatial and "
        "temporal abstractions directly from raw video pixels. Pre-trained on vast visual corpuses (such as ImageNet), deep models "
        "exhibit remarkable feature robustness across diverse real-world environmental settings.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 1.2 Box
    story.append(PageTarget("fig_1_2", target_dir))
    fig2_data = [
        [Paragraph("<b>Figure 1.2: Conceptual Paradigm of Automated Violence Intelligence Ecosystem</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   [ CCTV Stream / Upload ] --------> [ 32-Frame Vectorized Batching ] --------> [ MobileNetV2 Deep CNN ]\n"
            "                                                                                          |\n"
            "                                                                                          v\n"
            "   [ Executive Action ] <--- [ Full-Stack Cockpit ] <--- [ HTTP 206 Streaming ] <--- [ Evidence Extraction ]\n"
            "   (Instant Dispatch)        (React 19 / Next.js)       (Byte-Range Scrubbing)       (Exact Timestamps & Frames)",
            styles['BBCode']
        )]
    ]
    t_fig2 = Table(fig2_data, colWidths=[450])
    t_fig2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_fig2)
    story.append(PageBreak())

    # 1.5 Problem Statement & Research Challenges
    story.append(PageTarget("ch1_5", target_dir))
    story.append(Paragraph("1.5 Problem Statement & Research Challenges", styles['BBSectionHeader']))
    story.append(Paragraph(
        "While deep learning has established superior theoretical accuracy on benchmark academic datasets, translating these "
        "models into operational, real-world public safety software reveals profound architectural bottlenecks. Contemporary "
        "academic literature and commercial implementations suffer from four major deficiencies:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Challenge 1: Prohibitive Inference Latency and Hardware Cost:</b> State-of-the-art spatio-temporal video architectures "
        "(such as 3D Convolutional Networks, C3D, and Inflated 3D ConvNets - I3D) contain upwards of 40 to 60 million parameters and require "
        "hundreds of GFLOPs per second of video. Processing high-resolution video through these architectures requires multi-thousand-dollar "
        "server GPUs (e.g., NVIDIA A100/H100). Sequential frame processing in traditional Python loops yields abysmal throughput "
        "(10 to 18 FPS), making real-time multi-camera surveillance economically and computationally unviable.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Challenge 2: Black-Box Predictions Lacking Granular Evidence:</b> Most existing violence detection models output a single "
        "scalar prediction or an unanchored binary classification score for an entire video file. In real-world security operations, "
        "a simple alert stating 'Video contains violence' is completely inadequate. Security personnel require exact evidentiary "
        "verification: precisely which seconds of the footage contained violence, what physical actions took place, and exact visual "
        "thumbnails showing suspect identities, weapons, and points of impact.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Challenge 3: High False Alarm Rates from Fast Benign Motion:</b> Public environments abound with vigorous non-violent "
        "activities: running to catch a departing train, enthusiastic greetings, sports activities, dancing, and rapid gestures. "
        "Existing systems frequently misclassify these benign dynamic motions as violent attacks, overwhelming security operators "
        "with false alarms and triggering alert fatigue.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Challenge 4: Absence of Integrated Production Software Architecture:</b> Academic papers routinely evaluate model weights "
        "in isolated Python Jupyter notebooks, completely detached from enterprise operational workflows. Real-world incident response "
        "demands an integrated full-stack software system: responsive web dashboards, instant video seeking, dynamic byte-range streaming, "
        "database persistence, and tamper-resistant forensic dossier generation.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 1.6 Research Objectives
    story.append(PageTarget("ch1_6", target_dir))
    story.append(Paragraph("1.6 Research Objectives (General & Specific)", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The overarching objective of this Capstone Project is to architect, develop, empirically evaluate, and deploy "
        "<b>Ultimate Precision AI</b>—a production-grade, high-throughput automated video surveillance platform that resolves "
        "the latency, evidentiary, and full-stack integration bottlenecks of contemporary systems.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "To achieve this primary goal, the following specific research and engineering milestones were formulated and executed:",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # Table 1.2
    story.append(PageTarget("tab_1_2", target_dir))
    story.append(Paragraph("<b>Table 1.2: Key Research Objectives and Quantifiable Success Criteria</b>", styles['BBSubSectionHeader']))
    tab2_data = [
        [Paragraph("<b>Objective Code</b>", styles['BBTableHeader']), Paragraph("<b>Research & Engineering Milestone</b>", styles['BBTableHeader']), Paragraph("<b>Target Technical Metric / Criterion</b>", styles['BBTableHeader'])],
        [Paragraph("OBJ-1", styles['BBTableCellBold']), Paragraph("Vectorized Batch Pipeline Optimization", styles['BBTableCell']), Paragraph("Achieve >= 100 FPS throughput (32-frame vectorized batching)", styles['BBTableCell'])],
        [Paragraph("OBJ-2", styles['BBTableCellBold']), Paragraph("Deep Learning Transfer Model Integration", styles['BBTableCell']), Paragraph("Validation classification accuracy >= 85% on benchmark datasets", styles['BBTableCell'])],
        [Paragraph("OBJ-3", styles['BBTableCellBold']), Paragraph("Granular Keyframe Extraction & Timestamping", styles['BBTableCell']), Paragraph("Isolate physical frames with exact HH:MM:SS timestamps (00:00:05)", styles['BBTableCell'])],
        [Paragraph("OBJ-4", styles['BBTableCellBold']), Paragraph("Continuous Incident Clustering & Highlight Reel", styles['BBTableCell']), Paragraph("Cluster frames within 1.5s delta and stitch MP4 highlight video", styles['BBTableCell'])],
        [Paragraph("OBJ-5", styles['BBTableCellBold']), Paragraph("Dynamic Byte-Range Video Streaming UI", styles['BBTableCell']), Paragraph("Implement HTTP 206 partial streaming with sub-200ms scrubbing", styles['BBTableCell'])],
        [Paragraph("OBJ-6", styles['BBTableCellBold']), Paragraph("Full-Stack Production System Integration", styles['BBTableCell']), Paragraph("Deliver unified Next.js 15, React 19, and MongoDB persistent stack", styles['BBTableCell'])],
    ]
    t2 = Table(tab2_data, colWidths=[80, 180, 190])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # 1.7 Scope and Operational Boundaries
    story.append(PageTarget("ch1_7", target_dir))
    story.append(Paragraph("1.7 Scope and Operational Boundaries", styles['BBSectionHeader']))
    story.append(Paragraph(
        "To ensure rigorous execution and verifiable results, the functional and environmental scope of this dissertation "
        "is delineated as follows:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>In-Scope Capabilities:</b><br/>"
        "• Autonomous classification of video footage into violent and non-violent semantic categories.<br/>"
        "• Detection of interpersonal physical aggression, assaults, brawls, punching, kicking, and violent clashes.<br/>"
        "• Ingestion of standard digital video formats (MP4, AVI, MOV, MKV, WebM) up to 1GB per session.<br/>"
        "• Synchronous and asynchronous vectorized batch inference using optimized MobileNetV2 architecture.<br/>"
        "• Automated extraction and physical disk persistence of genuine violent keyframe images with confidence scores.<br/>"
        "• Accurate millisecond timestamp computation (HH:MM:SS format) synced to video source metadata.<br/>"
        "• Dynamic HTTP 206 Partial Content byte-range video streaming supporting arbitrary timeline seeking.<br/>"
        "• Responsive web dashboard providing interactive frame gallery scrutiny, seeking, and empty-state messaging.<br/>"
        "• Persistent storage of detection audit trails and user statistics in MongoDB document collections.",
        styles['BBBullet']
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Out-of-Scope / Operational Boundaries:</b><br/>"
        "• Semantic facial recognition or automated suspect identity profiling (omitted to preserve privacy regulations).<br/>"
        "• Direct hardware PTZ motor control of physical pan-tilt-zoom camera heads.<br/>"
        "• Acoustic gunshot or audio screams classification (current implementation operates purely on visual optical frames).<br/>"
        "• Real-time edge inference on sub-5W microcontrollers (system is designed for edge SBCs such as Jetson / x86 servers).",
        styles['BBBullet']
    ))
    story.append(Spacer(1, 10))

    # 1.8 Organization of the Dissertation
    story.append(PageTarget("ch1_8", target_dir))
    story.append(Paragraph("1.8 Organization of the Dissertation", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The remainder of this Capstone Project Dissertation is methodically structured across six succeeding chapters, an exhaustive "
        "bibliography of academic references, and four technical appendices:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "• <b>Chapter 2: Literature Survey & Theoretical Foundation</b> presents a comprehensive review of classical and deep learning "
        "approaches to video anomaly recognition, evaluates standard benchmark datasets, and highlights critical gaps in current literature.<br/>"
        "• <b>Chapter 3: Methodology and Mathematical Formulation</b> articulates the mathematical principles of depthwise separable "
        "convolutions, formulates the 32-frame vectorized batching speedup, and details keyframe extraction and temporal clustering.<br/>"
        "• <b>Chapter 4: System Design and Implementation</b> documents the full-stack system architecture, Next.js 15 App Router "
        "implementation, HTTP 206 byte-range streaming mechanics, MongoDB schema designs, and the Exact Detected Violent Frames UI.<br/>"
        "• <b>Chapter 5: Experimental Results and Performance Evaluation</b> delivers exhaustive empirical benchmarks, confusion matrices, "
        "throughput comparisons (114.9 FPS), extraction latency analyses, and comparative evaluations against published baselines.<br/>"
        "• <b>Chapter 6: Advantages, Limitations, and Practical Applications</b> evaluates operational strengths, articulates boundary "
        "conditions, and maps industrial deployment scenarios across smart cities, transit terminals, and educational campuses.<br/>"
        "• <b>Chapter 7: Conclusion and Future Scope</b> summarizes key technical accomplishments, concludes the findings, and outlines "
        "a forward-looking research roadmap encompassing edge TensorRT optimization and multi-modal audio-visual fusion.<br/>"
        "• <b>References</b> catalogs 28 IEEE format scholarly publications.<br/>"
        "• <b>Appendices A to D</b> provide full source code implementations, neural network layer specifications, hardware bills, and "
        "the drafted conference research manuscript.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    return story
