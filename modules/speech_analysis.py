import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np
import os
from datetime import datetime

audio_data = []
sample_rate = 44100
recording = False

def record_audio(duration=30,
                 filename="recordings/interview_audio.wav"):

    sample_rate = 44100

    print("Recording started...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write(
        filename,
        sample_rate,
        audio
    )

    print("Recording saved:", filename)

    return filename

def speech_to_text(audio_file):

    print("Loading Whisper Model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("Transcribing...")

    segments, info = model.transcribe(audio_file,language="en")

    text = ""

    for segment in segments:
        text += segment.text + " "

    print("Transcription Complete")

    return text.strip()

def calculate_wpm(text, duration_seconds):

    words = len(text.split())

    minutes = duration_seconds / 60

    if minutes == 0:
        return 0

    wpm = words / minutes

    return round(wpm, 2)


def count_fillers(text):

    fillers = [
        "um",
        "uh",
        "actually",
        "basically",
        "like"
    ]

    text = text.lower()

    count = 0

    for filler in fillers:
        count += text.count(filler)

    return count

def audio_callback(indata, frames, time, status):

    if recording:
        audio_data.append(indata.copy())


def start_recording():

    global recording, audio_data

    audio_data = []

    recording = True

    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        callback=audio_callback
    )

    stream.start()

    return stream


def stop_recording(
        stream,
        filename=None
):

    global recording

    if filename is None:

        os.makedirs(
            "recordings",
            exist_ok=True
        )

        filename = (
            "recordings/" +
            datetime.now().strftime(
                "%Y%m%d_%H%M%S.wav"
            )
        )
        
    recording = False
  
    stream.stop()
    stream.close()

    if len(audio_data) == 0:
        return None

    audio = np.concatenate(
        audio_data,
        axis=0
    )

    write(
        filename,
        sample_rate,
        audio
    )

    print("Audio saved:", filename)

    return filename