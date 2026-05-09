# blind_mcq_voice_quiz.py
#
# Voice-based MCQ Quiz System for Blind Users
#
# FEATURES
# ----------------------------------------
# - Reads questions from JSON
# - Uses TTS for questions
# - Uses STT for spoken answers
# - Measures:
#     * User speaking time
#     * STT processing time
#     * Total answer processing time
# - Generates final statistics report
# - Computes:
#     * Mean
#     * Variance
#     * Min / Max
#     * Per-question timings
#
# INSTALL
# ----------------------------------------
# pip install pyttsx3 SpeechRecognition pyaudio
#
# RUN
# ----------------------------------------
# python blind_mcq_voice_quiz.py

import json
import pyttsx3
import speech_recognition as sr
import time
import statistics

# ==========================================
# LOAD QUESTIONS
# ==========================================

JSON_FILE = "questions.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# ==========================================
# TTS SETUP
# ==========================================

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)


def speak(text):

    print(f"TTS: {text}")

    engine.say(text)
    engine.runAndWait()


# ==========================================
# STT SETUP
# ==========================================

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# ==========================================
# PERFORMANCE STORAGE
# ==========================================

performance_data = []

# ==========================================
# LISTEN FUNCTION
# ==========================================


def listen(question_id):

    with microphone as source:

        recognizer.adjust_for_ambient_noise(source, duration=1)

        speak("Please say your answer.")

        print("Listening...")

        # --------------------------------------
        # TOTAL TIMER START
        # --------------------------------------

        total_start = time.perf_counter()

        # --------------------------------------
        # USER SPEAKING TIMER
        # --------------------------------------

        speech_start = time.perf_counter()

        audio = recognizer.listen(source)

        speech_end = time.perf_counter()

        # --------------------------------------
        # STT PROCESSING TIMER
        # --------------------------------------

        stt_start = time.perf_counter()

    try:

        text = recognizer.recognize_google(audio)

        stt_end = time.perf_counter()

        total_end = time.perf_counter()

        # ======================================
        # TIME CALCULATIONS
        # ======================================

        speaking_time = speech_end - speech_start
        stt_time = stt_end - stt_start
        total_time = total_end - total_start

        # ======================================
        # STORE PERFORMANCE DATA
        # ======================================

        performance_data.append({
            "question_id": question_id,
            "recognized_text": text,
            "speaking_time": speaking_time,
            "stt_time": stt_time,
            "total_time": total_time
        })

        # ======================================
        # DISPLAY TIMING
        # ======================================

        print("\n===================================")
        print(f"Recognized Text : {text}")
        print("-----------------------------------")
        print(f"Speaking Time   : {speaking_time:.2f} sec")
        print(f"STT Time        : {stt_time:.2f} sec")
        print(f"Total Time      : {total_time:.2f} sec")
        print("===================================\n")

        return {
            "text": text.lower(),
            "speaking_time": speaking_time,
            "stt_time": stt_time,
            "total_time": total_time
        }

    except sr.UnknownValueError:

        speak("Sorry, I could not understand.")

        return None

    except sr.RequestError:

        speak("Speech recognition service unavailable.")

        return None


# ==========================================
# OPTION MAPPING
# ==========================================

OPTION_MAP = {
    "a": 0,
    "option a": 0,
    "1": 0,
    "one": 0,

    "b": 1,
    "option b": 1,
    "2": 1,
    "two": 1,

    "c": 2,
    "option c": 2,
    "3": 2,
    "three": 2,

    "d": 3,
    "option d": 3,
    "4": 3,
    "four": 3
}


def extract_answer_index(spoken_text):

    if not spoken_text:
        return None

    spoken_text = spoken_text.strip().lower()

    if spoken_text in OPTION_MAP:
        return OPTION_MAP[spoken_text]

    return None


# ==========================================
# QUIZ LOGIC
# ==========================================

score = 0

speak("Welcome to the General Knowledge Quiz.")

time.sleep(1)

for q in questions:

    speak(f"Question {q['id']}")

    speak(q["question"])

    option_letters = ["A", "B", "C", "D"]

    for idx, option in enumerate(q["options"]):

        speak(f"Option {option_letters[idx]}. {option}")

    user_answer_index = None

    for attempt in range(3):

        result = listen(q["id"])

        if not result:
            continue

        spoken_text = result["text"]

        answer_index = extract_answer_index(spoken_text)

        if answer_index is not None:

            user_answer_index = answer_index

            speak(
                f"Answer processed in "
                f"{result['total_time']:.1f} seconds."
            )

            break

        speak("Please answer using option A, B, C or D.")

    if user_answer_index is None:

        speak("Skipping this question.")

        continue

    selected_answer = q["options"][user_answer_index]

    if selected_answer.lower() == q["answer"].lower():

        speak("Correct answer.")

        score += 1

    else:

        speak(
            f"Wrong answer. "
            f"The correct answer is {q['answer']}."
        )

    time.sleep(1)

# ==========================================
# FINAL REPORT
# ==========================================

print("\n\n========================================")
print("FINAL STT PERFORMANCE REPORT")
print("========================================")

if performance_data:

    stt_times = [x["stt_time"] for x in performance_data]
    speaking_times = [x["speaking_time"] for x in performance_data]
    total_times = [x["total_time"] for x in performance_data]

    # --------------------------------------
    # MEAN
    # --------------------------------------

    mean_stt = statistics.mean(stt_times)
    mean_speaking = statistics.mean(speaking_times)
    mean_total = statistics.mean(total_times)

    # --------------------------------------
    # VARIANCE
    # --------------------------------------

    variance_stt = statistics.variance(stt_times) \
        if len(stt_times) > 1 else 0

    variance_speaking = statistics.variance(speaking_times) \
        if len(speaking_times) > 1 else 0

    variance_total = statistics.variance(total_times) \
        if len(total_times) > 1 else 0

    # --------------------------------------
    # MIN/MAX
    # --------------------------------------

    min_stt = min(stt_times)
    max_stt = max(stt_times)

    # ======================================
    # SUMMARY
    # ======================================

    print("\nSUMMARY")
    print("----------------------------------------")

    print(f"Questions Processed : {len(performance_data)}")

    print(f"\nMean STT Time       : {mean_stt:.3f} sec")
    print(f"Variance STT Time   : {variance_stt:.6f}")

    print(f"\nMean Speaking Time  : {mean_speaking:.3f} sec")
    print(f"Variance Speaking   : {variance_speaking:.6f}")

    print(f"\nMean Total Time     : {mean_total:.3f} sec")
    print(f"Variance Total Time : {variance_total:.6f}")

    print(f"\nFastest STT Time    : {min_stt:.3f} sec")
    print(f"Slowest STT Time    : {max_stt:.3f} sec")

    # ======================================
    # PER QUESTION REPORT
    # ======================================

    print("\nPER QUESTION REPORT")
    print("----------------------------------------")

    for item in performance_data:

        print(
            f"Q{item['question_id']} | "
            f"Text='{item['recognized_text']}' | "
            f"Speak={item['speaking_time']:.2f}s | "
            f"STT={item['stt_time']:.2f}s | "
            f"Total={item['total_time']:.2f}s"
        )

else:

    print("No performance data collected.")

# ==========================================
# FINAL SCORE
# ==========================================

print("\n========================================")
print(f"FINAL SCORE: {score}/{len(questions)}")
print("========================================")

speak(
    f"Quiz completed. "
    f"Your final score is "
    f"{score} out of {len(questions)}."
)
