import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

wake_words = ["kairo", "cairo"]


def speak(text):
    print(f"🗣️ {text}")  # helpful for debugging
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
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
        audio = listen()
        if audio is None:
            speak("Say my name to activate me.")
            continue

        try:
            trigger = recognizer.recognize_google(audio)
            print(f"You said: {trigger}")

            if is_wake_word(trigger):
                speak("I am Kairo, how can I help you?")

                command_audio = listen()
                if command_audio is None:
                    speak("Sorry, I didn't hear your command.")
                    continue

                try:
                    command = recognizer.recognize_google(command_audio)
                    command = command.lower()
                    print(f"Command: {command}")

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
                        speak("Sorry, I didn't understand that command.")

                except sr.UnknownValueError:
                    print("⚠️ Could not understand the command.")
                    speak("Sorry, I didn't catch that.")

            else:
                speak("Say my name to activate me.")

        except sr.UnknownValueError:
            print("⚠️ Could not understand speech.")
            speak("Say my name to activate me.")

        except sr.RequestError:
            print("❌ Could not reach Google. Check your internet.")
            speak("I can't reach Google. Please check your internet.")
