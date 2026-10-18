const fs = require('fs');
const path = require('path');

async function runTests() {
  console.log("=== STARTING INTEGRATION TESTS ===");

  // 1. Test Image Upload
  console.log("\n--- Testing Image Upload & AI Classification ---");
  const imgPath = path.join(process.cwd(), 'python', 'sample.jpg');
  if (!fs.existsSync(imgPath)) {
    throw new Error("sample.jpg not found at " + imgPath);
  }
  const imgBuffer = fs.readFileSync(imgPath);
  const imgBlob = new Blob([imgBuffer], { type: 'image/jpeg' });
  const imgFormData = new FormData();
  imgFormData.append('file', imgBlob, 'sample.jpg');
  imgFormData.append('userId', 'test_verification_user');
  imgFormData.append('userEmail', 'test@example.com');

  const imgRes = await fetch('http://localhost:3000/api/upload', {
    method: 'POST',
    body: imgFormData,
  });

  if (!imgRes.ok) {
    const errText = await imgRes.text();
    throw new Error(`Image upload failed: HTTP ${imgRes.status} - ${errText}`);
  }

  const imgData = await imgRes.json();
  console.log("Image Upload Result:", {
    _id: imgData.data._id,
    media_type: imgData.data.media_type,
    class: imgData.data.class,
    confidence: imgData.data.average_confidence,
    image_url: imgData.data.image_url,
    detected_frames_count: imgData.data.detected_frames?.length
  });

  if (imgData.data.media_type !== "image") {
    throw new Error(`Expected media_type 'image', got '${imgData.data.media_type}'`);
  }
  if (!imgData.data._id) {
    throw new Error("Expected _id in response");
  }

  const imageReportId = imgData.data._id;

  // 2. Test Video Upload
  console.log("\n--- Testing Video Upload & Frame-by-Frame Detection ---");
  const vidPath = path.join(process.cwd(), 'python', 'sample.mp4');
  if (!fs.existsSync(vidPath)) {
    throw new Error("sample.mp4 not found at " + vidPath);
  }
  const vidBuffer = fs.readFileSync(vidPath);
  const vidBlob = new Blob([vidBuffer], { type: 'video/mp4' });
  const vidFormData = new FormData();
  vidFormData.append('file', vidBlob, 'sample.mp4');
  vidFormData.append('userId', 'test_verification_user');
  vidFormData.append('userEmail', 'test@example.com');

  const vidRes = await fetch('http://localhost:3000/api/upload', {
    method: 'POST',
    body: vidFormData,
  });

  if (!vidRes.ok) {
    const errText = await vidRes.text();
    throw new Error(`Video upload failed: HTTP ${vidRes.status} - ${errText}`);
  }

  const vidData = await vidRes.json();
  console.log("Video Upload Result:", {
    _id: vidData.data._id,
    media_type: vidData.data.media_type,
    class: vidData.data.class,
    violence_percentage: vidData.data.violence_percentage,
    violent_frames: vidData.data.violent_frames,
    total_frames: vidData.data.total_frames,
    detected_frames_count: vidData.data.detected_frames?.length,
    first_detected_frame: vidData.data.detected_frames?.[0],
    last_detected_frame: vidData.data.detected_frames?.[vidData.data.detected_frames.length - 1],
    output_video: vidData.data.output_video
  });

  if (vidData.data.media_type !== "video") {
    throw new Error(`Expected media_type 'video', got '${vidData.data.media_type}'`);
  }
  if (!vidData.data.detected_frames || vidData.data.detected_frames.length === 0) {
    throw new Error("Expected detected_frames array with thumbnails");
  }
  const sampleFrame = vidData.data.detected_frames[0];
  if (typeof sampleFrame.timestampSeconds !== 'number' || !sampleFrame.imageUrl) {
    throw new Error("Invalid detected_frame structure: " + JSON.stringify(sampleFrame));
  }

  const videoReportId = vidData.data._id;

  // 3. Test Fetching Reports by ID from Database
  console.log("\n--- Testing Detection Database Fetch by ID ---");
  const fetchImgRes = await fetch(`http://localhost:3000/api/detections?id=${imageReportId}`);
  const fetchImgData = await fetchImgRes.json();
  console.log("Fetched Image Doc:", {
    id: fetchImgData.detection._id,
    mediaType: fetchImgData.detection.mediaType,
    imageUrl: fetchImgData.detection.imageUrl,
    class: fetchImgData.detection.result?.class
  });

  const fetchVidRes = await fetch(`http://localhost:3000/api/detections?id=${videoReportId}`);
  const fetchVidData = await fetchVidRes.json();
  console.log("Fetched Video Doc:", {
    id: fetchVidData.detection._id,
    mediaType: fetchVidData.detection.mediaType,
    videoUrl: fetchVidData.detection.videoUrl,
    detectedFramesCount: fetchVidData.detection.result?.detectedFrames?.length
  });

  // 4. Test Fetching User Detection History
  console.log("\n--- Testing History API ---");
  const historyRes = await fetch(`http://localhost:3000/api/detections?userId=test_verification_user`);
  const historyData = await historyRes.json();
  console.log(`Found ${historyData.detections?.length} records for user:`, historyData.detections?.map(d => ({
    id: d._id,
    file: d.filename,
    mediaType: d.mediaType,
    class: d.result?.class
  })));

  console.log("\n=== ALL INTEGRATION TESTS PASSED SUCCESSFULLY! ===");
}

runTests().catch((err) => {
  console.error("Test error:", err);
  process.exit(1);
});
