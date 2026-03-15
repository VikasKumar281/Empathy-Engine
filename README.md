🎙 Empathy Engine

A small project that converts text into emotion-aware speech.
Instead of reading text with a flat robotic voice, the system detects the emotion in the sentence and adjusts the speed, pitch, and loudness of the voice to match that emotion.

For example:

A happy sentence sounds energetic and upbeat

A sad sentence sounds slower and softer

A frustrated sentence sounds louder and slightly harsher

The goal of this project was to experiment with combining NLP emotion detection and voice synthesis to create more expressive audio output.

📌 What the project does

The Empathy Engine works in four main steps.

1. Text input

A user enters a sentence in the web interface.

Example:

"I can't believe this worked! I'm so happy."
2. Emotion detection

The system analyzes the text using an NLP model.

Primary model:

j-hartmann/emotion-english-distilroberta-base (HuggingFace transformer)

Fallback model:

VADER Sentiment Analyzer

Detected emotions include:

Happy

Surprised

Frustrated

Concerned

Sad

Neutral

3. Voice modulation

Once the emotion is detected, the system adjusts three parameters:

Parameter	Meaning
Rate	Speed of speech
Pitch	How high or low the voice sounds
Volume	Loudness

The intensity of the detected emotion controls how strong the adjustment is.

Example:

Mild happiness → slightly faster voice
Very strong happiness → much faster and higher pitch
4. Audio generation

The system generates an MP3 audio file using TTS and applies the voice modulation.

The audio is then returned and played in the browser.

🧠 Emotion → Voice Mapping

Each emotion is mapped to specific voice characteristics.

Emotion	Rate	Pitch	Volume	Description
Happy	Faster	Higher	Slightly louder	Energetic tone
Surprised	Much faster	High pitch	Loud	Excited tone
Frustrated	Slightly slower	Lower pitch	Loud	Strong tone
Concerned	Slower	Slightly lower	Slightly softer	Careful tone
Sad	Slow	Low pitch	Soft	Low energy tone
Neutral	Normal	Normal	Normal	Balanced voice
⚙️ Technology Used

This project combines a few different libraries.

Backend

Flask – lightweight web server

Emotion Detection

HuggingFace Transformers

Model: emotion-english-distilroberta-base

VADER Sentiment as fallback

Speech Generation

gTTS – Google Text-to-Speech

Audio Processing

pydub – audio manipulation

Offline Voice (fallback)

pyttsx3

🧩 Project Structure
empathy_engine/
│
├── app.py
│
├── emotion_detector.py
│
├── voice_modulator.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── audio/
│
├── requirements.txt
│
└── README.md

Explanation:

app.py
Flask server and API routes

emotion_detector.py
Handles emotion detection using the transformer model or VADER

voice_modulator.py
Generates speech and applies pitch/speed/volume modulation

templates/index.html
Simple web interface

static/audio/
Stores generated audio files

🖥 System Requirement

The project requires FFmpeg because pydub depends on it.

Install FFmpeg
macOS
brew install ffmpeg
Ubuntu / Debian
sudo apt update
sudo apt install ffmpeg
Windows

Download from

https://ffmpeg.org/download.html

Extract the zip

Add the bin folder to your system PATH

🚀 How to Run the Project

Follow these steps.

Step 1 — Clone the repository
git clone https://github.com/yourusername/empathy-engine.git

or download the ZIP.

Then move into the folder:

cd empathy_engine
Step 2 — Create a virtual environment
python -m venv venv

Activate it.

Windows:

venv\Scripts\activate

Mac / Linux:

source venv/bin/activate
Step 3 — Install dependencies
pip install -r requirements.txt
Step 4 — Run the server
python app.py
Step 5 — Open the web app

Open your browser and go to:

http://127.0.0.1:5000
🔌 API Endpoint
POST /synthesize

This endpoint generates emotion-aware speech.

Request
{
"text": "I just got promoted!",
"override_emotion": null
}

Fields:

Field	Description
text	Input sentence
override_emotion	Optional manual emotion
Response Example
{
"success": true,
"emotion": {
"label": "happy",
"confidence": 0.98
},
"voice_parameters": {
"rate": 1.15,
"pitch_semitones": 3,
"volume_db": 3
},
"audio_url": "/static/audio/speech_12345.mp3"
}
🎯 Why I Built This

Most TTS systems sound flat and emotionless.

This project explores how to:

detect emotions in text

translate that emotion into voice parameters

produce expressive speech

It was mainly built as a learning project combining NLP and speech processing.

📈 Possible Improvements

Some ideas for future work:

Real-time microphone emotion detection

Streaming audio output

Support for multiple languages

Emotion-aware chatbot responses

More advanced pitch/tempo control

📜 License

This project is open-source and free to use for learning or experimentation.