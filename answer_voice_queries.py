# ai_quiz_solver.py
#
# AI Voice Quiz Solver
#
# Features:
# - Listens to spoken quiz questions
# - Uses LLM to determine correct answer
# - Speaks the answer aloud
#
# Supports:
# - OpenAI API
# - Local Ollama models
#
# Install:
# pip install speechrecognition pyttsx3 pyaudio requests openai
#
# Run:
# python ai_quiz_solver.py
#
# Example spoken question:
# "What is the capital city of India?
# Option A Mumbai
# Option B Chennai
# Option C New Delhi
# Option D Kolkata"

import speech_recognition as sr
import pyttsx3
import requests
import re
import time

# ==========================================
# CONFIGURATION
# ==========================================

USE_OLLAMA = True

# OLLAMA CONFIG
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:4b"

# OPENAI CONFIG
OPENAI_API_BASE = "http://localhost:11434/v1/"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OPENAI_MODEL = "qwen3:4b"

# ==========================================
# TTS SETUP
# ==========================================

engine = pyttsx3.init()

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)


def speak(text):
    print(f"AI: {text}")

    engine.say(text)
    engine.runAndWait()


# ==========================================
# SPEECH RECOGNITION
# ==========================================

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def listen_question():

    with microphone as source:

        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening for question...")

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("\nQUESTION HEARD:")
        print(text)

        return text

    except sr.UnknownValueError:

        print("Could not understand audio.")
        return None

    except sr.RequestError:

        print("Speech recognition service unavailable.")
        return None


# ==========================================
# LLM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are a quiz solving AI.

You will receive:
- A multiple choice question
- Four options

Your task:
- Determine the correct answer
- Reply ONLY with:
Option A
Option B
Option C
Option D

Do not explain.
"""


# ==========================================
# OLLAMA CALL
# ==========================================

def ask_ollama(question_text):

    prompt = f"""
{SYSTEM_PROMPT}

Question:
{question_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]


# ==========================================
# OPENAI CALL
# ==========================================

def ask_openai(question_text):

    from openai import OpenAI

    client = OpenAI(base_url=, api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question_text
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ==========================================
# ANSWER EXTRACTION
# ==========================================

def extract_option(llm_response):

    text = llm_response.strip().upper()

    print("\nLLM RESPONSE:")
    print(text)

    match = re.search(r'OPTION\s*([ABCD])', text)

    if match:
        return match.group(1)

    # fallback
    for ch in ["A", "B", "C", "D"]:
        if ch in text:
            return ch

    return None


# ==========================================
# MAIN LOOP
# ==========================================

speak("AI Quiz Solver started.")

while True:

    print("\n--------------------------------")
    print("Press ENTER and ask question...")
    input()

    question_text = listen_question()

    if not question_text:
        continue

    try:

        if USE_OLLAMA:
            llm_response = ask_ollama(question_text)
        else:
            llm_response = ask_openai(question_text)

        answer = extract_option(llm_response)

        if answer:

            final_answer = f"Option {answer}"

            print(f"\nFINAL ANSWER: {final_answer}")

            speak(final_answer)

        else:

            speak("I could not determine the answer.")

    except Exception as e:

        print("ERROR:", e)

        speak("An error occurred.")

    time.sleep(1)
