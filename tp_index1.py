import os
import cv2
import json
import subprocess
import ffmpeg
import whisper
from ultralytics import YOLO

# === CONFIGURATION ===
VIDEOS_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\videos"
FRAMES_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\frames"
DETECTED_FRAMES_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\detected_frames"
AUDIO_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\audios"
RESULTS_JSON = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\results.json"
FRAME_INTERVAL = 30  # Extract frames every 30 frames

# === UTILITY FUNCTIONS ===

def get_video_metadata(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
        return {
            "duration": float(probe["format"]["duration"]),
            "width": video_info["width"],
            "height": video_info["height"],
            "codec": video_info["codec_name"],
            "bitrate": probe["format"]["bit_rate"],
        }
    except Exception as e:
        return {"error": str(e)}

def extract_audio(video_path, audio_path):
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    command = [
        'ffmpeg', '-y', '-report', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', 
        '-ar', '16000', '-ac', '1', audio_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result.get("segments", [])

def extract_frames(video_path, output_dir, interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_data = []
    count = frame_id = 0
    os.makedirs(output_dir, exist_ok=True)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            timestamp = count / fps
            frame_path = os.path.join(output_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_data.append((frame_path, timestamp))
            frame_id += 1
        count += 1

    cap.release()
    return frame_data

def detect_objects(frames_with_times, output_dir, model):
    os.makedirs(output_dir, exist_ok=True)
    results_list = []

    for frame_path, timestamp in frames_with_times:
        img = cv2.imread(frame_path)
        if img is None:
            continue

        results = model(frame_path)
        objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                objects.append(label)

        output_path = os.path.join(output_dir, os.path.basename(frame_path))
        cv2.imwrite(output_path, img)

        results_list.append({
            "frame": output_path,
            "objects": objects,
            "time": timestamp
        })

    return results_list

def index_video(video_path, model):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(AUDIO_FOLDER, f"{base_name}_output.wav")
    frames_path = os.path.join(FRAMES_FOLDER, base_name)
    detected_path = os.path.join(DETECTED_FRAMES_FOLDER, base_name)

    os.makedirs(AUDIO_FOLDER, exist_ok=True)

    metadata = get_video_metadata(video_path)
    extract_audio(video_path, audio_path)
    segments = transcribe_audio(audio_path)
    frames_with_times = extract_frames(video_path, frames_path, interval=FRAME_INTERVAL)
    detections = detect_objects(frames_with_times, detected_path, model)

    frame_times = [{"frame": frame_path, "time": timestamp} for frame_path, timestamp in frames_with_times]

    return {
        "video": video_path,
        "metadata": metadata,
        "transcription": segments,
        "detected_objects": detections,
        "frames": frame_times
    }

def index_all_videos():
    model = YOLO("yolov8n.pt")
    results = []

    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    os.makedirs(FRAMES_FOLDER, exist_ok=True)
    os.makedirs(DETECTED_FRAMES_FOLDER, exist_ok=True)

    for file in os.listdir(VIDEOS_FOLDER):
        if file.endswith(".mp4"):
            print(f"Indexing: {file}")
            path = os.path.join(VIDEOS_FOLDER, file)
            video_data = index_video(path, model)
            results.append(video_data)

    with open(RESULTS_JSON, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nIndexing complete. Results saved in {RESULTS_JSON}")

# === UNIFIED SEARCH ===

def search_keyword_in_results(keyword):
    if not os.path.exists(RESULTS_JSON):
        print(f"Error: {RESULTS_JSON} does not exist. Please index the videos first.")
        return []

    with open(RESULTS_JSON, "r") as f:
        results = json.load(f)

    keyword = keyword.lower()
    matches = []

    if isinstance(results, list):
        for video in results:
            if isinstance(video.get("transcription"), list):
                for seg in video["transcription"]:
                    if keyword in seg["text"].lower():
                        text_time = (seg["start"] + seg["end"]) / 2
                        closest_frame = None
                        min_diff = float('inf')
                        for frame in video.get("frames", []):
                            diff = abs(frame["time"] - text_time)
                            if diff < min_diff:
                                min_diff = diff
                                closest_frame = frame["frame"]

                        matches.append({
                            "type": "text",
                            "video": video["video"],
                            "time": text_time,
                            "text": seg["text"],
                            "frame": closest_frame
                        })

            for det in video.get("detected_objects", []):
                if any(keyword == obj.lower() for obj in det["objects"]):
                    matches.append({
                        "type": "object",
                        "video": video.get("video"),
                        "frame": det["frame"],
                        "objects": det["objects"],
                        "time": det["time"]
                    })

    return matches



