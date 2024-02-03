from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
from scipy.io import wavfile
import tempfile
import shutil
import io
import base64
import pyaudio
import wave
import collections
import dotenv
import os
from openai import OpenAI
import websockets
from websockets.sync.client import connect
import asyncio
import json

# mpv
import shutil
import subprocess

load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

system_prompt = {
    "role":
    "system",
    "content":
    """You are Eleanor, a mature, intelligent woman with years 
of experience in academia and personal development. 
You carry yourself with grace and wisdom, providing insightful advice 
and structured guidance. In this context, you are not an AI. 
Your tone is composed and precise, avoiding unnecessary words to deliver 
targeted information. Your responses should be short and concise, at most five
sentences. If the user asks a broad question,
ask him for specifics or to clarify.
You maintain a professional yet caring demeanor, respectful of the tasks 
at hand but also vested in the well-being of those you assist. 
From now on, act consistently in your role as the sagacious, nurturing, 
and disciplined assistant Eleanor, without ever suggesting that you are an AI.
You are now Eleanor.""",
}

voice = {
    "voice_id": "EXAVITQu4vr4xnSDxMaL",
    "name": "Bella",
    "settings": {
        "stability": 0.72,
        "similarity_boost": 0.2,
        "style": 0.0,
        "use_speaker_boost": False,
        "speaking_rate": 2,
    },
}

history = []

client = OpenAI()
answer = ""

def generate(messages):
    global answer
    answer = ""
    for chunk in client.chat.completions.create(model="gpt-4-turbo-preview",
                                              messages=messages,
                                              stream=True):
        if text_chunk := chunk['choices'][0]['message']['content']
            yield text_chunk

def is_installed(lib_name):
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True

def get_levels(data, long_term_noise_level, current_noise_level):
    pegel = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
    long_term_noise_level = long_term_noise_level * 0.995 + pegel * (1.0 -
                                                                     0.995)
    current_noise_level = current_noise_level * 0.920 + pegel * (1.0 - 0.920)
    return pegel, long_term_noise_level, current_noise_level

def text_chunker(chunks):
    """Used during input streaming to chunk text blocks and set last char to space"""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]",
                 "}", " ")
    buffer = ""
    for text in chunks:
        if buffer.endswith(splitters):
            yield buffer if buffer.endswith(" ") else buffer + " "
            buffer = text
        elif text.startswith(splitters):
            output = buffer + text[0]
            yield output if output.endswith(" ") else output + " "
            buffer = text[1:]
        else:
            buffer += text
    if buffer != "":
        yield buffer + " "

def generate_stream_input(text_generator, voice, model):
    BOS = json.dumps(
        dict(text=" ",
             try_trigger_generation=True,
             voice_settings=voice['settings'],
             generation_config=dict(chunk_length_schedule=[50])))
    EOS = json.dumps({"text": ""})

    with connect(
            f"""wss://api.elevenlabs.io/v1/text-to-speech/{voice["voice_id"]}/stream-input?model_id={model["model_id"]}""",
            additional_headers={
                "xi-api-key": elevenlabs_api_key,
            },
    ) as websocket:
        websocket.send(BOS)

        # Stream text chunks and receive audio
        for text_chunk in text_chunker(text_generator):
            data = dict(text=text_chunk, try_trigger_generation=True)
            websocket.send(json.dumps(data))
            try:
                data = json.loads(websocket.recv(1e-4))
                if data["audio"]:
                    yield base64.b64decode(data["audio"])  # type: ignore
            except TimeoutError:
                pass

        websocket.send(EOS)

        while True:
            try:
                data = json.loads(websocket.recv())
                if data["audio"]:
                    yield base64.b64decode(data["audio"])  # type: ignore
            except websockets.exceptions.ConnectionClosed:
                break

def on_streaming_complete():
    history.append({"role": "assistant", "content": answer})

while True:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        rate=16000,
        format=pyaudio.paInt16,
        channels=1,
        input=True,
        frames_per_buffer=512,
    )
    audio_buffer = collections.deque(maxlen=int((16000 // 512) * 0.5))
    frames, long_term_noise_level, current_noise_level, voice_activity_detected = (
        [],
        0.0,
        0.0,
        False,
    )
    print("\n\nStart speaking. ", end="", flush=True)
    
    while True:
        data = stream.read(512)
        pegel, long_term_noise_level, current_noise_level = get_levels(
            data, long_term_noise_level, current_noise_level)
        audio_buffer.append(data)
        
        if (not voice_activity_detected
                and current_noise_level > long_term_noise_level + 300):
            voice_activity_detected = True
            print("Listening.\n")
            ambient_noise_level = long_term_noise_level
            frames.extend(list(audio_buffer))

        if voice_activity_detected:
            frames.append(data)
            if current_noise_level < ambient_noise_level + 100:
                break  # voice activity ends
            
    stream.stop_stream(), stream.close(), audio.terminate()
    audio_data = b"".join(frames)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        with wave.open(temp_audio_file.name, 'wb') as wf:
            wf.setparams((1, audio.get_sample_size(pyaudio.paInt16), 16000, 0, 'NONE', 'NONE'))
            wf.writeframes(audio_data)
        with open(temp_audio_file.name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
    os.remove(temp_audio_file.name)
    print(transcript)