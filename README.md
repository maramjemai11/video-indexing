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

# 🎥 Smart Video Indexing & Search — Quick Start

How to run (brief)

PowerShell (from the `tp2` folder):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run interface.py
```

Lightweight video indexing and search using Whisper for speech transcription and YOLOv8 for object detection. This README is a short quick-start; the full documentation is saved as `README_FULL.md`.

Quick steps (PowerShell, from the `tp2` folder):

1) Create and activate a virtual env

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3) Ensure `ffmpeg` is installed and on PATH (e.g., `choco install ffmpeg`) 

4) Run the Streamlit UI

```powershell
streamlit run interface.py
```

Alternative: index all videos from the CLI

```powershell
python -c "from tp_index1 import index_all_videos; index_all_videos()"
```

Files of interest:
- `interface.py` — Streamlit UI
- `tp_index1.py` — core indexing & search logic
- `results.json` — generated index

Notes:
- Do not commit large files (models `.pt`, videos, frames). Use `.gitignore` and consider Git LFS. See `README_FULL.md` for full details.

If you want the long README back in `README.md` or any other edits (shorter/longer), tell me how brief you want it and I will update it.
  - Links the match to the source video
