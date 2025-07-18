import speech_recognition as sr
import webbrowser
import pyttsx3
import psutil
import time
import sys


try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    print("Speech engine initialized successfully")
except Exception as e:
    print(f"Failed to initialize speech engine: {e}")
    sys.exit(1)

recognizer = sr.Recognizer()
wake_words = ["jarvis", "neo", "kairo"]


def speak(text):
    """Reliable speaking function"""
    print(f"🗣️ {text}")
    try:
        # Clear any pending speech commands
        engine.stop()
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)
    except Exception as e:
        print(f"Speech error: {e}")


def listen(prompt="🎤 Listening...", timeout=5, phrase_time_limit=5):
    """Improved listening function"""
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(prompt)
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return audio
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return None
        except Exception as e:
            print(f" Listening error: {e}")
            return None


def is_wake_word(text):
    """Check for wake words"""
    if not text:
        return False
    return any(word in text.lower() for word in wake_words)


def close_browser():
    """Close browsers reliably"""
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe"]
    closed = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() in browsers:
            try:
                proc.kill()
                closed = True
            except Exception as e:
                print(f"Couldn't close {proc.info['name']}: {e}")
    return closed


def process_command(command):
    """Process commands with exact matching"""
    command = command.lower()
    print(f"Processing command: {command}")

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif any(cmd in command for cmd in ["close youtube", "close browser"]):
        if close_browser():
            speak("Browser closed successfully")
        else:
            speak("No browsers were open")

    elif "your name" in command:
        speak("I am Kairo, your voice assistant")

    elif any(cmd in command for cmd in ["exit", "quit", "goodbye"]):
        speak("Goodbye! Shutting down now.")
        sys.exit(0)

    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    else:
        speak("I didn't understand that command. Please try again.")


if __name__ == "__main__":
    print("Kairo Voice Assistant Initializing...")
    speak("Kairo is ready. Say my name to activate me.")

    while True:
        try:
           
            audio = listen(prompt="🔈 Say Jarvis, Neo, or Kairo to activate...",
                           timeout=None,
                           phrase_time_limit=4)

            if audio:
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")

                    if is_wake_word(text):
                        speak("Yes? How can I help you?")

                        # Command processing loop
                        while True:
                            command_audio = listen(
                                prompt="🎤 Waiting for your command...",
                                timeout=8,
                                phrase_time_limit=8)

                            if not command_audio:
                                speak(
                                    "I didn't hear a command. Say exit to quit or try again.")
                                continue

                            try:
                                command = recognizer.recognize_google(
                                    command_audio)
                                print(f"Command: {command}")

                                # Exit command loop if user says exit
                                if any(cmd in command.lower() for cmd in ["exit", "quit", "goodbye"]):
                                    process_command(command)
                                    break

                                process_command(command)

                            except sr.UnknownValueError:
                                speak("Sorry, I didn't catch that. Please repeat.")
                            except sr.RequestError:
                                speak("Network error. Please check your internet.")
                                break

                except sr.UnknownValueError:
                    print("⚠️ Couldn't understand audio")
                except sr.RequestError as e:
                    print(f"❌ API error: {e}")
                    speak("Sorry, I'm having trouble with the speech service.")

        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            speak("Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(1)
