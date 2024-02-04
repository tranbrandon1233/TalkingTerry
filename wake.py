import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import tempfile

# Initialize Pygame mixer
pygame.mixer.init()

def speak(text):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=text, lang='en')
        tts.save(f"{fp.name}.mp3")
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

def listen():
    # Initialize recognizer
    r = sr.Recognizer()

    # Open the microphone
    with sr.Microphone() as source:
        print("Please say something:")
        audio = r.listen(source)

    # Recognize speech using Sphinx
    try:
        text = r.recognize_sphinx(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Sphinx service; {e}")
        return None

if __name__ == "__main__":
    text = listen()
    if text and 'testing' in text.lower():
        response = "Hi"
        speak(response)
    elif text:
        response = f"I heard you say: {text}"
        speak(response)
