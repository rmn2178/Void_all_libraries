import speech_recognition as sr
import whisper
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# 1. Load the model (Base is good, Tiny is fastest)
print("Loading Whisper model...")
model = whisper.load_model("base")


def start_listening():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n--- SYSTEM ONLINE (FFmpeg-Free Mode) ---")
        print("Calibrating for room noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print(">>> Ready! Speak now...")

        try:
            while True:
                # 2. Capture audio from microphone
                audio_data = recognizer.listen(source, phrase_time_limit=10)

                # 3. Convert raw audio bytes to a NumPy array
                # Whisper expects 16,000Hz mono audio
                raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)

                # Convert buffer to int16, then normalize to float32 between -1 and 1
                audio_np = np.frombuffer(raw_data, np.int16).astype(np.float32) / 32768.0

                # 4. Transcribe the array directly
                result = model.transcribe(audio_np, fp16=False)

                text = result['text'].strip()
                if text:
                    print(f"Detected: {text}")

        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    start_listening()