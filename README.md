# Meeting Transcriber — Simple Local Audio Transcription

Very simple UI to transcribe your 2-3 minute meeting summaries. 100% local, free, offline. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper).

## Quick Start

```bash
cd MeetingTranscriber
chmod +x run.sh
./run.sh
# open http://localhost:5001
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

First run downloads the model (~40MB tiny / ~150MB base / ~500MB small). Afterwards fully offline.

## Usage

1. Drag & drop or click to select `mp3 / wav / m4a / ogg / webm / mp4`
2. Choose model: `tiny` fastest, `base` balanced (recommended for 2-3 min notes), `small`/`medium` more accurate but slower
3. Click Transcribe → copy or download `.txt`

## Notes

- Max 100MB file
- Requires `ffmpeg` for some formats: `brew install ffmpeg`
- Models auto-download to `~/.cache/huggingface`
- Language auto-detected, or force English etc.

## API

`POST /transcribe` multipart: `file`, `model=tiny|base|small|medium`, `language=auto|en|...`
