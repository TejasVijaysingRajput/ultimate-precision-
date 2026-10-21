from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def generate_chapter_3(styles, PageTarget, target_dir):
    story = []
    PRIMARY = colors.HexColor("#0f172a")
    SECONDARY = colors.HexColor("#1e3a8a")
    CARD_BORDER = colors.HexColor("#cbd5e1")
    BG_LIGHT = colors.HexColor("#f8fafc")

    # =========================================================================
    # CHAPTER 3: METHODOLOGY AND MATHEMATICAL FORMULATION
    # =========================================================================
    story.append(PageTarget("ch3_start", target_dir))
    story.append(Paragraph("CHAPTER 3", styles['BBTitle24']))
    story.append(Paragraph("METHODOLOGY AND MATHEMATICAL FORMULATION", styles['BBChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=14))

    # 3.1 Overall System Architecture
    story.append(PageTarget("ch3_1", target_dir))
    story.append(Paragraph("3.1 Overall System Architecture & Workflow Pipeline", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The architectural design of <b>Ultimate Precision AI</b> is governed by three primary engineering criteria: "
        "<b>extreme processing throughput</b>, <b>mathematical rigor in decision logic</b>, and <b>uncompromising evidentiary fidelity</b>. "
        "The end-to-end processing pipeline transforms raw, uncompressed surveillance video streams into structured forensic intelligence "
        "through five tightly coupled computational stages: (1) Demuxing and Video Decoding, (2) Spatial Tensor Preprocessing, "
        "(3) Vectorized Batch Deep Neural Inference, (4) Temporal Interval Clustering & Keyframe Extraction, and (5) Forensic Asset Synthesis.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 3.1 Box
    story.append(PageTarget("fig_3_1", target_dir))
    fig31_data = [
        [Paragraph("<b>Figure 3.1: End-to-End Computational Architecture of Ultimate Precision AI</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   [ Input Video: MP4 / AVI ]\n"
            "               |\n"
            "               v\n"
            "   [ OpenCV VideoCapture ] -----> Demux Container, Read FPS, Total Frames, Dimensions (W, H)\n"
            "               |\n"
            "               v\n"
            "   [ Frame Preprocessing ] -----> Bicubic Resize (128x128), BGR-to-RGB, Normalization [0, 1]\n"
            "               |\n"
            "               v\n"
            "   [ Batch Buffer Queue ] ------> Accumulate N = 32 Frames into Tensor Shape [32, 128, 128, 3]\n"
            "               |\n"
            "               v\n"
            "   [ MobileNetV2 Neural Net ] --> Inverted Residuals, Linear Bottlenecks, Depthwise Convolutions\n"
            "               |\n"
            "               v\n"
            "   [ Batch Softmax Logits ] ----> Parallel Vectorized Output: P(Violence | Frame_i), for i=1..32\n"
            "               |\n"
            "               +----------------------------------+----------------------------------+\n"
            "               |                                                                     |\n"
            "               v                                                                     v\n"
            "   [ Keyframe Extraction ]                                              [ Temporal Clustering Engine ]\n"
            "   - Threshold >= 0.50                                                  - Cluster frames if delta <= 1.5s\n"
            "   - Save Frame JPEG: `frame_N.jpg`                                     - Synthesize Highlight Interval Bounds\n"
            "   - Timestamp: `00:00:05` (HH:MM:SS)                                   - cv2.VideoWriter stitches `highlight.mp4`\n"
            "               |                                                                     |\n"
            "               +----------------------------------+----------------------------------+\n"
            "                                                  |\n"
            "                                                  v\n"
            "                                     [ JSON Intelligence Payload ]\n"
            "                                     - Status: VIOLENT / NON-VIOLENT\n"
            "                                     - Confidence Score & Duration\n"
            "                                     - Array of `detected_frames` with Timestamps\n"
            "                                     - Stored in MongoDB & Served via Next.js 15",
            styles['BBCode']
        )]
    ]
    t_fig31 = Table(fig31_data, colWidths=[450])
    t_fig31.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig31)
    story.append(PageBreak())

    # 3.2 Video Ingestion, Demuxing, and Decoding
    story.append(PageTarget("ch3_2", target_dir))
    story.append(Paragraph("3.2 Video Ingestion, Demuxing, and Decoding via OpenCV", styles['BBSectionHeader']))
    story.append(Paragraph(
        "The ingestion pipeline interfaces with the physical file system using an optimized OpenCV (<code>cv2.VideoCapture</code>) "
        "backend. Upon receiving the absolute path of an uploaded surveillance video, the pipeline extracts structural container metadata "
        "including the native frame rate ($F_{fps}$), spatial resolution ($W_{orig} \\times H_{orig}$), and total frame count ($N_{total}$). "
        "The continuous temporal duration ($T_{total}$) in seconds is computed as:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$T_{total} = \\frac{N_{total}}{F_{fps}}$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "Decoding occurs frame-by-frame via hardware-accelerated FFmpeg native decoders. To safeguard against corrupted containers, "
        "truncated byte streams, or malformed keyframe headers, each frame read invocation is validated using defensive boundary guards. "
        "If a frame read returns false or yields a null pointer, the pipeline gracefully flushes any remaining buffered tensors and completes execution.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # 3.3 Spatial Preprocessing and Normalization
    story.append(PageTarget("ch3_3", target_dir))
    story.append(Paragraph("3.3 Spatial Preprocessing, Bicubic Resizing, and Tensor Normalization", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Raw surveillance frames captured from high-definition security cameras typically possess resolutions ranging from 1080p "
        "($1920 \\times 1080$) to 4K ($3840 \\times 2160$). Ingesting these native dimensions directly into a deep neural network "
        "would cause catastrophic memory exhaustion and crippling computational delays without yielding meaningful improvements in "
        "violence classification accuracy. Therefore, each decoded frame undergoes a rigorous three-step mathematical transformation:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>1. Color Space Conversion:</b> OpenCV natively reads pixel values in Blue-Green-Red (BGR) channel ordering. The tensor is "
        "converted to standard Red-Green-Blue (RGB) representation using the affine transformation matrix:<br/>"
        "$$I_{RGB}(x, y) = \\mathcal{T}_{BGR \\to RGB}(I_{BGR}(x, y))$$",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>2. Bicubic Spatial Downsampling:</b> The spatial dimensions are resized to standard model input dimensions ($W_{in} = 128, "
        "H_{in} = 128$) using bicubic interpolation over a $4 \\times 4$ pixel neighborhood, preserving essential motion edge gradients "
        "while eliminating high-frequency sensor noise.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>3. Floating-Point Min-Max Normalization:</b> The unsigned integer pixel intensities ($p \\in [0, 255]$) are mapped into a standardized "
        "floating-point interval $[0.0, 1.0]$ via element-wise scalar division:<br/>"
        "$$\\hat{I}_{norm}(x, y, c) = \\frac{I_{RGB}(x, y, c)}{255.0}, \\quad \\forall c \\in \\{R, G, B\\}$$",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # Table 3.1
    story.append(PageTarget("tab_3_1", target_dir))
    story.append(Paragraph("<b>Table 3.1: Mathematical Parameter Notations and Dimension Specifications</b>", styles['BBSubSectionHeader']))
    tab31_data = [
        [Paragraph("<b>Mathematical Symbol</b>", styles['BBTableHeader']), Paragraph("<b>Description / Definition</b>", styles['BBTableHeader']), Paragraph("<b>Standard Nominal Value</b>", styles['BBTableHeader'])],
        [Paragraph("$F_{fps}$", styles['BBTableCellBold']), Paragraph("Native Video Frame Rate (frames per second)", styles['BBTableCell']), Paragraph("25.0 - 30.0 FPS", styles['BBTableCell'])],
        [Paragraph("$W_{in}, H_{in}$", styles['BBTableCellBold']), Paragraph("Spatial Tensor Input Dimensions (Width, Height)", styles['BBTableCell']), Paragraph("128 x 128 pixels", styles['BBTableCell'])],
        [Paragraph("$C_{channels}$", styles['BBTableCellBold']), Paragraph("Color Channel Depth (Red, Green, Blue)", styles['BBTableCell']), Paragraph("3 channels (RGB)", styles['BBTableCell'])],
        [Paragraph("$B_{size}$", styles['BBTableCellBold']), Paragraph("Vectorized Batch Processing Size", styles['BBTableCell']), Paragraph("32 frames per batch", styles['BBTableCell'])],
        [Paragraph("$\\theta_{conf}$", styles['BBTableCellBold']), Paragraph("Violent Event Decision Confidence Threshold", styles['BBTableCell']), Paragraph("0.50 (50.0% probability)", styles['BBTableCell'])],
        [Paragraph("$\\Delta t_{cluster}$", styles['BBTableCellBold']), Paragraph("Maximum Temporal Cluster Merging Window", styles['BBTableCell']), Paragraph("1.50 seconds", styles['BBTableCell'])],
    ]
    t31 = Table(tab31_data, colWidths=[110, 230, 110])
    t31.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t31)
    story.append(PageBreak())

    # 3.4 Temporal Vectorized Batch Processing Algorithm
    story.append(PageTarget("ch3_4", target_dir))
    story.append(Paragraph("3.4 Temporal Vectorized Batch Processing Algorithm", styles['BBSectionHeader']))
    story.append(Paragraph(
        "A critical innovation of this research is the replacement of conventional sequential frame inference with a synchronized "
        "<b>temporal vectorized batch processing algorithm</b>. In naive implementations, each video frame is dispatched individually "
        "to the neural network runtime:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\text{Naive Sequential Loop:} \\quad y_t = f_{model}(x_t), \\quad \\text{for } t = 1, 2, \\dots, N_{total}$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "In sequential execution, each invocation incurs substantial operating system context-switching overhead, memory bus transfers "
        "between host CPU RAM and device cache, and dispatch latency for GPU compute kernels. When processing a 3-minute video at 30 FPS "
        "($5,400$ frames), sequential inference executes $5,400$ discrete kernel invocations, capping throughput at a dismal 15-20 FPS.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # 3.4.1 Mathematical Formulation of Batching Speedup
    story.append(PageTarget("ch3_4_1", target_dir))
    story.append(Paragraph("3.4.1 Mathematical Formulation of Batching Speedup", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "To eliminate this overhead, our engine structures the incoming frame queue into dense 4-dimensional tensors of size "
        "$\\mathcal{B} \\in \\mathbb{R}^{B_{size} \\times H_{in} \\times W_{in} \\times C}$, where $B_{size} = 32$. Let $T_{seq}$ represent "
        "the total latency of processing $N$ frames sequentially, and $T_{batch}$ represent the vectorized batch latency:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$T_{seq} = \\sum_{i=1}^{N} \\left( t_{transfer} + t_{kernel} + t_{overhead} \\right) = N \\cdot (t_{transfer} + t_{kernel} + t_{overhead})$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "By contrast, grouping $B$ frames into a single vectorized tensor amortizes the kernel launch and memory bus transaction costs over $B$ items:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$T_{batch} = \\frac{N}{B} \\cdot \\left( t_{transfer}(B) + t_{kernel}(B) + t_{overhead} \\right)$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "Because modern SIMD (Single Instruction, Multiple Data) CPU vector registers and GPU streaming multiprocessors (SMs) execute "
        "matrix multiplications in parallel across tensor dimensions, $t_{kernel}(B) \\ll B \\cdot t_{kernel}(1)$. The resulting theoretical "
        "acceleration factor $\\mathcal{S}_{batch}$ is expressed as:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\mathcal{S}_{batch} = \\frac{T_{seq}}{T_{batch}} \\approx \\frac{B \\cdot t_{overhead}}{t_{overhead} + \\epsilon} \\approx \\mathcal{O}(B)$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "Empirical benchmarks detailed in Chapter 5 confirm that configuring $B_{size} = 32$ achieves an actual <b>5.6x speedup</b>, "
        "elevating processing throughput from 20.4 FPS to <b>114.9 FPS</b>.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 3.2 Box
    story.append(PageTarget("fig_3_2", target_dir))
    fig32_data = [
        [Paragraph("<b>Figure 3.2: Temporal Vectorized 32-Frame Batch Ingestion and Tensor Formation</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   Frames Stream: [ f_1, f_2, f_3, ..., f_32 ]  --> Accumulate into Python List of Arrays\n"
            "                                   |\n"
            "                                   v\n"
            "       [ np.asarray(batch_frames, dtype=np.float32) ]  --> Fast C-Contiguous Memory Block\n"
            "                                   |\n"
            "                                   v\n"
            "       Batch Tensor: Shape (32, 128, 128, 3) --> Transferred via Single PCIe Memory Copy\n"
            "                                   |\n"
            "                                   v\n"
            "       [ model.predict(batch_tensor, batch_size=32) ] --> Single Vectorized BLAS GEMM Kernel\n"
            "                                   |\n"
            "                                   v\n"
            "       Predictions Array: Shape (32, 2) --> [[P_v1, P_nv1], [P_v2, P_nv2], ..., [P_v32, P_nv32]]",
            styles['BBCode']
        )]
    ]
    t_fig32 = Table(fig32_data, colWidths=[450])
    t_fig32.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig32)
    story.append(PageBreak())

    # 3.5 Deep Neural Network Architecture: MobileNetV2
    story.append(PageTarget("ch3_5", target_dir))
    story.append(Paragraph("3.5 Deep Neural Network Architecture: MobileNetV2 Transfer Learning", styles['BBSectionHeader']))
    story.append(Paragraph(
        "To achieve real-time execution without sacrificing semantic feature discriminability, our system employs an optimized "
        "<b>MobileNetV2</b> convolutional neural network backbone (Sandler et al., 2018). MobileNetV2 was chosen over bulkier architectures "
        "(such as ResNet-50 or VGG-16) due to its revolutionary balance of high top-1 classification accuracy and minimal computational complexity.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # 3.5.1 Inverted Residuals & Linear Bottlenecks
    story.append(PageTarget("ch3_5_1", target_dir))
    story.append(Paragraph("3.5.1 Inverted Residuals and Linear Bottlenecks", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "Standard residual bottleneck architectures (such as ResNet) utilize a wide $\\to$ narrow $\\to$ wide channel topology: "
        "they compress high-dimensional representations into a low-dimensional bottleneck before expanding them back. However, Sandler et al. "
        "discovered that applying non-linear activation functions (such as ReLU) directly to low-dimensional manifolds destroys crucial "
        "visual information. MobileNetV2 solves this through two revolutionary design concepts:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>1. Inverted Residual Connections:</b> The network connects skip connections directly between thin bottleneck layers. "
        "The intermediate layer expands the feature channels by an expansion factor $t=6$, computes depthwise spatial convolutions in "
        "high-dimensional space, and then projects the features back down to a compact bottleneck representation.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<b>2. Linear Bottleneck Activations:</b> To prevent non-linearities from destroying the manifold of interest, the final projection "
        "convolution in each bottleneck block uses a linear activation rather than a rectified linear unit (ReLU6), preserving rich "
        "visual descriptors of fast motion and interpersonal physical contact.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 3.3 Box
    story.append(PageTarget("fig_3_3", target_dir))
    fig33_data = [
        [Paragraph("<b>Figure 3.3: Micro-Architecture of MobileNetV2 Inverted Residual Bottleneck Block</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   Input Tensor: [ H x W x k ]  (Low-dimensional Bottleneck)\n"
            "             |\n"
            "             +---------------------------------------------+ (Residual Skip Connection: Stride=1)\n"
            "             |                                             |\n"
            "             v                                             |\n"
            "   [ 1x1 Conv2D (Expansion) ] --> Channels: k * t (t=6)    |\n"
            "   [ Batch Normalization ] + [ ReLU6 Activation ]          |\n"
            "             |\n"
            "             v                                             |\n"
            "   [ 3x3 Depthwise Conv2D ] --> Spatial Filtering          |\n"
            "   [ Batch Normalization ] + [ ReLU6 Activation ]          |\n"
            "             |\n"
            "             v                                             |\n"
            "   [ 1x1 Conv2D (Linear Projection) ] --> Channels: k'     |\n"
            "   [ Batch Normalization ] (NO Non-Linearity)              |\n"
            "             |\n"
            "             v                                             |\n"
            "       [ Add (+) ] <---------------------------------------+\n"
            "             |\n"
            "             v\n"
            "   Output Tensor: [ H' x W' x k' ]",
            styles['BBCode']
        )]
    ]
    t_fig33 = Table(fig33_data, colWidths=[450])
    t_fig33.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig33)
    story.append(PageBreak())

    # 3.5.2 Depthwise Separable Convolutions
    story.append(PageTarget("ch3_5_2", target_dir))
    story.append(Paragraph("3.5.2 Depthwise Separable Convolution vs Standard 2D Convolution", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "The computational efficiency of MobileNetV2 stems from replacing standard 2D convolutions with <b>depthwise separable convolutions</b>. "
        "A standard convolution layer applies a spatial kernel across all input channels simultaneously. Let $D_K$ denote the kernel size "
        "(e.g., $3 \\times 3$), $D_F$ denote the output feature map size, $M$ denote the number of input channels, and $N$ denote the number "
        "of output channels. The computational cost (FLOPs) of a standard convolution is:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\text{Cost}_{standard} = D_K \\cdot D_K \\cdot M \\cdot N \\cdot D_F \\cdot D_F$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "Depthwise separable convolution factors this operation into two distinct stages: (1) a <b>depthwise convolution</b> that applies "
        "a single $D_K \\times D_K$ spatial filter per input channel, followed by (2) a <b>pointwise $1 \\times 1$ convolution</b> that linearly "
        "combines channel representations. The total computational cost is:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\text{Cost}_{separable} = D_K \\cdot D_K \\cdot M \\cdot D_F \\cdot D_F + M \\cdot N \\cdot D_F \\cdot D_F$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "The ratio of computational complexity reduction is mathematically derived as:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\text{Reduction Ratio} = \\frac{D_K \\cdot D_K \\cdot M \\cdot D_F^2 + M \\cdot N \\cdot D_F^2}{D_K \\cdot D_K \\cdot M \\cdot N \\cdot D_F^2} = \\frac{1}{N} + \\frac{1}{D_K^2}$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "For standard $3 \\times 3$ convolutional filters ($D_K = 3$), $\\frac{1}{D_K^2} = \\frac{1}{9} \\approx 0.111$. When $N$ is large "
        "(e.g., $N=128$ or $256$), $\\frac{1}{N} \\to 0$. Consequently, depthwise separable convolutions achieve an <b>8 to 9-fold reduction "
        "in computational FLOPs</b> with virtually no degradation in feature representational power.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 6))

    # Table 3.2
    story.append(PageTarget("tab_3_2", target_dir))
    story.append(Paragraph("<b>Table 3.2: Computational Complexity: Standard 2D Conv vs Depthwise Separable Conv</b>", styles['BBSubSectionHeader']))
    tab32_data = [
        [Paragraph("<b>Convolution Type</b>", styles['BBTableHeader']), Paragraph("<b>Spatial Kernel</b>", styles['BBTableHeader']), Paragraph("<b>FLOPs Formula</b>", styles['BBTableHeader']), Paragraph("<b>Nominal FLOPs (M=64, N=128)</b>", styles['BBTableHeader']), Paragraph("<b>Relative Efficiency</b>", styles['BBTableHeader'])],
        [Paragraph("Standard 2D Conv", styles['BBTableCellBold']), Paragraph("3 x 3", styles['BBTableCell']), Paragraph("$D_K^2 \\cdot M \\cdot N \\cdot D_F^2$", styles['BBTableCell']), Paragraph("117.96 MFLOPs", styles['BBTableCell']), Paragraph("1.0x (Baseline)", styles['BBTableCell'])],
        [Paragraph("Depthwise Conv", styles['BBTableCellBold']), Paragraph("3 x 3 (per channel)", styles['BBTableCell']), Paragraph("$D_K^2 \\cdot M \\cdot D_F^2$", styles['BBTableCell']), Paragraph("9.21 MFLOPs", styles['BBTableCell']), Paragraph("12.8x Lighter", styles['BBTableCell'])],
        [Paragraph("Pointwise Conv", styles['BBTableCellBold']), Paragraph("1 x 1", styles['BBTableCell']), Paragraph("$M \\cdot N \\cdot D_F^2$", styles['BBTableCell']), Paragraph("13.10 MFLOPs", styles['BBTableCell']), Paragraph("9.0x Lighter", styles['BBTableCell'])],
        [Paragraph("<b>Depthwise Separable (Total)</b>", styles['BBTableCellBold']), Paragraph("<b>Hybrid 3x3 + 1x1</b>", styles['BBTableCellBold']), Paragraph("<b>$\\text{Cost}_{DW} + \\text{Cost}_{PW}$</b>", styles['BBTableCellBold']), Paragraph("<b>22.31 MFLOPs</b>", styles['BBTableCellBold']), Paragraph("<b>5.3x Total Savings</b>", styles['BBTableCellBold'])],
    ]
    t32 = Table(tab32_data, colWidths=[105, 75, 120, 95, 55])
    t32.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('GRID', (0, 0), (-1, -1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#e0f2fe")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
    ]))
    story.append(t32)
    story.append(PageBreak())

    # 3.5.3 Custom Head Classification Layers & Regularization
    story.append(PageTarget("ch3_5_3", target_dir))
    story.append(Paragraph("3.5.3 Custom Head Classification Layers & Regularization", styles['BBSubSectionHeader']))
    story.append(Paragraph(
        "The pre-trained MobileNetV2 base acts as a generic spatial feature extractor. We truncate the original 1000-class ImageNet "
        "dense head and append a specialized, regularized violence classification head comprising:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "1. <b>Global Average Pooling 2D:</b> Collapses spatial feature dimensions from $4 \\times 4 \\times 1280$ into a compact 1280-dimensional "
        "latent representation vector $\\mathbf{z} \\in \\mathbb{R}^{1280}$, rendering the architecture invariant to spatial translation.<br/>"
        "2. <b>Dropout Layer ($p=0.40$):</b> Stochastically zeroes out 40% of hidden activations during training, breaking co-adaptation "
        "and preventing overfitting on subtle visual backgrounds.<br/>"
        "3. <b>Dense Layer (128 units, ReLU):</b> Projects the latent representation into a refined non-linear feature space.<br/>"
        "4. <b>Batch Normalization:</b> Stabilizes internal covariate shift across training mini-batches.<br/>"
        "5. <b>Softmax Output Layer:</b> Computes normalized posterior class probabilities for binary classification:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$P(y = \\text{Violent} \\mid \\mathbf{x}) = \\frac{e^{z_{v}}}{e^{z_{v}} + e^{z_{nv}}}$$",
        styles['BBCallout']
    ))
    story.append(Spacer(1, 10))

    # 3.6 Classification Confidence & Heuristics
    story.append(PageTarget("ch3_6", target_dir))
    story.append(Paragraph("3.6 Classification Confidence, Dynamic Thresholding, and Heuristics", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Surveillance environments exhibit high background variability. To suppress false positive detections generated by benign "
        "motion or brief optical glitches, the pipeline applies a dual-threshold heuristic:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "• <b>Frame-Level Threshold ($\\theta_{frame} = 0.50$):</b> A frame $f_i$ is flagged as violent if and only if $P(Violent \\mid f_i) \\ge 0.50$.<br/>"
        "• <b>Session Aggregation Confidence:</b> The overall session violence confidence $C_{session}$ is calculated as the mean confidence "
        "across all detected violent frames. If no violent frames are detected, $C_{session}$ defaults to the global maximum non-violent probability.<br/>"
        "• <b>Categorical Status Assignment:</b> If the count of detected violent frames $N_{violent} \\ge 1$, the video session status is "
        "categorically assigned as <b>VIOLENT</b>; otherwise, it is assigned as <b>NON-VIOLENT</b>.",
        styles['BBBullet']
    ))
    story.append(PageBreak())

    # 3.7 Temporal Clustering Algorithm
    story.append(PageTarget("ch3_7", target_dir))
    story.append(Paragraph("3.7 Temporal Clustering of Continuous Violent Episodes (1.5s Interval)", styles['BBSectionHeader']))
    story.append(Paragraph(
        "In physical assaults, camera angles and rapid movements often cause transient occlusions where violence classification "
        "momentarily drops below the threshold for several frames before re-escalating. Treating these disconnected detections as separate "
        "security incidents would overwhelm operators with fragmented notifications. To solve this, our system introduces a "
        "<b>Temporal Clustering Algorithm</b> that merges adjacent violent frame detections within a 1.5-second temporal window.",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "Let $\\{t_1, t_2, \\dots, t_k\\}$ represent the discrete timestamps of detected violent frames in ascending order. "
        "The clustering algorithm iterates through the temporal sequence: if $t_{i+1} - t_i \\le 1.50\\text{ seconds}$, frame $t_{i+1}$ "
        "is merged into the current incident cluster. Otherwise, the current cluster is closed, and a new incident episode is initialized.",
        styles['BBBodyIndent']
    ))
    story.append(Spacer(1, 8))

    # Figure 3.5 Box
    story.append(PageTarget("fig_3_5", target_dir))
    fig35_data = [
        [Paragraph("<b>Figure 3.5: Temporal Clustering Algorithm Merging Contiguous Frames within 1.5s Delta</b>", styles['BBTableCellBold'])],
        [Paragraph(
            "   Detected Frames:  f(00:03) ---- [Delta = 0.8s <= 1.5s] ----> f(00:03.8) ---- [Delta = 1.1s <= 1.5s] ----> f(00:04.9)\n"
            "                                  |\n"
            "                                  v\n"
            "             [ Incident Cluster 1: Start = 00:00:03.00, End = 00:00:04.90 ]\n"
            "             =============================================================\n"
            "             Gap: Delta = 12.5 seconds (> 1.5s) --> Cluster 1 Closed\n"
            "             =============================================================\n"
            "   Next Detection:   f(00:17.4) ---- [Delta = 0.5s <= 1.5s] ----> f(00:17.9)\n"
            "                                  |\n"
            "                                  v\n"
            "             [ Incident Cluster 2: Start = 00:00:17.40, End = 00:00:17.90 ]",
            styles['BBCode']
        )]
    ]
    t_fig35 = Table(fig35_data, colWidths=[450])
    t_fig35.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, CARD_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fig35)
    story.append(Spacer(1, 12))

    # 3.8 Exact Keyframe Extraction & Timestamps
    story.append(PageTarget("ch3_8", target_dir))
    story.append(Paragraph("3.8 Exact Physical Keyframe Extraction & Millisecond Timestamps", styles['BBSectionHeader']))
    story.append(Paragraph(
        "Whenever a frame exceeds the violence confidence threshold ($\\theta_{conf} \\ge 0.50$), the engine extracts the actual "
        "unmodified visual frame directly from the decoding buffer and persists it to disk as a high-quality JPEG asset inside "
        "the session's upload directory (e.g., <code>public/uploads/session_id/frame_142.jpg</code>). The exact presentation timestamp "
        "is mathematically derived from the frame index and native frame rate:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "$$\\text{Timestamp (seconds)} = \\frac{\\text{Frame Index}}{F_{fps}}, \\quad \\text{Timestamp (HH:MM:SS)} = \\text{format\\_time}\\left(\\frac{\\text{Frame Index}}{F_{fps}}\\right)$$",
        styles['BBCallout']
    ))
    story.append(Paragraph(
        "For example, a frame detected at index 150 in a 30 FPS video is mapped to exact timestamp <code>00:00:05</code>. "
        "Crucially, the file system path, relative web URL, formatted timestamp string, raw seconds float, and classification confidence "
        "are encapsulated into a structured JSON record:",
        styles['BBBodyIndent']
    ))
    story.append(Paragraph(
        "<code>{\"frame_index\": 150, \"timestamp\": \"00:00:05\", \"timestamp_sec\": 5.0, \"confidence\": 0.942, \"url\": \"/uploads/.../frame_150.jpg\"}</code>",
        styles['BBCode']
    ))
    story.append(Spacer(1, 10))

    # 3.9 Automated Violent Highlight Synthesis Pipeline
    story.append(PageTarget("ch3_9", target_dir))
    story.append(Paragraph("3.9 Automated Violent Highlight Synthesis Pipeline", styles['BBSectionHeader']))
    story.append(Paragraph(
        "To provide executive security leadership with an instant overview of an incident without requiring review of extensive "
        "inactive footage, the pipeline automatically stitches all detected violent frames into a condensed MP4 highlight video "
        "(<code>highlight.mp4</code>). The highlight clip is encoded using OpenCV's <code>cv2.VideoWriter</code> with standard <code>mp4v</code> "
        "fourcc codec parameters at native framerate, creating an immediate, shareable forensic summary.",
        styles['BBBodyIndent']
    ))
    story.append(PageBreak())

    return story
