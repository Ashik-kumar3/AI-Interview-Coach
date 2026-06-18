from modules.speech_analysis import speech_to_text

text = speech_to_text(
    "recordings/interview_audio.wav"
)

print("\nTRANSCRIBED TEXT:\n")
print(text)