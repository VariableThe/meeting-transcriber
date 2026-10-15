import os
import tempfile
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

MODELS = {}
AVAILABLE_MODELS = ["tiny", "base", "small", "medium"]

def get_model(name="base"):
    if name in MODELS:
        return MODELS[name]
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    print(f"Loading whisper model: {name} ...")
    model = WhisperModel(name, device="auto", compute_type="auto")
    MODELS[name] = model
    print(f"Model {name} loaded")
    return model

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No file selected"}), 400

    model_name = request.form.get("model", "base")
    if model_name not in AVAILABLE_MODELS:
        model_name = "base"
    language = request.form.get("language", "auto")
    if language == "auto":
        language = None

    model = get_model(model_name)
    if model is None:
        return jsonify({"error": "faster-whisper not installed. Run: pip install faster-whisper"}), 500

    suffix = os.path.splitext(f.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name

    try:
        start = time.time()
        segments, info = model.transcribe(tmp_path, language=language, beam_size=5, vad_filter=True)
        text_parts = []
        segs = []
        for s in segments:
            text_parts.append(s.text)
            segs.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        full_text = " ".join(text_parts).strip()
        elapsed = round(time.time() - start, 2)
        return jsonify({
            "text": full_text,
            "segments": segs,
            "language": info.language,
            "duration": round(info.duration, 2),
            "time_taken": elapsed,
            "model": model_name
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("\n Meeting Transcriber")
    print(" Open http://localhost:5001 in your browser\n")
    try:
        from faster_whisper import WhisperModel
        print(" faster-whisper installed ✓")
    except ImportError:
        print(" ! faster-whisper not installed - run: pip install -r requirements.txt")
    app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)
