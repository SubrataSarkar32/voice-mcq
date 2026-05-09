# Voice-Based MCQ Quiz System for Blind Users

A Python-based accessible quiz system designed for blind and visually impaired users.

The application:

* Reads MCQ questions aloud using Text-to-Speech (TTS)
* Accepts spoken answers using Speech-to-Text (STT)
* Measures speech recognition performance
* Generates a detailed timing and statistics report

---

# Features

* Voice-based interaction
* Fully hands-free quiz experience
* Reads questions and options aloud
* Accepts answers like:

  * "A"
  * "Option B"
  * "2"
  * "Three"
* Measures:

  * User speaking duration
  * STT processing time
  * Total processing time
* Generates:

  * Mean processing time
  * Variance
  * Fastest and slowest STT response
  * Per-question timing report

---

# Project Structure

```text
project/
│
├── blind_mcq_voice_quiz.py
├── questions.json
├── requirements.txt
└── README.md
```

---

# Requirements

* Python 3.9+
* Microphone
* Internet connection (Google Speech Recognition API)

---

# Installation

## 1. Clone or Download the Project

```bash
git clone <repo-url>
cd project
```

Or manually download the files.

---

## 2. Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PyAudio Installation Notes

PyAudio may require additional setup.

## Windows

Usually works with:

```bash
pip install pyaudio
```

If it fails:

### Option 1

Install wheel:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## Ubuntu / Debian Linux

```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

## macOS

```bash
brew install portaudio
pip install pyaudio
```

---

# questions.json Format

Example:

```json
[
  {
    "id": 1,
    "question": "What is the capital city of India?",
    "options": [
      "Mumbai",
      "Chennai",
      "New Delhi",
      "Kolkata"
    ],
    "answer": "New Delhi"
  }
]
```

---

# Running the Quiz

```bash
python blind_mcq_voice_quiz.py
```

---

# How It Works

1. The system reads the question aloud.
2. It reads all four options.
3. User speaks the answer.
4. Speech is converted to text.
5. Answer is validated.
6. Timing metrics are recorded.
7. Final report is generated.

---

# Accepted Voice Inputs

The following are supported:

| Spoken Input | Interpreted As |
| ------------ | -------------- |
| A            | Option A       |
| Option A     | Option A       |
| 1            | Option A       |
| One          | Option A       |
| B            | Option B       |
| 2            | Option B       |
| Three        | Option C       |
| Option D     | Option D       |

---

# Example Output

```text
Recognized Text : option c

Speaking Time   : 1.42 sec
STT Time        : 0.81 sec
Total Time      : 2.31 sec
```

---

# Final Statistics Report

Example:

```text
FINAL STT PERFORMANCE REPORT

Questions Processed : 10

Mean STT Time       : 0.742 sec
Variance STT Time   : 0.013821

Mean Speaking Time  : 1.802 sec
Variance Speaking   : 0.225192

Fastest STT Time    : 0.52 sec
Slowest STT Time    : 1.12 sec
```

---

# Accessibility Notes

* Designed for blind users
* No visual interaction required
* Fully keyboard-independent
* Audio prompts guide the user throughout the quiz

---

# Troubleshooting

## Microphone Not Detected

Check available microphones:

```python
import speech_recognition as sr

print(sr.Microphone.list_microphone_names())
```

---

## Speech Recognition Not Working

Ensure:

* Internet connection is active
* Microphone permissions are enabled
* Background noise is low

---

## TTS Voice Too Fast

Modify:

```python
engine.setProperty("rate", 150)
```

Lower values = slower speech.

---

# Future Improvements

* Offline STT support using Whisper/Vosk
* Multilingual quizzes
* Difficulty levels
* CSV/Excel export for reports
* GUI mode
* Real-time analytics dashboard
* AI-generated quizzes

---

# License

MIT License
