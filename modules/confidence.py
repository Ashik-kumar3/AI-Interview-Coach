def calculate_confidence(
        eye_score,
        head_score,
        posture_score,
        communication_score
):

    confidence = (
        eye_score * 0.25 +
        head_score * 0.20 +
        posture_score * 0.20 +
        communication_score * 0.35
    )

    return round(confidence, 2)

def calculate_communication_score(
        wpm,
        filler_count
):

    # WPM Score

    if 100 <= wpm <= 150:
        wpm_score = 100

    elif 80 <= wpm < 100:
        wpm_score = 80

    elif 150 < wpm <= 180:
        wpm_score = 80

    else:
        wpm_score = 50

    # Filler Score

    filler_score = max(
        0,
        100 - (filler_count * 10)
    )

    communication_score = (
        wpm_score * 0.6 +
        filler_score * 0.4
    )

    return round(
        communication_score,
        2
    )