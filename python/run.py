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

# Load the pretrained neural network model
model = load_model('python/violence_detection_model.h5', custom_objects={'DepthwiseConv2D': FixedDepthwiseConv2D})

def create_video_from_frames(output_path, frames_dir, fps=30, frame_size=(128, 128)):
    image_files = [os.path.join(frames_dir, img)
                   for img in os.listdir(frames_dir)
                   if img.endswith(".jpg")]
    image_files.sort() 

    if not image_files:
        return None
    try:
        clip = ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(output_path, codec="libx264", logger=None)
        return output_path
    except Exception as e:
        print(f"Warning creating highlight clip: {e}", file=sys.stderr)
        return None

def format_time(seconds):
    s = max(0, int(seconds))
    hours = s // 3600
    mins = (s % 3600) // 60
    secs = s % 60
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

def preprocess_image(image_path, frames_dir='public/violent_frames', img_size=(128, 128)):
    norm_frame_dir = os.path.normpath(frames_dir)
    if os.path.exists(norm_frame_dir):
        import shutil
        shutil.rmtree(norm_frame_dir, ignore_errors=True)
    os.makedirs(norm_frame_dir, exist_ok=True)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not open or read image file: {image_path}")

    resized = cv2.resize(img, img_size)
    normalized = resized.astype('float32') / 255.0

    raw_prediction = float(model.predict(np.expand_dims(normalized, axis=0), verbose=0)[0][0])
    confidence_pct = round(raw_prediction * 100, 1)
    is_violent = raw_prediction >= 0.50
    label = "Violent" if is_violent else "Non-Violent"

    saved_frame_path = os.path.normpath(os.path.join(norm_frame_dir, "analyzed_image_0.jpg"))
    cv2.imwrite(saved_frame_path, img)
    rel_frame_path = saved_frame_path.replace('\\', '/')

    detected_frames = []
    if is_violent:
        detected_frames.append({
            "frame_idx": 0,
            "timestamp_seconds": 0.0,
            "timestamp": "00:00:00",
            "confidence": confidence_pct,
            "label": label,
            "image_path": rel_frame_path
        })

    return {
        "media_type": "image",
        "class": label,
        "violence_percentage": confidence_pct if is_violent else 0.0,
        "violent_frames": 1 if is_violent else 0,
        "total_frames": 1,
        "fps": 0,
        "duration": 0,
        "average_confidence": confidence_pct,
        "timeline": [],
        "detected_frames": detected_frames,
        "output_video": None,
        "first_frame": rel_frame_path,
        "last_frame": rel_frame_path,
        "has_bounding_box": False,
        "note": "AI model evaluates whole-frame deep learning features."
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

    norm_frame_dir = os.path.normpath(violent_frame_dir)
    if save_violent_frames:
        if os.path.exists(norm_frame_dir):
            import shutil
            shutil.rmtree(norm_frame_dir, ignore_errors=True)
        os.makedirs(norm_frame_dir, exist_ok=True)

    frame_idx = 0
    total_predictions = []
    batch_size = 32
    batch_frames = []
    batch_meta = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, img_size)
        normalized_frame = resized_frame.astype('float32') / 255.0
        batch_frames.append(normalized_frame)
        batch_meta.append((frame_idx, frame))
        frame_idx += 1

        if len(batch_frames) >= batch_size:
            predictions = model.predict(np.array(batch_frames), batch_size=batch_size, verbose=0)
            for i, pred in enumerate(predictions):
                pred_val = float(pred[0])
                total_predictions.append(pred_val)
                f_idx, orig_frame = batch_meta[i]

                # Classification threshold for violent frames
                if pred_val >= 0.50:
                    violent_frame_path = os.path.normpath(os.path.join(norm_frame_dir, f'violent_frame_{f_idx}.jpg'))
                    cv2.imwrite(violent_frame_path, orig_frame)
                    rel_img_path = violent_frame_path.replace('\\', '/')
                    violent_frames.append(rel_img_path)
                    
                    timestamp_sec = round(f_idx / fps, 2)
                    violent_indices.append((f_idx, timestamp_sec, pred_val))
                    
                    detected_frames_list.append({
                        "frame_idx": f_idx,
                        "timestamp_seconds": timestamp_sec,
                        "timestamp": format_time(timestamp_sec),
                        "confidence": round(pred_val * 100, 1),
                        "label": "Violent",
                        "image_path": rel_img_path
                    })
            batch_frames.clear()
            batch_meta.clear()

    # Process remaining batch frames
    if batch_frames:
        predictions = model.predict(np.array(batch_frames), batch_size=len(batch_frames), verbose=0)
        for i, pred in enumerate(predictions):
            pred_val = float(pred[0])
            total_predictions.append(pred_val)
            f_idx, orig_frame = batch_meta[i]

            if pred_val >= 0.50:
                violent_frame_path = os.path.normpath(os.path.join(norm_frame_dir, f'violent_frame_{f_idx}.jpg'))
                cv2.imwrite(violent_frame_path, orig_frame)
                rel_img_path = violent_frame_path.replace('\\', '/')
                violent_frames.append(rel_img_path)
                
                timestamp_sec = round(f_idx / fps, 2)
                violent_indices.append((f_idx, timestamp_sec, pred_val))
                
                detected_frames_list.append({
                    "frame_idx": f_idx,
                    "timestamp_seconds": timestamp_sec,
                    "timestamp": format_time(timestamp_sec),
                    "confidence": round(pred_val * 100, 1),
                    "label": "Violent",
                    "image_path": rel_img_path
                })
        batch_frames.clear()
        batch_meta.clear()

    cap.release()

    total_frames = len(total_predictions)
    violent_frames_count = len(violent_frames)
    duration_sec = total_frames / fps if fps > 0 else 0

    violence_percentage = round((violent_frames_count / total_frames) * 100, 2) if total_frames > 0 else 0.0
    video_class = "Violent" if violent_frames_count > 0 else "Non-Violent"

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
        try:
            norm_output_vid = os.path.normpath(output_video_path)
            os.makedirs(os.path.dirname(norm_output_vid), exist_ok=True)
            created = create_video_from_frames(norm_output_vid, norm_frame_dir, fps=min(int(fps), 60))
            if created and os.path.exists(norm_output_vid):
                output_video_file = norm_output_vid.replace('\\', '/')
            first_frame = violent_frames[0].replace('\\', '/')
            last_frame = violent_frames[-1].replace('\\', '/')
        except Exception as clip_err:
            print(f"Highlight clip note: {clip_err}", file=sys.stderr)

    return {
        "media_type": "video",
        "class": video_class,
        "violence_percentage": violence_percentage,
        "violent_frames": violent_frames_count,
        "total_frames": total_frames,
        "fps": round(fps, 2),
        "duration": round(duration_sec, 2),
        "average_confidence": round(avg_confidence * 100, 1),
        "timeline": timeline,
        "detected_frames": detected_frames_list,
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
