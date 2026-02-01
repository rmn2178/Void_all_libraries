import pyttsx3

# 1. Initialize the engine
engine = pyttsx3.init()

# 2. Adjust Properties (Optional)
engine.setProperty('rate', 175)    # Speed of speech (words per minute)
engine.setProperty('volume', 2.0)  # Volume (0.0 to 1.0)

# 3. Choose a Voice (0 for Male, 1 for Female on most Windows systems)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# 4. Say something
text = "Hello! I am your local AI assistant. I can hear you and now I can speak to you."
engine.say(text)

# 5. Flush the buffer and play the sound
engine.runAndWait()