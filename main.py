import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

wake_words = ["kairo", "cairo"]


def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()


def listen(prompt="🎤 Listening...", timeout=5, phrase_time_limit=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(prompt)
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return audio
        except sr.WaitTimeoutError:
            print("⏰ Timeout: No speech detected.")
            return None


def is_wake_word(text):
    return any(word in text.lower() for word in wake_words)


if __name__ == "__main__":
    print("Kairo initializing...")
    speak("Kairo initializing")

    while True:
        # Step 1: Wait for wake word
        trigger_audio = listen(
            prompt="🎤 Say my name to activate me...", timeout=10, phrase_time_limit=5)
        if trigger_audio is None:
            continue

        try:
            trigger_text = recognizer.recognize_google(trigger_audio)
            print(f"You said: {trigger_text}")
        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
            continue
        except sr.RequestError:
            speak("Can't connect to Google. Check your internet.")
            continue

        if is_wake_word(trigger_text):
            speak("I am Kairo, how can I help you?")

            # Step 2: Listen for command after wake word
            command_audio = listen(
                prompt="🎤 Listening for your command...", timeout=8, phrase_time_limit=6)
            if command_audio is None:
                speak("I didn't hear any command.")
                continue

            try:
                command = recognizer.recognize_google(command_audio).lower()
                print(f"Command: {command}")
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that.")
                continue
            except sr.RequestError:
                speak("Can't connect to Google.")
                continue

            # Step 3: Match commands
            if "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif "open google" in command:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")

            elif "what is your name" in command:
                speak("My name is Kairo")

            elif "exit" in command or "quit" in command:
                speak("Goodbye")
                break

            else:
                speak("Sorry, I don't recognize that command.")
        else:
            speak("Say my name to activate me.")
