import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

assistant_name = "Kairo"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)
    return audio


if __name__ == "__main__":
    print(f"{assistant_name} initializing")
    speak(f"{assistant_name} initializing")

    while True:
        try:
            audio = listen()
            trigger = recognizer.recognize_google(audio)
            print(f"You said: {trigger}")

            if trigger.lower() == assistant_name.lower():
                speak("Hello, how can I assist you?")

                try:
                    command_audio = listen()
                    command = recognizer.recognize_google(command_audio)
                    command = command.lower()
                    print(f"Command: {command}")

                    # Example: open YouTube
                    if "open youtube" in command:
                        speak("Opening YouTube")
                        webbrowser.open("https://www.youtube.com")

                    elif "open google" in command:
                        speak("Opening Google")
                        webbrowser.open("https://www.google.com")

                    elif "what is your name" in command:
                        speak(f"My name is {assistant_name}")

                    elif "exit" in command or "quit" in command:
                        speak("Goodbye")
                        break

                    else:
                        speak("Sorry, I didn't understand that command.")

                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
        except sr.UnknownValueError:
            pass  # ignore unrecognized wake-up attempts
        except sr.RequestError:
            print("❌ Could not reach Google. Check your internet.")
