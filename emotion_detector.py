import re

_transformer_loaded = False
_classifier = None

def _try_load_transformer():
    global _transformer_loaded, _classifier
    try:
        from transformers import pipeline
        _classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,
            truncation=True,
        )
        _transformer_loaded = True
        print("[EmotionDetector] Using transformer model (j-hartmann/emotion-english-distilroberta-base)")
    except Exception as e:
        print(f"[EmotionDetector] Transformer unavailable ({e}), falling back to VADER.")

_try_load_transformer()

_vader_analyzer = None
if not _transformer_loaded:
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        _vader_analyzer = SentimentIntensityAnalyzer()
        print("[EmotionDetector] Using VADER sentiment analyser.")
    except ImportError:
        print("[EmotionDetector] VADER not available either. Install vaderSentiment.")

TRANSFORMER_LABEL_MAP = {
    "joy": "happy",
    "surprise": "surprised",
    "anger": "frustrated",
    "disgust": "frustrated",
    "fear": "concerned",
    "sadness": "sad",
    "neutral": "neutral",
}

VOICE_CONFIGS = {
    "happy": {
        "rate": 1.15,
        "pitch_semitones": 3,
        "volume_db": 3,
        "description": "Enthusiastic and upbeat",
        "color": "#f59e0b",
        "emoji": "😊",
    },
    "surprised": {
        "rate": 1.25,
        "pitch_semitones": 5,
        "volume_db": 4,
        "description": "Animated and energetic",
        "color": "#8b5cf6",
        "emoji": "😲",
    },
    "frustrated": {
        "rate": 0.90,
        "pitch_semitones": -2,
        "volume_db": 5,
        "description": "Firm and assertive",
        "color": "#ef4444",
        "emoji": "😤",
    },
    "concerned": {
        "rate": 0.85,
        "pitch_semitones": -1,
        "volume_db": -1,
        "description": "Careful and measured",
        "color": "#f97316",
        "emoji": "😟",
    },
    "sad": {
        "rate": 0.80,
        "pitch_semitones": -4,
        "volume_db": -3,
        "description": "Somber and subdued",
        "color": "#3b82f6",
        "emoji": "😢",
    },
    "neutral": {
        "rate": 1.00,
        "pitch_semitones": 0,
        "volume_db": 0,
        "description": "Balanced and clear",
        "color": "#6b7280",
        "emoji": "😐",
    },
}

def _scale_by_intensity(config: dict, intensity: float) -> dict:
    if intensity < 0.01:
        intensity = 0.01
    scaled = dict(config)
    scaled["rate"] = 1.0 + (config["rate"] - 1.0) * intensity
    scaled["pitch_semitones"] = config["pitch_semitones"] * intensity
    scaled["volume_db"] = config["volume_db"] * intensity
    return scaled

def detect_emotion(text: str) -> dict:
    text = text.strip()
    if not text:
        return _neutral_result()

    if _transformer_loaded and _classifier is not None:
        return _detect_transformer(text)
    elif _vader_analyzer is not None:
        return _detect_vader(text)
    else:
        return _neutral_result()

def _detect_transformer(text: str) -> dict:
    results = _classifier(text)[0]
    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
    top = results_sorted[0]

    raw_label = top["label"].lower()
    confidence = top["score"]
    emotion = TRANSFORMER_LABEL_MAP.get(raw_label, "neutral")

    intensity = min(confidence * 1.2, 1.0)

    base_config = VOICE_CONFIGS.get(emotion, VOICE_CONFIGS["neutral"])
    voice_config = _scale_by_intensity(base_config, intensity)

    all_scores = {
        TRANSFORMER_LABEL_MAP.get(r["label"].lower(), r["label"].lower()): round(r["score"], 4)
        for r in results_sorted
    }

    return {
        "raw_emotion": raw_label,
        "emotion": emotion,
        "confidence": round(confidence, 4),
        "intensity": round(intensity, 4),
        "voice_config": voice_config,
        "all_scores": all_scores,
    }

def _detect_vader(text: str) -> dict:
    scores = _vader_analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.6:
        emotion, intensity = "happy", min(compound, 1.0)
    elif compound >= 0.2:
        emotion, intensity = "happy", compound * 0.6
    elif compound <= -0.6:
        emotion, intensity = "frustrated", min(abs(compound), 1.0)
    elif compound <= -0.2:
        emotion, intensity = "sad", abs(compound) * 0.6
    else:
        emotion, intensity = "neutral", 0.4

    base_config = VOICE_CONFIGS.get(emotion, VOICE_CONFIGS["neutral"])
    voice_config = _scale_by_intensity(base_config, intensity)

    return {
        "raw_emotion": emotion,
        "emotion": emotion,
        "confidence": round(abs(compound), 4),
        "intensity": round(intensity, 4),
        "voice_config": voice_config,
        "all_scores": {
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"],
        },
    }

def _neutral_result() -> dict:
    config = VOICE_CONFIGS["neutral"]
    return {
        "raw_emotion": "neutral",
        "emotion": "neutral",
        "confidence": 1.0,
        "intensity": 0.5,
        "voice_config": config,
        "all_scores": {},
    }