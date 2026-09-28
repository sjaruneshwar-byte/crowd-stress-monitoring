import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from database import init_db, save_analysis, get_recent_analyses
from detector import analyze_video

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
MAX_UPLOAD_MB = 100

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
app.config["DATABASE"] = str(BASE_DIR / "crowd_monitor.db")
init_db(app.config["DATABASE"])


def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/history")
def history():
    return jsonify(get_recent_analyses(app.config["DATABASE"]))


@app.post("/api/analyze")
def analyze():
    uploaded = request.files.get("video")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please choose a video file."}), 400
    if not allowed_file(uploaded.filename):
        return jsonify({"error": "Unsupported format. Upload MP4, AVI, MOV or MKV."}), 400

    original_name = secure_filename(uploaded.filename) or "uploaded_video"
    suffix = Path(original_name).suffix.lower()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp_path = temp.name
            uploaded.save(temp_path)

        result = analyze_video(temp_path)
        record_id = save_analysis(
            app.config["DATABASE"],
            filename=original_name,
            result=result
        )
        result["id"] = record_id
        result["filename"] = original_name
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422
    except Exception:
        app.logger.exception("Video analysis failed")
        return jsonify({"error": "Analysis failed. Check that the video is valid and readable."}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": f"File too large. Maximum upload size is {MAX_UPLOAD_MB} MB."}), 413


if __name__ == "__main__":
    # Local development only. Use a production WSGI server for deployment.
    app.run(debug=True)
