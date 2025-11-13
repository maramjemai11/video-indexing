# 🎥 Smart Video Indexing & Search

A comprehensive video indexing and search system that extracts, analyzes, and indexes video content using AI-powered object detection and speech recognition.

## 📋 Overview

This project processes video files to create a searchable index combining:
- **Speech Recognition**: Transcribes audio using OpenAI's Whisper
- **Object Detection**: Identifies objects in frames using YOLOv8
- **Frame Extraction**: Systematically samples frames from videos
- **Unified Search**: Search videos by keywords that match either transcribed text or detected objects

## 🏗️ Project Structure

```
tp2/
├── interface.py              # Streamlit web interface for searching and indexing
├── tp_index1.py              # Core indexing and search logic
├── results.json              # Indexed results (auto-generated after processing)
├── yolov8n.pt               # YOLOv8 Nano model weights (object detection)
├── yolov8l.pt               # YOLOv8 Large model weights (alternative)
├── videos/                   # Input video files (.mp4)
├── frames/                   # Extracted frames from videos
│   ├── vid2.0/
│   └── vid3/
├── detected_frames/          # Frames with detected objects highlighted
│   ├── vid2.0/
│   └── vid3/
├── audios/                   # Extracted audio files (.wav)
└── __pycache__/             # Python cache files
```

## 🔧 How It Works

### 1. **Video Indexing** (`tp_index1.py`)

The indexing process (`index_video()`) performs the following steps for each video:

#### Step 1: Extract Metadata
- Gets video duration, resolution, codec, and bitrate using FFmpeg

#### Step 2: Extract Audio
- Converts video audio to 16kHz mono WAV format using FFmpeg
- Saved to `audios/` folder

#### Step 3: Transcribe Audio
- Uses Whisper (OpenAI's speech recognition model) to transcribe audio
- Returns timestamped text segments showing what was said and when

#### Step 4: Extract Frames
- Extracts frames at intervals (default: every 30 frames)
- Frame interval is configurable via `FRAME_INTERVAL` constant
- Saves frames to `frames/` folder with timestamp information

#### Step 5: Detect Objects
- Uses YOLOv8 model to detect objects in each extracted frame
- Draws bounding boxes around detected objects
- Saves annotated frames to `detected_frames/` folder
- Records detected object types (person, chair, tie, etc.) with timestamps

#### Step 6: Save Results
- Combines all data into `results.json` with structure:
  ```json
  {
    "video": "path/to/video.mp4",
    "metadata": { duration, width, height, codec, bitrate },
    "transcription": [ { start, end, text, ... } ],
    "detected_objects": [ { frame, objects, time } ],
    "frames": [ { frame, time } ]
  }
  ```

### 2. **Search Functionality** (`search_keyword_in_results()`)

Performs unified search across transcription and detected objects:

- **Text Search**: Finds keywords in transcribed speech
  - Returns the exact text segment containing the keyword
  - Provides the closest frame to the timestamp
  - Links the match to the source video

- **Object Search**: Finds detected objects by type
  - Matches detected object labels (e.g., "person", "dog")
  - Returns the frame where the object was detected
  - Provides the timestamp of detection

### 3. **Web Interface** (`interface.py`)

A Streamlit-based user-friendly interface featuring:

- **Index All Videos**: One-click button to process all videos in the `videos/` folder
- **Search Bar**: Enter keywords to search across all indexed content
- **Results Display**: 
  - Shows matches organized by video
  - For text matches: displays the spoken text and closest frame
  - For object matches: displays detected objects and annotated frame
- **Raw JSON View**: Optional view of the complete `results.json` file

## ⚙️ Configuration

Key configuration parameters in `tp_index1.py`:

```python
VIDEOS_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\videos"
FRAMES_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\frames"
DETECTED_FRAMES_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\detected_frames"
AUDIO_FOLDER = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\audios"
RESULTS_JSON = "C:\\Users\\maram\\Desktop\\glsi2\\s2\\indexation\\tp2\\results.json"
FRAME_INTERVAL = 30  # Extract frames every 30 frames
```

## 📦 Dependencies

- **OpenCV** (`cv2`): Video processing and frame extraction
- **FFmpeg**: Audio extraction and video metadata
- **OpenAI Whisper** (`whisper`): Speech transcription
- **Ultralytics YOLO** (`ultralytics`): Object detection
- **Streamlit** (`streamlit`): Web interface
- **FFmpeg-python** (`ffmpeg`): Python FFmpeg wrapper

Install dependencies:
```bash
pip install opencv-python ffmpeg-python openai-whisper ultralytics streamlit
```

Also ensure FFmpeg is installed on your system:
- **Windows**: Download from https://ffmpeg.org/download.html or use `choco install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

## 🚀 Usage

### 1. Prepare Videos
Place video files (`.mp4`) in the `videos/` folder

### 2. Run the Web Interface
```bash
streamlit run interface.py
```

### 3. Index Videos
- Open the web interface in your browser
- Click "📁 Index All Videos"
- Wait for the process to complete (depends on video duration and size)
- Results will be saved to `results.json`

### 4. Search
- Enter a keyword in the search bar (e.g., "person", "hello")
- Click "🔎 Search"
- View results organized by match type (text or object)

### 5. (Optional) View Raw Data
- Check the "📂 Show raw JSON results" checkbox to see the complete indexed data

### Run locally (Windows PowerShell)

Follow these steps to set up and run the project on Windows using PowerShell. These commands assume you're in the project directory (`tp2`).

1. Create and activate a virtual environment

```powershell
python -m venv .venv
# Activate the venv in PowerShell
.\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install dependencies

```powershell
pip install --upgrade pip
pip install opencv-python ffmpeg-python openai-whisper ultralytics streamlit
```

3. Ensure FFmpeg is installed and available in PATH
- If you installed via Chocolatey: `choco install ffmpeg`
- Or add the FFmpeg `bin` folder to your system PATH so `ffmpeg` is callable from PowerShell.

4. Start the Streamlit web UI

```powershell
streamlit run interface.py
```

Open the URL printed by Streamlit (usually http://localhost:8501) in your browser.

5. (Alternative) Run indexing from the command line without the Streamlit UI

If you prefer to index all videos directly (no UI), run this one-liner from PowerShell in the project folder:

```powershell
python -c "from tp_index1 import index_all_videos; index_all_videos()"
```

This will process all `.mp4` files in the `videos/` folder and write `results.json`.

## 📊 Example Results

When indexing a 10-second video of two people talking:

**Transcription Result:**
```
"Hi, how are you doing?" (0-2 seconds)
"I'm fine." (2-4 seconds)
"How about yourself?" (4-6 seconds)
```

**Object Detection Result:**
```
Frame at 0.0 sec: person, person, tie
Frame at 1.25 sec: person, person, tie
Frame at 2.5 sec: person, person, tie, tie
...
```

**Search for "person":**
- Returns 9 results from detected objects across multiple frames
- Each result includes the annotated frame with bounding boxes

**Search for "fine":**
- Returns 1 text match: "I'm fine."
- Includes the frame closest to the 2-3 second timestamp

## 🎯 Use Cases

- **Video Content Management**: Quickly find videos containing specific content
- **Accessibility**: Search video content without watching the entire video
- **Video Archival**: Build searchable archives of recorded content
- **Meeting Analysis**: Index recorded meetings and search by topics or attendees
- **Media Monitoring**: Track mentions of specific topics or objects in video content

## 🔍 How Search Matching Works

```python
# Text matching (case-insensitive)
if keyword.lower() in segment["text"].lower()

# Object matching (exact match, case-insensitive)
if any(keyword.lower() == obj.lower() for obj in detected_objects)
```

## 📝 Notes

- The first time you run the project, it will download the Whisper model (~1.4GB)
- YOLOv8 models (yolov8n.pt or yolov8l.pt) must be present in the project folder
- Processing time depends on:
  - Video length
  - Video resolution
  - Number of frames extracted
  - CPU/GPU availability
- All paths in `tp_index1.py` are hardcoded to your local system. Update if moving the project.

## 🛠️ Troubleshooting

**FFmpeg not found**: Ensure FFmpeg is installed and in your system PATH

**YOLO model not found**: Download the appropriate model:
```bash
# YOLOv8 Nano (lighter, faster)
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# YOLOv8 Large (more accurate)
python -c "from ultralytics import YOLO; YOLO('yolov8l.pt')"
```

**Out of Memory**: Reduce `FRAME_INTERVAL` or use a smaller YOLO model

**No results found**: Verify videos are in `.mp4` format and in the `videos/` folder

## 📄 License

This project is for educational purposes.

## 📤 Publish to GitHub

Follow these instructions to push the project to a GitHub repository from Windows PowerShell.

1) (Optional) Install Git LFS to store large files (recommended for model weights and videos):

```powershell
# Install with Chocolatey (if you have choco)
choco install git-lfs
# Or download and run the installer from https://git-lfs.github.com/
git lfs install
```

2) Initialize a local git repository, add files and create the first commit:

```powershell
# from the project folder (tp2)
git init
git add .
git commit -m "chore: initial commit - add video indexer project"
```

3) Create a new repository on GitHub (manually via the website) and copy the repository URL (HTTPS or SSH). Then add it as a remote and push:

```powershell
# Example for HTTPS remote
git remote add origin https://github.com/<your-username>/<your-repo>.git
# Push initial commit (if using main branch)
git branch -M main
git push -u origin main
```

Notes:
- If you tracked large files (models `.pt` or videos), use `git lfs track "*.pt"` and `git lfs track "*.mp4"` before `git add .` so those files are stored via LFS. Example:

```powershell
git lfs track "*.pt"
git lfs track "*.mp4"
# re-add files after tracking
git add .gitattributes
git add .
git commit -m "chore: track large files with git-lfs"
git push
```

- If you want, I can initialize the repository and make the initial commit for you here. To push to GitHub from this environment I'd need the remote repository URL and your consent to run the git commands. I will not request any credentials — Git will prompt you locally for username/password or personal access token (PAT) when required.

---

If you'd like, I can now:
- create a `requirements.txt` and `.gitignore` (done)
- initialize git and make the initial commit here (I can run the commands locally in the terminal) — tell me to proceed and provide the GitHub remote URL when ready
- or show step-by-step copy-paste commands tailored to your preferred workflow (SSH vs HTTPS, use LFS or not)

Which would you like me to do next? 
