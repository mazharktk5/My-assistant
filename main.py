import speech_recognition as sr
import webbrowser
import pyttsx3
import psutil
import time
import sys

# Initialize speech engine with better error handling
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Try 0 or 1 for different voices
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"❌ Failed to initialize speech engine: {e}")
    sys.exit(1)

recognizer = sr.Recognizer()
wake_words = ["jarvis", "neo", "kairo", "computer"]


def speak(text, wait=True):
    """Improved speak function with better error handling"""
    print(f"🗣️ {text}")
    try:
        engine.say(text)
        if wait:
            engine.runAndWait()
        else:
            engine.startLoop(False)
            engine.iterate()
            time.sleep(0.1)  # Small delay for non-blocking speech
    except Exception as e:
        print(f"❌ Speech error: {e}")


def listen(prompt="🎤 Listening...", timeout=5, phrase_time_limit=5):
    """Enhanced listening function with better mic handling"""
    with sr.Microphone() as source:
        print("🔊 Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(prompt)
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return audio
        except sr.WaitTimeoutError:
            print("⏰ Timeout: No speech detected.")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return None


def is_wake_word(text):
    """Check for wake words with fuzzy matching"""
    text_lower = text.lower()
    return any(word in text_lower for word in wake_words)


def close_browser():
    """Close browsers more reliably"""
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe"]
    closed = False
    for proc in psutil.process_iter(['name']):
        if proc.info["name"].lower() in browsers:
            try:
                proc.kill()
                closed = True
            except Exception as e:
                print(f"⚠️ Couldn't close {proc.info['name']}: {e}")
    return closed


def process_command(command):
    """Process commands with better matching"""
    command = command.lower()

    if any(word in command for word in ["youtube", "watch video"]):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif any(word in command for word in ["google", "search"]):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif any(word in command for word in ["close browser", "stop browser"]):
        if close_browser():
            speak("All browsers closed successfully")
        else:
            speak("No browsers were open")

    elif any(word in command for word in ["your name", "who are you"]):
        speak("I am Kairo, your personal voice assistant")

    elif any(word in command for word in ["exit", "quit", "goodbye"]):
        speak("Goodbye! Have a great day!")
        sys.exit(0)

    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    else:
        speak("I didn't understand that command. Try something else.")


if __name__ == "__main__":
    print("🚀 Kairo Voice Assistant Initializing...")
    speak("Kairo is ready. Say my name to activate me.")

    while True:
        try:
            # Listen for wake word
            audio = listen(prompt="🔈 Say a wake word: Jarvis, Neo, or Kairo...",
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
                                prompt="🎤 Listening for your command...",
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
                                process_command(command)
                            except sr.UnknownValueError:
                                speak("Sorry, I didn't catch that. Please repeat.")
                            except sr.RequestError:
                                speak(
                                    "Network error. Please check your internet connection.")
                                break

                except sr.UnknownValueError:
                    print("⚠️ Couldn't understand audio")
                except sr.RequestError as e:
                    print(f"❌ API error: {e}")
                    speak("Sorry, I'm having trouble connecting to the speech service.")

        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            speak("Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            speak("Sorry, something went wrong. I'll restart.")
            time.sleep(1)
