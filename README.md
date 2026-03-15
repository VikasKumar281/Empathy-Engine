🎙 Empathy Engine

Empathy Engine is a small experiment in combining Natural Language Processing (NLP) with Text-to-Speech (TTS) to produce more expressive audio.

Instead of reading text in a flat robotic tone, the system first detects the emotion in the sentence and then adjusts the speed, pitch, and loudness of the voice accordingly.

For example:

Input Emotion	Voice Behavior
Happy	Faster and energetic speech
Sad	Slower and softer voice
Frustrated	Louder and slightly harsher tone

The goal of this project is to explore how emotion detection can improve speech synthesis and make generated audio feel more natural.

📌 What the Project Does

The Empathy Engine works in four main stages.

1️⃣ Text Input

A user enters a sentence in the web interface.

Example:

I can't believe this worked! I'm so happy.

The input text is then sent to the backend for emotion analysis.

2️⃣ Emotion Detection

The system analyzes the sentence using an NLP model.

Primary Model
Model	Library
j-hartmann/emotion-english-distilroberta-base	HuggingFace Transformers

This model detects emotional categories from text.

Fallback Model
Model	Library
VADER Sentiment Analyzer	vaderSentiment

If the transformer cannot load, the system automatically falls back to VADER.

Supported Emotions
Emotion
Happy
Surprised
Frustrated
Concerned
Sad
Neutral
3️⃣ Voice Modulation

Once the emotion is detected, the system adjusts three voice parameters.

Parameter	Description
Rate	Speed of speech
Pitch	How high or low the voice sounds
Volume	Loudness of the voice

The intensity of the emotion determines how strong the modulation will be.

Example:

Emotion Intensity	Result
Mild happiness	Slightly faster voice
Strong happiness	Faster speech + higher pitch
4️⃣ Audio Generation

The system generates speech using a Text-to-Speech engine and applies voice modulation.

The final output is:

An MP3 audio file

Played directly in the browser

🧠 Emotion → Voice Mapping

Each detected emotion corresponds to specific voice characteristics.

Emotion	Rate	Pitch	Volume	Description
Happy	Faster	Higher	Slightly louder	Energetic and upbeat
Surprised	Much faster	High pitch	Loud	Animated tone
Frustrated	Slightly slower	Lower pitch	Loud	Strong and assertive
Concerned	Slower	Slightly lower	Softer	Careful tone
Sad	Slow	Low pitch	Soft	Low energy tone
Neutral	Normal	Normal	Normal	Balanced speech
⚙️ Technology Stack

The project combines multiple tools from NLP and audio processing.

Backend
Tool	Purpose
Flask	Lightweight web server
Emotion Detection
Tool	Purpose
HuggingFace Transformers	Emotion classification
DistilRoBERTa emotion model	NLP emotion detection
VADER	Fallback sentiment analysis
Speech Generation
Tool	Purpose
gTTS	Google Text-to-Speech
pydub	Audio manipulation
pyttsx3	Offline TTS fallback
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
File Explanation
File	Purpose
app.py	Flask server and API routes
emotion_detector.py	Emotion detection logic
voice_modulator.py	Speech synthesis and modulation
templates/index.html	Web interface
static/audio	Stores generated audio files
🖥 System Requirements

The project requires FFmpeg because pydub depends on it.

Install FFmpeg
macOS
brew install ffmpeg
Ubuntu / Debian
sudo apt update
sudo apt install ffmpeg -y
Windows

Download FFmpeg from:

https://ffmpeg.org/download.html

Extract the ZIP file

Add the bin folder to your system PATH

🚀 How to Run the Project

Follow these steps.

Step 1 — Clone the Repository
git clone https://github.com/VikasKumar281/Empathy-Engine.git

Move into the project directory.

cd Empathy-Engine
Step 2 — Create a Virtual Environment
python -m venv venv

Activate the environment.

Windows
venv\Scripts\activate
Mac / Linux
source venv/bin/activate
Step 3 — Install Dependencies
pip install -r requirements.txt
Step 4 — Run the Server
python app.py
Step 5 — Open the Web App

Open your browser and go to:

http://127.0.0.1:5000
🔌 API Endpoint
POST /synthesize

Generates emotion-aware speech.

Request
{
"text": "I just got promoted!",
"override_emotion": null
}
Request Fields
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
🎯 Motivation

Most text-to-speech systems produce speech that sounds flat and emotionless.

This project explores how we can:

detect emotions in text

translate emotions into voice parameters

generate more expressive speech output

The project was built mainly as a learning experiment combining NLP and speech processing.

📈 Future Improvements

Some possible future enhancements:

Feature	Idea
Real-time emotion detection	Microphone input
Streaming speech	Generate audio continuously
Multilingual support	Detect emotion in multiple languages
Emotion chatbot	Emotion-aware responses
Advanced DSP	Better pitch/tempo separation
📜 License

This project is open-source and free to use for learning and experimentation.
