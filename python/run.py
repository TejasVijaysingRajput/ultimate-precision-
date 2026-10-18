import os
import sys
import cv2
import json
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D

class FixedDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop('groups', None)
        super().__init__(*args, **kwargs)

# Load the model
model = load_model('python/violence_detection_model.h5', custom_objects={'DepthwiseConv2D': FixedDepthwiseConv2D})

def create_video_from_frames(output_path, frames_dir, fps=30, frame_size=(128, 128)):
    image_files = [os.path.join(frames_dir, img)
                   for img in os.listdir(frames_dir)
                   if img.endswith(".jpg")]
    image_files.sort() 

    if not image_files:
        print("No images found in the directory!", file=sys.stderr)
        return None
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_path, codec="libx264", logger=None)


def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def preprocess_image(image_path, frames_dir='public/violent_frames', img_size=(128, 128)):
    if os.path.exists(frames_dir):
        import shutil
        shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not open or read image file: {image_path}")

    resized = cv2.resize(img, img_size)
    normalized = resized.astype('float32') / 255.0

    raw_prediction = float(model.predict(np.expand_dims(normalized, axis=0), verbose=0)[0][0])
    confidence_pct = round(raw_prediction * 100, 2)
    is_violent = raw_prediction > 0.5
    label = "Violent" if is_violent else "Non-Violent"

    saved_frame_path = os.path.join(frames_dir, "analyzed_image_0.jpg").replace('\\', '/')
    cv2.imwrite(saved_frame_path, img)

    detected_frame = {
        "frame_idx": 0,
        "timestamp_seconds": 0.0,
        "timestamp": "00:00",
        "confidence": confidence_pct,
        "label": label,
        "image_path": saved_frame_path
    }

    return {
        "media_type": "image",
        "class": label,
        "violence_percentage": confidence_pct,
        "violent_frames": 1 if is_violent else 0,
        "total_frames": 1,
        "fps": 0,
        "duration": 0,
        "average_confidence": confidence_pct,
        "timeline": [],
        "detected_frames": [detected_frame],
        "output_video": None,
        "first_frame": saved_frame_path,
        "last_frame": saved_frame_path,
        "has_bounding_box": False,
        "note": "Existing AI model performs whole-frame classification; no spatial bounding boxes are output."
    }

def preprocess_video(video_path, violent_frame_dir='public/violent_frames', output_video_path='public/violent_video.mp4', img_size=(128, 128), save_violent_frames=True):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0 or np.isnan(fps):
        fps = 30.0

    violent_frames = []
    violent_indices = []
    detected_frames_list = []

    if save_violent_frames:
        if os.path.exists(violent_frame_dir):
            import shutil
            shutil.rmtree(violent_frame_dir, ignore_errors=True)
        os.makedirs(violent_frame_dir, exist_ok=True)

    frame_idx = 0
    total_predictions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, img_size)
        normalized_frame = resized_frame.astype('float32') / 255.0

        if save_violent_frames:
            prediction = float(model.predict(np.expand_dims(normalized_frame, axis=0), verbose=0)[0][0])
            total_predictions.append(prediction)
            if prediction > 0.2:  
                violent_frame_path = os.path.join(violent_frame_dir, f'violent_frame_{frame_idx}.jpg').replace('\\', '/')
                cv2.imwrite(violent_frame_path, frame)
                violent_frames.append(violent_frame_path)
                timestamp_sec = round(frame_idx / fps, 2)
                violent_indices.append((frame_idx, timestamp_sec, prediction))
                
                label = "Violent" if prediction > 0.5 else "Potential Violence"
                detected_frames_list.append({
                    "frame_idx": frame_idx,
                    "timestamp_seconds": timestamp_sec,
                    "timestamp": format_time(timestamp_sec),
                    "confidence": round(prediction * 100, 1),
                    "label": label,
                    "image_path": violent_frame_path
                })

        frame_idx += 1

    cap.release()

    total_frames = len(total_predictions)
    violent_frames_count = len(violent_frames)
    duration_sec = total_frames / fps if fps > 0 else 0

    violence_percentage = (violent_frames_count / total_frames) * 100 if total_frames > 0 else 0
    video_class = "Violent" if violence_percentage > 50 else "Non-Violent"

    # Group timestamps into incident timeline
    timeline = []
    if violent_indices:
        curr_segment = [violent_indices[0]]
        for item in violent_indices[1:]:
            if item[1] - curr_segment[-1][1] <= 1.5:
                curr_segment.append(item)
            else:
                s_sec = curr_segment[0][1]
                e_sec = curr_segment[-1][1]
                avg_c = sum(x[2] for x in curr_segment) / len(curr_segment)
                timeline.append({
                    "start": format_time(s_sec),
                    "end": format_time(e_sec),
                    "startSeconds": round(s_sec, 2),
                    "endSeconds": round(e_sec, 2),
                    "confidence": round(float(avg_c) * 100, 1),
                    "frameCount": len(curr_segment)
                })
                curr_segment = [item]
        if curr_segment:
            s_sec = curr_segment[0][1]
            e_sec = curr_segment[-1][1]
            avg_c = sum(x[2] for x in curr_segment) / len(curr_segment)
            timeline.append({
                "start": format_time(s_sec),
                "end": format_time(e_sec),
                "startSeconds": round(s_sec, 2),
                "endSeconds": round(e_sec, 2),
                "confidence": round(float(avg_c) * 100, 1),
                "frameCount": len(curr_segment)
            })

    avg_confidence = (sum(x[2] for x in violent_indices) / len(violent_indices)) if violent_indices else 0.0

    output_video_file = None
    first_frame = None
    last_frame = None

    if violent_frames:
        os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
        create_video_from_frames(output_video_path, violent_frame_dir, fps=min(int(fps), 60))
        output_video_file = output_video_path.replace('\\', '/')
        first_frame = violent_frames[0].replace('\\', '/')
        last_frame = violent_frames[-1].replace('\\', '/')

    # Ensure chronological order and smart sampling if more than 60 frames
    if len(detected_frames_list) > 60:
        step = len(detected_frames_list) / 60.0
        sampled_indices = set()
        for i in range(60):
            idx = int(round(i * step))
            if idx < len(detected_frames_list):
                sampled_indices.add(idx)
        # Always include highest confidence frames
        top_indices = sorted(range(len(detected_frames_list)), key=lambda k: detected_frames_list[k]["confidence"], reverse=True)[:10]
        for tidx in top_indices:
            sampled_indices.add(tidx)
        sorted_sampled = sorted(list(sampled_indices))
        final_detected_frames = [detected_frames_list[i] for i in sorted_sampled]
    else:
        final_detected_frames = detected_frames_list

    return {
        "media_type": "video",
        "class": video_class,
        "violence_percentage": round(violence_percentage, 2),
        "violent_frames": violent_frames_count,
        "total_frames": total_frames,
        "fps": round(fps, 2),
        "duration": round(duration_sec, 2),
        "average_confidence": round(avg_confidence * 100, 1),
        "timeline": timeline,
        "detected_frames": final_detected_frames,
        "output_video": output_video_file,
        "first_frame": first_frame,
        "last_frame": last_frame
    }


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

if __name__ == "__main__":
    media_path = sys.argv[1] if len(sys.argv) > 1 else "python/video.mp4"
    frames_dir = sys.argv[2] if len(sys.argv) > 2 else "public/violent_frames"
    output_vid = sys.argv[3] if len(sys.argv) > 3 else "public/violent_video.mp4"

    ext = os.path.splitext(media_path)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        res = preprocess_image(media_path, frames_dir=frames_dir)
    else:
        res = preprocess_video(media_path, violent_frame_dir=frames_dir, output_video_path=output_vid)
    print(json.dumps(res, indent=4))
