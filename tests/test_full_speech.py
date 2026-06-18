from modules.speech_analysis import (
    speech_to_text,
    calculate_wpm,
    count_fillers
)

# Transcribe audio
text = speech_to_text(
    "recordings/interview_audio.wav"
)

print("\nTRANSCRIPTION:\n")
print(text)

# Example: if interview lasted 60 seconds
duration = 60

wpm = calculate_wpm(
    text,
    duration
)

fillers = count_fillers(text)

print("\nWPM:", wpm)
print("Filler Words:", fillers)