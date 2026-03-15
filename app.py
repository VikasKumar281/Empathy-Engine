from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import traceback
from emotion_detector import detect_emotion, VOICE_CONFIGS
from voice_modulator import synthesize

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

@app.route("/")
def index():
    emotions = list(VOICE_CONFIGS.keys())
    return render_template("index.html", emotions=emotions)

@app.route("/synthesize", methods=["POST"])
def synthesize_route():
    data = request.get_json(force=True, silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400
    if len(text) > 1000:
        return jsonify({"error": "Text too long (max 1000 characters)."}), 400

    try:
        result = detect_emotion(text)

        override = (data.get("override_emotion") or "").strip().lower()
        if override and override in VOICE_CONFIGS:
            result["emotion"] = override
            result["voice_config"] = VOICE_CONFIGS[override]

        emotion = result["emotion"]
        voice_config = result["voice_config"]

        audio_result = synthesize(text, voice_config)

        cfg = VOICE_CONFIGS.get(emotion, VOICE_CONFIGS["neutral"])
        return jsonify({
            "success": True,
            "text": text,
            "emotion": {
                "label": emotion,
                "raw": result["raw_emotion"],
                "confidence": result["confidence"],
                "intensity": result["intensity"],
                "description": cfg["description"],
                "color": cfg["color"],
                "emoji": cfg["emoji"],
                "all_scores": result.get("all_scores", {})
            },
            "voice_parameters": audio_result["parameters"],
            "ssml": audio_result["ssml"],
            "audio_url": f"/static/audio/{audio_result['filename']}"
        })

    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": str(exc)}), 500

@app.route("/static/audio/<path:filename>")
def serve_audio(filename):
    audio_dir = os.path.join(app.root_path, "static", "audio")
    return send_from_directory(audio_dir, filename)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("=" * 60)
    print("  🎙  Empathy Engine  –  http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)