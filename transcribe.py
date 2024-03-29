from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
import tempfile
import shutil
import base64
import pyaudio
import wave
import collections
import os
from openai import OpenAI
import websockets
from websockets.sync.client import connect
import asyncio
import json

# mpv
import shutil
import subprocess

from GCP import upload_blob_from_memory, download_blob_into_memory
load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
GCP_BUCKET = os.getenv("GCP_BUCKET")
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

from Controller import Controller


def is_installed(lib_name):
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True


def get_levels(data, long_term_noise_level, current_noise_level):
    pegel = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
    long_term_noise_level = long_term_noise_level * 0.995 + pegel * (1.0 - 0.995)
    current_noise_level = current_noise_level * 0.920 + pegel * (1.0 - 0.920)
    return pegel, long_term_noise_level, current_noise_level


async def text_chunker(chunks):
    """Used during input streaming to chunk text blocks and set last char to space"""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""
    async for text in chunks:
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


async def generate_stream_input(first_text_chunk, text_generator, voice, model):
    BOS = json.dumps(
        dict(
            text=" ",
            try_trigger_generation=True,
            voice_settings=voice["settings"],
            generation_config=dict(chunk_length_schedule=[50]),
        )
    )
    EOS = json.dumps({"text": ""})

    with connect(
        f"""wss://api.elevenlabs.io/v1/text-to-speech/{voice["voice_id"]}/stream-input?model_id={model["model_id"]}""",
        additional_headers={
            "xi-api-key": elevenlabs_api_key,
        },
    ) as websocket:
        websocket.send(BOS)

        # Send the first text chunk immediately
        first_data = dict(text=first_text_chunk, try_trigger_generation=True)
        websocket.send(json.dumps(first_data))

        # Stream text chunks and receive audio
        async for text_chunk in text_chunker(text_generator):
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


async def stream_output(audio_stream):
    if not is_installed("mpv"):
        message = (
            "mpv not found, necessary to stream audio. "
            "On mac you can install it with 'brew install mpv'. "
            "On linux and windows you can install it from https://mpv.io/"
        )
        raise ValueError(message)

    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    audio = b""

    async for chunk in audio_stream:
        if chunk is not None:
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore
            audio += chunk

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()

    return audio


async def main():
    controller = Controller()
    client = OpenAI()
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
                data, long_term_noise_level, current_noise_level
            )
            audio_buffer.append(data)

            if (
                not voice_activity_detected
                and current_noise_level > long_term_noise_level + 300
            ):
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

        with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ) as temp_audio_file:
            with wave.open(temp_audio_file.name, "wb") as wf:
                wf.setparams(
                    (
                        1,
                        audio.get_sample_size(pyaudio.paInt16),
                        16000,
                        0,
                        "NONE",
                        "NONE",
                    )
                )
                wf.writeframes(audio_data)
            with open(temp_audio_file.name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="text"
                )
        os.remove(temp_audio_file.name)
        print(f"Transcribed:{transcript}\n<<< ", end="", flush=True)
        upload_blob_from_memory(GCP_BUCKET,transcript+'\n\n'+download_blob_into_memory(GCP_BUCKET,'transcript.txt').decode('utf-8'), 'transcript.txt')
        model = {
            "model_id": "eleven_multilingual_v2",
        }

        text_generator = controller.invoke(transcript)
        first_text_chunk = await text_generator.__anext__()
        print("First text data received:", first_text_chunk)
        await stream_output(
            generate_stream_input(first_text_chunk, text_generator, voice, model)
        )


import asyncio

asyncio.run(main())
