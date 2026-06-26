import cv2
import mediapipe as mp
import time

from modules.questions import load_questions
from modules.eye_contact import get_eye_contact
from modules.head_pose import get_head_pose
from modules.posture import get_posture
from modules.confidence import ( calculate_confidence, calculate_communication_score )
from modules.report import generate_report
from modules.speech_analysis import ( start_recording, stop_recording, speech_to_text, calculate_wpm, count_fillers)
from modules.feedback import generate_feedback
from modules.interview_type import select_interview_type
from modules.pdf_report import generate_pdf_report

# MediaPipe Setup
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Webcam
cap = cv2.VideoCapture(0)

audio_stream = start_recording()

print("Interview recording started...")

# Start interview timer
start_time = time.time()

choice = select_interview_type()

if choice == "1":

    interview_type = "HR Interview"

    questions = load_questions(
        "assets/hr_questions.txt"
    )

elif choice == "2":

    interview_type = "Technical Interview"

    questions = load_questions(
        "assets/technical_questions.txt"
    )

else:

    interview_type = "HR + Technical Interview"

    hr_questions = load_questions(
        "assets/hr_questions.txt"
    )

    technical_questions = load_questions(
        "assets/technical_questions.txt"
    )

    questions = (
        hr_questions +
        technical_questions
    )


current_question_index = 0

asked_questions = []

interview_results = []

question_start_time = time.time()

MAX_QUESTION_TIME = 120

# Default values
eye_score = 0
head_score = 0
posture_score = 0
confidence_score = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Face Mesh Processing
    face_results = face_mesh.process(rgb)

    # Pose Processing
    pose_results = pose.process(rgb)

    h, w, _ = frame.shape

    eye_status = "No Face"
    head_status = "No Face"
    posture_status = "No Person"

    # -------------------------------
    # Eye Contact + Head Pose
    # -------------------------------
    if face_results.multi_face_landmarks:

        face_landmarks = face_results.multi_face_landmarks[0]

        eye_score, eye_status = get_eye_contact(
            face_landmarks,
            w,
            h
        )

        head_score, head_status = get_head_pose(
            face_landmarks,
            w,
            h
        )

    # -------------------------------
    # Posture
    # -------------------------------
    if pose_results.pose_landmarks:

        posture_score, posture_status = get_posture(
            pose_results.pose_landmarks.landmark,
            w,
            h
        )

    # -------------------------------
    # Display Scores
    # -------------------------------

    cv2.putText(
        frame,
        f"Eye Contact: {eye_score}%",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Head Stability: {head_score}%",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Posture Score: {posture_score}%",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {confidence_score}%",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2
    )

    # -------------------------------
    # Status Messages
    # -------------------------------

    cv2.putText(
        frame,
        f"Eye: {eye_status}",
        (20, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Head: {head_status}",
        (20, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Posture: {posture_status}",
        (20, 280),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    elapsed_time = int(time.time() - start_time)

    current_question = questions[current_question_index]

    question_number = current_question_index + 1
    
    question_elapsed = int(
        time.time() - question_start_time
    )   

    cv2.putText(
        frame,
        f"Duration: {elapsed_time}s",
        (20, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Question {question_number}/{len(questions)}",
        (20, 345),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Question Time : {question_elapsed}s",
        (20, 370),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Question:",
        (20, 395),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        current_question,
        (20, 420),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press N : Next Qn",
        (20,445),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0,255,0),
        2
    )
    
    cv2.putText(
        frame,
        "Press Q : Finish Interview",
        (20, 475),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "AI Interview Coach",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Next Question
    if key == ord('n'):

        if current_question not in asked_questions:
            asked_questions.append(current_question)
        
        # Temporary placeholder answer
        interview_results.append({

            "question": current_question,

            "answer": "Sample Answer",

            "answer_score": 0,

            "keywords_found": [],

            "missing_keywords": [],

            "feedback": ""

        })

        if current_question_index < len(questions) - 1:

            current_question_index += 1

            question_start_time = time.time()

    # Quit Interview
    elif key == ord('q'):

        if current_question not in asked_questions:
            asked_questions.append(current_question)
        
        interview_results.append({

            "question": current_question,

            "answer": "Sample Answer",

            "answer_score": 0,

            "keywords_found": [],

            "missing_keywords": [],

            "feedback": ""

        })

        break

# Release Resources
cap.release()
cv2.destroyAllWindows()

audio_file = stop_recording(
    audio_stream
)

interview_duration = int(time.time() - start_time)

if audio_file:

    text = speech_to_text(
        audio_file
    )

    wpm = calculate_wpm(
        text,
        interview_duration
    )

    fillers = count_fillers(
        text
    )

else:

    text = ""

    wpm = 0

    fillers = 0

communication_score = calculate_communication_score(
    wpm,
    fillers
)

feedback = generate_feedback(
    eye_score,
    head_score,
    posture_score,
    communication_score
)

confidence_score = calculate_confidence(
    eye_score,
    head_score,
    posture_score,
    communication_score
)

print(
    "Communication Score:",
    communication_score
)

print("WPM:", wpm)
print("Filler Words:", fillers)

# Final Report
generate_report(
    eye_score,
    head_score,
    posture_score,
    confidence_score,
    interview_type,
    interview_duration,
    asked_questions,
    wpm,
    fillers,
    communication_score,
    feedback
)

generate_pdf_report(

    interview_type,

    interview_duration,

    eye_score,

    head_score,

    posture_score,

    communication_score,

    confidence_score,

    asked_questions,

    feedback

)

print("\nInterview Results:\n")

for result in interview_results:

    print(result)