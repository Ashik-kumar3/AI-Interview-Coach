import cv2

# Score variables
total_frames = 0
center_frames = 0


def get_eye_contact(face_landmarks, w, h):

    global total_frames
    global center_frames

    status = "No Face"
    score = 0

    left_corner = face_landmarks.landmark[33]
    right_corner = face_landmarks.landmark[133]
    iris = face_landmarks.landmark[468]

    lx = int(left_corner.x * w)
    rx = int(right_corner.x * w)
    ix = int(iris.x * w)

    eye_width = rx - lx

    if eye_width > 0:

        ratio = (ix - lx) / eye_width

        total_frames += 1

        if ratio < 0.35:
            status = "Looking Right"

        elif ratio > 0.65:
            status = "Looking Left"

        else:
            status = "Looking Center"
            center_frames += 1

    if total_frames > 0:
        score = int((center_frames / total_frames) * 100)

    return score, status