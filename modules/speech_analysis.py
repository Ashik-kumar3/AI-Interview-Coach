import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


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