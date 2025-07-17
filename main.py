import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

wake_words = ["kairo", "cairo"]  # Accept both


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=4)
    return audio


def is_wake_word(text):
    return any(word in text.lower() for word in wake_words)


if __name__ == "__main__":
    print("Kairo initializing")
    speak("Kairo initializing")

    while True:
        try:
            audio = listen()
            trigger = recognizer.recognize_google(audio)
            print(f"You said: {trigger}")

            if is_wake_word(trigger):
                speak("Hello, how can I assist you?")

                try:
                    command_audio = listen()
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
                    speak("Sorry, I didn't catch that.")
            else:
                print("👂 Wake word not detected.")
                speak("Say my name to activate me.")

        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
            speak("Say my name to activate me.")
        except sr.RequestError:
            print("❌ Could not reach Google. Check your internet.")
