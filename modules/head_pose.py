total_frames = 0
stable_frames = 0


def get_head_pose(face_landmarks, w, h):

    global total_frames
    global stable_frames

    score = 0

    nose = face_landmarks.landmark[1]
    left_face = face_landmarks.landmark[234]
    right_face = face_landmarks.landmark[454]

    left_eye = face_landmarks.landmark[33]
    right_eye = face_landmarks.landmark[263]

    nose_x = int(nose.x * w)
    nose_y = int(nose.y * h)

    left_x = int(left_face.x * w)
    right_x = int(right_face.x * w)

    left_eye_y = int(left_eye.y * h)
    right_eye_y = int(right_eye.y * h)

    face_center_x = (left_x + right_x) // 2

    horizontal_offset = nose_x - face_center_x

    eye_level = (left_eye_y + right_eye_y) // 2

    vertical_offset = nose_y - eye_level

    total_frames += 1

    if horizontal_offset < -25:
        status = "Looking Left"

    elif horizontal_offset > 25:
        status = "Looking Right"

    elif vertical_offset < 55:
        status = "Looking Up"

    elif vertical_offset > 95:
        status = "Looking Down"

    else:
        status = "Facing Forward"
        stable_frames += 1

    if total_frames > 0:
        score = int((stable_frames / total_frames) * 100)

    return score, status