total_frames = 0
good_posture_frames = 0


def get_posture(landmarks, w, h):

    global total_frames
    global good_posture_frames

    score = 0

    nose = landmarks[0]

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    nose_x = int(nose.x * w)

    ls_x = int(left_shoulder.x * w)
    ls_y = int(left_shoulder.y * h)

    rs_x = int(right_shoulder.x * w)
    rs_y = int(right_shoulder.y * h)

    shoulder_center_x = (ls_x + rs_x) // 2

    shoulder_diff = abs(ls_y - rs_y)

    neck_offset = abs(nose_x - shoulder_center_x)

    total_frames += 1

    if shoulder_diff < 20 and neck_offset < 40:

        status = "Good Posture"
        good_posture_frames += 1

    else:
        status = "Poor Posture"

    if total_frames > 0:
        score = int(
            (good_posture_frames / total_frames) * 100
        )

    return score, status