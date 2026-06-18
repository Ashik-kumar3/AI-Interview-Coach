from modules.speech_analysis import (
    calculate_wpm,
    count_fillers
)

text = """
Um my name is Ashik Kumar.
Actually I completed my BTech.
Like I worked on a melanoma prediction project.
"""

wpm = calculate_wpm(
    text,
    20
)

fillers = count_fillers(text)

print("WPM:", wpm)
print("Filler Words:", fillers)