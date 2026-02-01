import speech_recognition as sr
import pyttsx3
import whisper
import numpy as np
import ollama
import warnings
import re
import sys

# --- CONFIGURATION ---
WAKE_WORD = "jarvis"
OLLAMA_MODEL = "llama3.2"

# Suppress Warnings
warnings.filterwarnings("ignore")


# --- 1. SETUP TEXT-TO-SPEECH ---
def setup_tts_engine():
    engine = pyttsx3.init()
    # Speed: 175 is a good conversational pace
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)

    # Try to set a specific voice (optional)
    voices = engine.getProperty('voices')
    if len(voices) > 0:
        # Index 0 is usually Male, 1 is Female
        engine.setProperty('voice', voices[0].id)
    return engine


tts_engine = setup_tts_engine()


def speak(text):
    """
    Prints the text and speaks it immediately.
    This blocks code execution until speaking is done.
    """
    # Print with a tag so you know who is talking
    print(f"[Jarvis]: {text}")

    # Clean text of asterisks (*) often used by AI for actions
    clean_text = text.replace("*", "")
    tts_engine.say(clean_text)
    tts_engine.runAndWait()


# --- 2. SETUP SPEECH-TO-TEXT (Whisper) ---
print("[System] Loading Whisper Model... (Please wait)")
whisper_model = whisper.load_model("base")


# --- 3. HELPER: LISTEN FOR COMMAND ---
def listen_for_command(recognizer, source):
    """
    Listens for the main command after the wake word is triggered.
    """
    print("\n[System] Listening for command...")
    try:
        # Listen for up to 5 seconds of silence, max 10 seconds of speech
        audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        # Notify user that processing has started
        print("[System] Transcribing audio...")

        # Prepare audio for Whisper
        raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        audio_np = np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0

        # Transcribe
        result = whisper_model.transcribe(audio_np, fp16=False)
        return result['text'].strip()
    except sr.WaitTimeoutError:
        return None
    except Exception as e:
        print(f"[Error] {e}")
        return None


# --- 4. MAIN LOOP ---
def start_jarvis():
    recognizer = sr.Recognizer()

    # Check Microphone
    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone Error: {e}")
        return

    with mic as source:
        print("\n--- JARVIS ONLINE ---")
        # Notify: Calibration
        speak("Calibrating background sensors...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        # Notify: Ready
        speak("I am ready. Waiting for wake word.")

        while True:
            try:
                # A. Listen for Wake Word (Offline Sphinx)
                # We do NOT speak here, or it would loop forever.
                # Just listen silently for "Jarvis"
                audio = recognizer.listen(source, phrase_time_limit=3)

                # Sensitivity: 1e-15 (Adjust if too sensitive/insensitive)
                wake_text = recognizer.recognize_sphinx(audio, keyword_entries=[(WAKE_WORD, 1e-15)])

                if WAKE_WORD in wake_text.lower():
                    # CONDITION 1: Wake Word Detected
                    speak("Yes, sir?")

                    # CONDITION 2: Listen for User Command
                    user_command = listen_for_command(recognizer, source)

                    if user_command:
                        # CONDITION 3: Confirm Input
                        print(f"User: {user_command}")
                        speak(f"You asked: {user_command}")

                        # CONDITION 4: Thinking/Processing
                        speak("Thinking...")

                        # CONDITION 5: Streaming Response
                        stream = ollama.generate(model=OLLAMA_MODEL, prompt=user_command, stream=True)

                        print("Jarvis Response: ", end="")

                        # Buffer for sentence-by-sentence speech
                        sentence_buffer = ""

                        for chunk in stream:
                            text_part = chunk['response']

                            # Visual: Print word-by-word
                            print(text_part, end="", flush=True)

                            # Audio: Build the sentence
                            sentence_buffer += text_part

                            # Check for sentence endings (. ? !)
                            if re.search(r'[.!?](\s|\n)', sentence_buffer):
                                # Speak the complete sentence
                                tts_engine.say(sentence_buffer)
                                tts_engine.runAndWait()
                                sentence_buffer = ""  # Clear buffer

                        # Speak any remaining words (incomplete sentence)
                        if sentence_buffer.strip():
                            tts_engine.say(sentence_buffer)
                            tts_engine.runAndWait()

                        print("\n")  # Formatting

                    else:
                        # Condition: No command heard
                        speak("I didn't hear a command, sir.")

            except sr.UnknownValueError:
                pass  # Normal background noise
            except sr.RequestError as e:
                print(f"[Sphinx Error] {e}")
            except KeyboardInterrupt:
                speak("Shutting down systems.")
                break


if __name__ == "__main__":
    start_jarvis()