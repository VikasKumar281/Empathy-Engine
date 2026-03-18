from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

VOICE_CONFIGS = {
    "happy": {"rate": 1.15, "pitch_semitones": 3, "volume_db": 3},
    "surprised": {"rate": 1.25, "pitch_semitones": 5, "volume_db": 4},
    "frustrated": {"rate": 0.90, "pitch_semitones": -2, "volume_db": 5},
    "concerned": {"rate": 0.85, "pitch_semitones": -1, "volume_db": -1},
    "sad": {"rate": 0.80, "pitch_semitones": -4, "volume_db": -3},
    "neutral": {"rate": 1.00, "pitch_semitones": 0, "volume_db": 0},
}

def scale(config, intensity):
    return {
        "rate": 1.0 + (config["rate"] - 1.0) * intensity,
        "pitch_semitones": config["pitch_semitones"] * intensity,
        "volume_db": config["volume_db"] * intensity,
    }

def detect_emotion(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.6:
        emotion, intensity = "happy", compound
    elif compound >= 0.2:
        emotion, intensity = "happy", compound * 0.6
    elif compound <= -0.6:
        emotion, intensity = "frustrated", abs(compound)
    elif compound <= -0.2:
        emotion, intensity = "sad", abs(compound) * 0.6
    else:
        emotion, intensity = "neutral", 0.4

    config = scale(VOICE_CONFIGS[emotion], intensity)

    return {
        "emotion": emotion,
        "confidence": round(abs(compound), 4),
        "intensity": round(intensity, 4),
        "voice_config": config
    }