import speech_recognition as sr

def start_wake_word_detection():
    r = sr.Recognizer()

    # Check if we can find the microphone
    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone Error: {e}")
        return

    with mic as source:
        print("Wait... calibrating background noise.")
        r.adjust_for_ambient_noise(source, duration=2)

        # Lowering energy threshold makes it more sensitive to quiet speech
        r.energy_threshold = 300

        print("Listening natively for 'jarvis'...")

        while True:
            try:
                # phrase_time_limit: stops recording after 2 secs even if user is still talking
                audio = r.listen(source, phrase_time_limit=3)

                # recognize_sphinx is the native, offline engine
                # Use a very small threshold for higher sensitivity
                text = r.recognize_sphinx(audio, keyword_entries=[("jarvis", 1e-10)])

                if "jarvis" in text.lower():
                    print(">>> Wake word detected!")
                    # Optional: Add a 'beep' sound here so you know it triggered

            except sr.UnknownValueError:
                # This is normal; it means no speech was recognized in the audio chunk
                pass
            except sr.RequestError as e:
                print(f"Sphinx error; {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")


if __name__ == "__main__":
    start_wake_word_detection()