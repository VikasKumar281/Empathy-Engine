import os
import uuid
import tempfile
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

_use_gtts = False
try:
    from gtts import gTTS
    from pydub import AudioSegment
    _use_gtts = True
    print("[VoiceModulator] Using gTTS + pydub for audio generation.")
except ImportError as e:
    print(f"[VoiceModulator] gTTS/pydub unavailable ({e}). Falling back to pyttsx3.")

_use_pyttsx3 = False
if not _use_gtts:
    try:
        import pyttsx3
        _use_pyttsx3 = True
        print("[VoiceModulator] Using pyttsx3 (offline TTS, rate + volume only).")
    except ImportError:
        print("[VoiceModulator] No TTS engine found. Install gtts+pydub or pyttsx3.")

def build_ssml(text: str, rate_factor: float, pitch_semitones: float, volume_db: float) -> str:
    rate_pct = f"{'+' if rate_factor >= 1 else ''}{round((rate_factor - 1) * 100)}%"
    pitch_st = f"{'+' if pitch_semitones >= 0 else ''}{round(pitch_semitones)}st"
    vol_db_str = f"{'+' if volume_db >= 0 else ''}{round(volume_db)}dB"

    return (
        f'<speak>'
        f'<prosody rate="{rate_pct}" pitch="{pitch_st}" volume="{vol_db_str}">'
        f'{text}'
        f'</prosody>'
        f'</speak>'
    )

def _modulate_pydub(raw_path: str, out_path: str, rate: float, pitch_semitones: float, volume_db: float):
    sound = AudioSegment.from_file(raw_path)
    original_fr = sound.frame_rate

    pitch_factor = 2 ** (pitch_semitones / 12.0)
    combined_factor = pitch_factor * rate

    if abs(combined_factor - 1.0) > 0.001:
        new_fr = int(original_fr * combined_factor)
        sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_fr})
        sound = sound.set_frame_rate(original_fr)

    if abs(volume_db) > 0.01:
        sound = sound + volume_db

    sound.export(out_path, format="mp3")

def _modulate_pyttsx3(text: str, out_path: str, rate_factor: float, volume_db: float):
    import pyttsx3
    engine = pyttsx3.init()

    base_rate = engine.getProperty("rate")
    engine.setProperty("rate", int(base_rate * rate_factor))

    vol = min(max(0.9 + volume_db * 0.02, 0.1), 1.0)
    engine.setProperty("volume", vol)

    engine.save_to_file(text, out_path)
    engine.runAndWait()

def synthesize(text: str, voice_config: dict, filename: str | None = None) -> dict:
    if not filename:
        filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"

    out_path = os.path.join(OUTPUT_DIR, filename)
    rate = voice_config.get("rate", 1.0)
    pitch_st = voice_config.get("pitch_semitones", 0)
    volume_db = voice_config.get("volume_db", 0)

    ssml_str = build_ssml(text, rate, pitch_st, volume_db)

    if _use_gtts:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(tmp_path)
            _modulate_pydub(tmp_path, out_path, rate, pitch_st, volume_db)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    elif _use_pyttsx3:
        _modulate_pyttsx3(text, out_path, rate, volume_db)

    else:
        raise RuntimeError(
            "No TTS engine available. Please install: pip install gtts pydub or pip install pyttsx3"
        )

    return {
        "filename": filename,
        "filepath": out_path,
        "static_url": f"audio/{filename}",
        "ssml": ssml_str,
        "parameters": {
            "rate": round(rate, 3),
            "pitch_semitones": round(pitch_st, 2),
            "volume_db": round(volume_db, 2),
        },
    }