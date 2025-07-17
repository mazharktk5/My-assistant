import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import psutil
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()
wake_words = ["kairo", "cairo"]


def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()


def listen(prompt="🎤 Listening...", timeout=5, phrase_time_limit=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
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


def close_browser():
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe"]
    closed = False
    for proc in psutil.process_iter(['name']):
        if proc.info["name"] in browsers:
            try:
                proc.kill()
                closed = True
            except Exception:
                pass
    return closed


if __name__ == "__main__":
    print("Kairo initializing...")
    speak("Kairo initializing")

    while True:
        # Wait for wake word
        audio = listen(prompt="🎤 Say my name to activate me...",
                       timeout=None, phrase_time_limit=5)
        if audio is None:
            continue

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
            continue
        except sr.RequestError:
            speak("Can't connect to Google. Check your internet.")
            continue

        if is_wake_word(text):
            speak("I am Kairo, how can I help you?")

            # Start continuous command loop
            while True:
                command_audio = listen(
                    prompt="🎤 Listening for your command...", timeout=10, phrase_time_limit=6)
                if command_audio is None:
                    speak("Didn't hear a command. Say 'exit' to quit or keep speaking.")
                    continue

                try:
                    command = recognizer.recognize_google(
                        command_audio).lower()
                    print(f"Command: {command}")
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
                    continue
                except sr.RequestError:
                    speak("Can't connect to Google.")
                    break

                # Command actions
                if "open youtube" in command:
                    speak("Opening YouTube")
                    webbrowser.open("https://www.youtube.com")

                elif "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")

                elif "close youtube" in command or "close browser" in command:
                    if close_browser():
                        speak("Browser closed.")
                    else:
                        speak("No browser found open.")

                elif "what is your name" in command:
                    speak("My name is Kairo")

                elif "exit" in command or "quit" in command:
                    speak("Goodbye!")
                    exit()

                else:
                    speak("Sorry, I don't recognize that command.")
