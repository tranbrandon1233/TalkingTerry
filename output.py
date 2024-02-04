from gtts import gTTS
import pygame
import tempfile

# Initialize Pygame mixer
pygame.mixer.init()

def speak(text):
    # Create a temporary file to store the audio from gTTS
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        # Generate the speech audio file
        tts = gTTS(text=text, lang='en')
        tts.save(f"{fp.name}.mp3")
        
        # Load the audio file with Pygame and play it
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            continue

# Example usage
if __name__ == "__main__":
    speak("Hello, this is a test of the Raspberry Pi speaker.")
