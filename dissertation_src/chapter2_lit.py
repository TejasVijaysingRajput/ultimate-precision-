from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def generate_chapter_2(styles, PageTarget, target_dir):
    story = []
    PRIMARY = colors.HexColor("#0f172a")
    SECONDARY = colors.HexColor("#1e3a8a")
    CARD_BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f8fafc")

    # =========================================================================
    # CHAPTER 2: LITERATURE SURVEY & THEORETICAL FOUNDATION
    # =========================================================================
    story.append(PageTarget("ch2_start", target_dir))
    story.append(Paragraph("CHAPTER 2", styles['BBTitle24']))
    story.append(Paragraph("LITERATURE SURVEY & THEORETICAL FOUNDATION", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=14))

    # 2.1 Historical Perspectives
    story.append(PageTarget("ch2_1", target_dir))
    story.append(Paragraph("2.1 Historical Perspectives in Video Anomaly Detection", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Automated visual violence detection is a specialized, highly challenging subset of general video activity recognition "
        "and human action understanding. Unlike generic human activities (such as walking, sitting, or waving), violent encounters "
        "are characterized by chaotic non-linear motion trajectories, extreme physical occlusions between bodies, rapid fluctuations "
        "in velocity, and subtle psychological intentions that distinguish aggressive combat from energetic sporting or social interactions. "
        "Over the past three decades, research in this domain has progressed from handcrafted heuristic descriptors to deep end-to-end "
        "neural feature representations.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "Early research treated anomaly detection as an outlier modeling problem in low-dimensional visual feature spaces. "
        "Normal crowd behaviors were modeled using statistical distributions (such as Hidden Markov Models or Gaussian Mixture Models), "
        "and any deviation in optical flow magnitude was flagged as an anomaly. However, these formulations proved brittle in public "
        "environments where normal behaviors display immense stochastic variance. Figure 2.1 illustrates the structural taxonomy "
        "of methodological paradigms developed across the computer vision literature.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 2.1 Box
    story.append(PageTarget("fig_2_1", target_dir))
    fig21_data = [
        [Paragraph("<b>Figure 2.1: Taxonomy of Video Anomaly and Violence Detection Methodologies</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "                             [ Video Violence Detection Methodologies ]\n"
            "                                                 |\n"
            "                 +-------------------------------+-------------------------------+\n"
            "                 |                                                               |\n"
            "     [ Classical Handcrafted Approaches ]                         [ Deep Learning Architectures ]\n"
            "                 |                                                               |\n"
            "     +-----------+-----------+                     +-------------+---------------+-------------+\n"
            "     |                       |                     |             |               |             |\n"
            " [ Optical Flow ]     [ STIP / HOF / HOG ]     [ 2D-CNNs ]   [ 3D-CNNs ]   [ CNN-LSTM ]   [ Transformers ]\n"
            " (Horn-Schunck,        (Laptev et al.,          (VGG, ResNet, (C3D, I3D,    (ConvLSTM,     (TimeSformer,\n"
            "  Lucas-Kanade)        Dollar et al.)            MobileNet)    SlowFast)     BiLSTM)        ViViT)",
            styles['BBCode']
        )]
    ]
    t_fig21 = Table(fig21_data, colWidths=[450])
    t_fig21.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig21)
    story.append(PageBreak())

    # 2.2 Classical Computer Vision Approaches
    story.append(PageTarget("ch2_2", target_dir))
    story.append(Paragraph("2.2 Classical Computer Vision Approaches (STIP, HOF, Optical Flow, SVM)", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Prior to the resurgence of deep artificial neural networks, video violence detection relied predominantly on a two-stage "
        "pipeline: handcrafted feature engineering followed by shallow statistical classification. The seminal contributions in this "
        "paradigm focused on capturing spatio-temporal motion dynamics:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>1. Spatio-Temporal Interest Points (STIP):</b> Laptev and Lindeberg (2003) extended 2D Harris corner detectors into the temporal "
        "dimension by computing space-time interest points where visual values exhibit significant local variations in both space and time. "
        "Dollar et al. (2005) applied separable linear filters to extract periodic motion cuboids. While effective for isolated periodic "
        "actions, STIP extractors suffered from severe computational bottlenecks and failed when background clutter or camera motion "
        "introduced spurious interest points.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>2. Optical Flow Histograms (HOF & Violent Flows - ViF):</b> Hassner et al. (2012) proposed the Violent Flows (ViF) descriptor "
        "specifically designed for detecting violence in crowded scenes. ViF computes the magnitude and orientation of optical flow vectors "
        "between consecutive frames and constructs statistical histograms tracking high-frequency flow variations. While computationally "
        "lighter than 3D interest points, ViF is incapable of distinguishing aggressive interpersonal violence from benign crowd panics, "
        "running crowds, or sudden panning movements of the surveillance camera.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>3. Support Vector Machine (SVM) Classification:</b> Handcrafted feature vectors (HOG, HOF, Motion Boundary Histograms - MBH) "
        "were concatenated and passed into non-linear Support Vector Machines (SVMs) with Radial Basis Function (RBF) kernels. Although "
        "these classifiers achieved modest success on small, constrained datasets (such as the Hockey Fights dataset), they completely "
        "failed to generalize when deployed in real-world surveillance scenarios exhibiting variable lighting, shadows, occlusions, and "
        "complex camera viewing geometries.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 2.3 Deep Learning Architectures
    story.append(PageTarget("ch2_3", target_dir))
    story.append(Paragraph("2.3 Deep Learning Architectures for Violence Recognition", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The breakthrough of Deep Learning in visual computing has fundamentally supplanted handcrafted heuristics. Modern deep neural "
        "networks learn hierarchical feature representations directly from raw pixel data. Within the violence detection literature, "
        "four major architectural families have emerged, as detailed in the subsequent subsections.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 2.2 Box
    story.append(PageTarget("fig_2_2", target_dir))
    fig22_data = [
        [Paragraph("<b>Figure 2.2: Structural Comparison of Deep Learning Video Architectures</b>", styles['BBTableCellBold'])],
        [Paragraph(
            " (A) 2D-CNN (Frame-wise)      (B) 3D-CNN (Spatio-Temporal)    (C) Hybrid CNN-LSTM         (D) Video Transformer\n"
            "   [ Frame t ] -> [ Conv2D ]     [ Cuboid TxFxH ] -> [ Conv3D ]  [ Frame t ] -> [ Conv2D ]   [ Patches ] -> [ Self-Attn ]\n"
            "   [ Frame t+1] -> [ Conv2D ]                                              |\n"
            "          |                              |                                 v                       |\n"
            "          v                              v                           [ LSTM Cell ]                 v\n"
            "   [ Avg / Voting ]              [ Dense Classifier ]                      |              [ MLP Head Classifier ]\n"
            "          |                              |                                 v                       |\n"
            "    P(Violence)                    P(Violence)                       P(Violence)              P(Violence)\n"
            " -----------------------------------------------------------------------------------------------------------------\n"
            " High FPS, Low Latency        Heavy FLOPs, Very Slow         Sequential Dependency        Massive Training Data",
            styles['BBCode']
        )]
    ]
    t_fig22 = Table(fig22_data, colWidths=[450])
    t_fig22.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig22)
    story.append(PageBreak())

    # 2.3.1 2D-CNNs
    story.append(PageTarget("ch2_3_1", target_dir))
    story.append(Paragraph("2.3.1 2D Convolutional Neural Networks (2D-CNNs)", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "2D Convolutional Neural Networks process individual video frames as static 2D spatial matrices. Pioneer models such as "
        "AlexNet, VGG-16, and ResNet-50 demonstrated that deep spatial features capture indicative visual patterns of physical "
        "aggression—including body postures, aggressive gestures, fallen bodies, and visual contact. Transfer learning from models "
        "pre-trained on ImageNet enables 2D-CNNs to generalize exceptionally well even on modest-sized violence datasets. "
        "However, early 2D-CNN implementations evaluated frames one by one through sequential Python iterations, leading to high "
        "CPU-GPU communication overhead and degraded throughput. This limitation is directly solved in our work via 32-frame vectorized batching.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # 2.3.2 3D-CNNs
    story.append(PageTarget("ch2_3_2", target_dir))
    story.append(Paragraph("2.3.2 3D Spatio-Temporal Networks (C3D, I3D, SlowFast)", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "To explicitly model temporal dynamics across consecutive frames, Tran et al. (2015) proposed C3D, expanding standard 2D convolution "
        "kernels into 3D spatio-temporal filters (typically 3x3x3). Carreira and Zisserman (2017) subsequently introduced the Inflated 3D ConvNet "
        "(I3D) by inflating 2D filters trained on ImageNet into 3D spatio-temporal kernels. Feichtenhofer et al. (2019) proposed SlowFast "
        "networks operating with two pathways: a Slow pathway with low frame rate to capture spatial semantics, and a Fast pathway with high "
        "frame rate to capture rapid temporal motion.<br/><br/>"
        "While 3D-CNNs achieve impressive classification scores on benchmark academic clips, they present prohibitive computational "
        "burdens in real-world deployment. A standard I3D model requires over 108 GFLOPs per 64-frame clip and consumes gigabytes of GPU "
        "VRAM. Consequently, 3D-CNNs cannot be scaled across multi-camera municipal networks on commodity compute hardware without "
        "introducing massive processing lag and prohibitive server infrastructure expenses.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # 2.3.3 Recurrent & Hybrid Frameworks
    story.append(PageTarget("ch2_3_3", target_dir))
    story.append(Paragraph("2.3.3 Recurrent & Hybrid Frameworks (CNN-LSTM, ConvLSTM)", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "To decouple spatial feature extraction from temporal sequence modeling, researchers engineered hybrid CNN-LSTM architectures "
        "(Donahue et al., 2015). In this design, a 2D-CNN extracts a compact spatial latent vector for each frame, and a Long Short-Term "
        "Memory (LSTM) or Bidirectional LSTM network models the temporal evolution across successive feature vectors. Shi et al. (2015) "
        "extended this paradigm with ConvLSTM, embedding convolutional operators directly into the recurrent state transitions.<br/><br/>"
        "Although hybrid CNN-LSTMs reduce parameter counts compared to pure 3D-CNNs, their recurrent hidden state dependencies prevent "
        "massively parallel GPU execution. Furthermore, long sequence recurrence introduces gradient vanishing/exploding hazards, and "
        "the models frequently misclassify non-violent burst motions (such as sports celebrations or sudden running) as violent attacks.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # 2.3.4 Vision Transformers
    story.append(PageTarget("ch2_3_4", target_dir))
    story.append(Paragraph("2.3.4 Vision Transformers & Temporal Attention Mechanisms", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "Inspired by the monumental success of Transformers in natural language processing, recent literature has explored pure "
        "self-attention architectures for video analysis, including TimeSformer (Bertasius et al., 2021) and Video Vision Transformer "
        "(ViViT, Arnab et al., 2021). These architectures divide video cuboids into spatio-temporal tokens and compute divided "
        "space-time self-attention.<br/><br/>"
        "Despite their theoretical expressiveness, Vision Transformers suffer from quadratic computational complexity O(N²) relative "
        "to token sequence length, require colossal training datasets (millions of video clips) to prevent overfitting, and exhibit "
        "extreme memory footprints that make real-time edge execution impossible on current commercial surveillance hardware.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    # 2.4 Benchmark Datasets Analysis
    story.append(PageTarget("ch2_4", target_dir))
    story.append(Paragraph("2.4 Benchmark Video Violence Datasets Analysis", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The empirical development and validation of automated violence detection algorithms depend crucially upon curated benchmark "
        "video corpuses. Over the past fifteen years, several benchmark datasets have been released to the research community. "
        "Understanding their respective structural characteristics, strengths, and operational limitations is essential for contextualizing "
        "experimental outcomes.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>1. Hockey Fights Dataset (Nievas et al., 2011):</b> Comprises 1,000 short video clips (500 fight, 500 non-fight) extracted from "
        "National Hockey League (NHL) broadcasts. While widely cited, the dataset suffers from severe domain specificity: all actions "
        "occur on high-contrast white ice rinks with athletes wearing distinct hockey gear, limiting its transferability to urban surveillance.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>2. Movies Violence Dataset (Bermejo et al., 2011):</b> Contains 200 clips extracted from Hollywood movies featuring choreographed "
        "fights and non-violent interactions. The cinematic editing, rapid cuts, artificial lighting, and dramatic camera pans do not "
        "reflect the stationary, wide-angle, low-contrast reality of actual CCTV security cameras.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>3. Real-Life Violence Situations (RLVS) Dataset (Soliman et al., 2019):</b> Contains 2,000 genuine video clips (1,000 violent, "
        "1,000 non-violent) collected from real-world surveillance systems, mobile phone recordings, and public street encounters. "
        "This dataset features authentic street brawls, aggressive assaults, and complex real-world backgrounds, making it an ideal "
        "benchmark for evaluating practical public safety systems.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>4. UCF-Crime Dataset (Sultani et al., 2018):</b> A large-scale untrimmed surveillance anomaly dataset spanning 128 hours of video "
        "across 13 crime categories (Fighting, Robbery, Assault, Burglary, etc.). Videos are long, unconstrained, and exhibit severe real-world "
        "sensor noise and variable frame rates.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>5. RWF-2000 Benchmark (Cheng et al., 2021):</b> Contains 2,000 video clips captured exclusively by real-world surveillance cameras, "
        "specifically designed to challenge algorithms with subtle physical engagements and non-violent dynamic motions.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Table 2.2
    story.append(PageTarget("tab_2_2", target_dir))
    story.append(Paragraph("<b>Table 2.2: Benchmark Violence Datasets Quantitative Specification Comparison</b>", styles['BBSubSectionHeader']))
    tab_d_data = [
        [Paragraph("<b>Dataset Name</b>", styles['BBTableHeader']), Paragraph("<b>Total Clips</b>", styles['BBTableHeader']), Paragraph("<b>Resolution</b>", styles['BBTableHeader']), Paragraph("<b>Average Duration</b>", styles['BBTableHeader']), Paragraph("<b>Domain / Setting</b>", styles['BBTableHeader']), Paragraph("<b>Realism Index</b>", styles['BBTableHeader'])],
        [Paragraph("Hockey Fights", styles['BBTableCellBold']), Paragraph("1,000", styles['BBTableCell']), Paragraph("360 x 288", styles['BBTableCell']), Paragraph("1.5 - 2.5 sec", styles['BBTableCell']), Paragraph("Ice Hockey Arenas", styles['BBTableCell']), Paragraph("Low (Sport Specific)", styles['BBTableCell'])],
        [Paragraph("Movies Dataset", styles['BBTableCellBold']), Paragraph("200", styles['BBTableCell']), Paragraph("720 x 480", styles['BBTableCell']), Paragraph("2.0 - 5.0 sec", styles['BBTableCell']), Paragraph("Cinematic Film Clips", styles['BBTableCell']), Paragraph("Moderate (Staged)", styles['BBTableCell'])],
        [Paragraph("RLVS Dataset", styles['BBTableCellBold']), Paragraph("2,000", styles['BBTableCell']), Paragraph("Various (HQ)", styles['BBTableCell']), Paragraph("3.0 - 7.0 sec", styles['BBTableCell']), Paragraph("Street / CCTV / Mobile", styles['BBTableCell']), Paragraph("High (Authentic)", styles['BBTableCell'])],
        [Paragraph("UCF-Crime", styles['BBTableCellBold']), Paragraph("1,900", styles['BBTableCell']), Paragraph("Various (CCTV)", styles['BBTableCell']), Paragraph("1 - 10 mins", styles['BBTableCell']), Paragraph("Untrimmed Surveillance", styles['BBTableCell']), Paragraph("Very High (CCTV)", styles['BBTableCell'])],
        [Paragraph("RWF-2000", styles['BBTableCellBold']), Paragraph("2,000", styles['BBTableCell']), Paragraph("Various (CCTV)", styles['BBTableCell']), Paragraph("5.0 sec", styles['BBTableCell']), Paragraph("Surveillance Cameras", styles['BBTableCell']), Paragraph("Very High (CCTV)", styles['BBTableCell'])],
    ]
    td_table = Table(tab_d_data, colWidths=[90, 60, 75, 75, 90, 60])
    td_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 1), (3, -1), 'CENTER'),
    ]))
    story.append(td_table)
    story.append(PageBreak())

    # 2.5 Comparative Analysis of Existing Systems (Table 2.1)
    story.append(PageTarget("ch2_5", target_dir))
    story.append(Paragraph("2.5 Comparative Analysis of Contemporary Systems", styles['BBSectionHeader']))
    story.append(Paragraph(
        "To establish a rigorous technical baseline, an exhaustive comparative analysis was conducted evaluating recent peer-reviewed "
        "methodologies published between 2018 and 2026. Table 2.1 analyzes these contemporary works across multiple critical operational "
        "dimensions: primary architecture, reported accuracy, inference throughput (FPS), keyframe evidentiary extraction capability, "
        "video streaming support, and full-stack software integration.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Table 2.1
    story.append(PageTarget("tab_2_1", target_dir))
    story.append(Paragraph("<b>Table 2.1: Exhaustive Comparative Literature Analysis of Video Violence Detection</b>", styles['BBSubSectionHeader']))
    tab21_data = [
        [Paragraph("<b>Author & Year</b>", styles['BBTableHeader']), Paragraph("<b>Architecture / Methodology</b>", styles['BBTableHeader']), Paragraph("<b>Dataset</b>", styles['BBTableHeader']), Paragraph("<b>Accuracy</b>", styles['BBTableHeader']), Paragraph("<b>Throughput (FPS)</b>", styles['BBTableHeader']), Paragraph("<b>Evidence Extraction?</b>", styles['BBTableHeader']), Paragraph("<b>Web Integration?</b>", styles['BBTableHeader'])],
        [Paragraph("Hassner et al. (2012)", styles['BBTableCellBold']), Paragraph("Violent Flows (ViF) + SVM", styles['BBTableCell']), Paragraph("Hockey / Crowd", styles['BBTableCell']), Paragraph("81.3%", styles['BBTableCell']), Paragraph("18.4 FPS", styles['BBTableCell']), Paragraph("No (Binary scalar)", styles['BBTableCell']), Paragraph("No (Offline script)", styles['BBTableCell'])],
        [Paragraph("Sudhakaran et al. (2017)", styles['BBTableCellBold']), Paragraph("ConvLSTM + ResNet-50", styles['BBTableCell']), Paragraph("Hockey Fights", styles['BBTableCell']), Paragraph("87.1%", styles['BBTableCell']), Paragraph("14.2 FPS", styles['BBTableCell']), Paragraph("No (Sequence level)", styles['BBTableCell']), Paragraph("No (Research code)", styles['BBTableCell'])],
        [Paragraph("Carreira et al. (2017)", styles['BBTableCellBold']), Paragraph("Two-Stream Inflated 3D (I3D)", styles['BBTableCell']), Paragraph("Kinetics / UCF", styles['BBTableCell']), Paragraph("89.4%", styles['BBTableCell']), Paragraph("11.8 FPS (GPU)", styles['BBTableCell']), Paragraph("No (Clip score only)", styles['BBTableCell']), Paragraph("No (Jupyter demo)", styles['BBTableCell'])],
        [Paragraph("Soliman et al. (2019)", styles['BBTableCellBold']), Paragraph("VGG-19 + Bi-LSTM", styles['BBTableCell']), Paragraph("RLVS Dataset", styles['BBTableCell']), Paragraph("85.6%", styles['BBTableCell']), Paragraph("16.0 FPS", styles['BBTableCell']), Paragraph("No (Binary label)", styles['BBTableCell']), Paragraph("No (CLI script)", styles['BBTableCell'])],
        [Paragraph("Cheng et al. (2021)", styles['BBTableCellBold']), Paragraph("RWF Optical Flow 3D-CNN", styles['BBTableCell']), Paragraph("RWF-2000", styles['BBTableCell']), Paragraph("87.3%", styles['BBTableCell']), Paragraph("21.5 FPS (GPU)", styles['BBTableCell']), Paragraph("No (Segment label)", styles['BBTableCell']), Paragraph("No (Stand-alone)", styles['BBTableCell'])],
        [Paragraph("Al-Dhamari et al. (2024)", styles['BBTableCellBold']), Paragraph("Spatial Attention ResNet + GRU", styles['BBTableCell']), Paragraph("UCF-Crime / RLVS", styles['BBTableCell']), Paragraph("86.2%", styles['BBTableCell']), Paragraph("24.0 FPS", styles['BBTableCell']), Paragraph("No (Temporal heat)", styles['BBTableCell']), Paragraph("Partial (Flask API)", styles['BBTableCell'])],
        [Paragraph("<b>Proposed System (2027)</b>", styles['BBTableCellBold']), Paragraph("<b>MobileNetV2 + 32-Batch Vectorization</b>", styles['BBTableCellBold']), Paragraph("<b>RLVS / Mixed Surveillance</b>", styles['BBTableCellBold']), Paragraph("<b>86.8%</b>", styles['BBTableCellBold']), Paragraph("<b>114.9 FPS (5.6x)</b>", styles['BBTableCellBold']), Paragraph("<b>YES (Exact Timestamps & Images)</b>", styles['BBTableCellBold']), Paragraph("<b>YES (Next.js 15, HTTP 206)</b>", styles['BBTableCellBold'])],
    ]
    t21 = Table(tab21_data, colWidths=[80, 105, 75, 45, 55, 45, 45])
    t21.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#e0f2fe")), # Highlight proposed system row
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (3, 1), (6, -1), 'CENTER'),
    ]))
    story.append(t21)
    story.append(PageBreak())

    # 2.6 Critical Gaps in Contemporary Literature
    story.append(PageTarget("ch2_6", target_dir))
    story.append(Paragraph("2.6 Critical Gaps in Contemporary Literature", styles['BBSectionHeader']))
    story.append(Paragraph(
        "A rigorous synthesis of the state of the art revealed five persistent, fundamental research gaps that severely obstruct "
        "the operational adoption of automated violence detection in practical surveillance environments:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Gap 1: The Sequential Inference Throughput Bottleneck:</b> Existing deep models evaluate frames in naive iterative loops. "
        "Each frame incurs redundant memory roundtrips between system RAM and GPU VRAM, along with kernel invocation overheads. "
        "This limits throughput to 12-25 FPS, rendering systems incapable of handling multi-camera ingest or high-speed recorded batches.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Gap 2: Complete Absence of Granular Keyframe Evidence:</b> Prior systems treat violence detection as an ungrounded classification "
        "task. A security officer receiving an alert is given no physical frame thumbnails, no millisecond timestamps, and no mechanism "
        "to visually verify the threat without manually scrubbing through hours of raw video.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Gap 3: Temporal Fragmentation of Continuous Incidents:</b> Violent fights are continuous physical events spanning several seconds "
        "or minutes. Existing frame-wise classifiers generate sporadic, jittery predictions—flickering between violent and non-violent "
        "labels across adjacent frames—without a temporal clustering heuristic to synthesize cohesive incident intervals.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Gap 4: Inefficient Video Scrubbing and Ingestion Protocols:</b> Surveillance videos are large binary media files. Conventional "
        "web players require the entire file to be downloaded before seeking, resulting in prolonged browser freezes, high bandwidth "
        "consumption, and terrible user experiences when reviewing critical security events.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>Gap 5: Disconnect between AI Research and Enterprise Software:</b> Academic computer vision papers routinely end at offline "
        "F1-scores calculated in isolated Jupyter notebooks. They lack the enterprise software scaffolding required for actual deployment: "
        "secure role-based authentication, non-repudiation audit logging, persistent database models, and certified PDF dossier generation.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 10))

    # 2.7 Proposed Contributions of Ultimate Precision AI
    story.append(PageTarget("ch2_7", target_dir))
    story.append(Paragraph("2.7 Proposed Contributions of Ultimate Precision AI", styles['BBSectionHeader']))
    story.append(Paragraph(
        "This Capstone Project directly resolves each of the aforementioned gaps through the following novel engineering contributions:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "1. <b>Temporal Vectorized Batching Engine:</b> Replaced sequential frame inference with a 32-frame vectorized batching algorithm "
        "operating via NumPy tensor stacking and compiled TensorFlow kernels, achieving an accelerated throughput of <b>114.9 FPS (5.6x speedup)</b>.<br/>"
        "2. <b>Exact Detected Violent Frames Feature:</b> Engineered an automated keyframe extraction pipeline that saves high-resolution JPEG "
        "thumbnails of detected violent frames to disk, computes exact millisecond timestamps in <code>HH:MM:SS</code> format (e.g. <code>00:00:05</code>), "
        "and binds each frame to its classification confidence probability.<br/>"
        "3. <b>Temporal Interval Clustering & Highlight Synthesis:</b> Implemented a 1.5-second temporal window clustering algorithm that aggregates "
        "discontinuous violent frames into continuous incident intervals and automatically synthesizes a standalone MP4 violent highlight clip.<br/>"
        "4. <b>Dynamic HTTP 206 Byte-Range Video Streaming:</b> Implemented a Next.js dynamic route handler with byte-range negotiation, enabling "
        "instantaneous sub-200ms scrubbing to any timestamp directly from the evidentiary frame gallery.<br/>"
        "5. <b>Enterprise Full-Stack Architecture:</b> Delivered a unified production application utilizing Next.js 15, React 19, TailwindCSS, "
        "MongoDB ODM persistence, and automated forensic PDF reporting via ReportLab.",
        styles['BBBullet']
    ))
    story.append(PageBreak())

    return story
