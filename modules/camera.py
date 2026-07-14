import cv2
import mediapipe as mp

from streamlit_webrtc import VideoTransformerBase
from modules.analysis import analysis

mp_face_mesh = mp.solutions.face_mesh


face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

class VideoProcessor(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb)

        pose_results = pose.process(rgb)

        h, w, _ = img.shape

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:

                # Nose Tip

                nose = face_landmarks.landmark[1]

                nose_x = nose.x
                nose_y = nose.y

                center = 0.5

                distance = abs(nose_x - center)

                score = max(
                    0,
                    100 - int(distance * 400)
                )

                analysis.eye_contact = score

                if analysis.previous_nose_x is None:

                    analysis.previous_nose_x = nose_x
                    analysis.previous_nose_y = nose_y

                movement = (
                    abs(nose_x - analysis.previous_nose_x)
                    +
                    abs(nose_y - analysis.previous_nose_y)
                )

                stability = max(
                    0,
                    100 - int(movement * 1500)
                )

                analysis.head_stability = stability

                analysis.previous_nose_x = nose_x
                analysis.previous_nose_y = nose_y
                
                 # Draw Face Mesh

                for landmark in face_landmarks.landmark:

                    x = int(landmark.x * w)

                    y = int(landmark.y * h)

                    cv2.circle(
                        img,
                        (x, y),
                        1,
                        (0, 255, 0),
                        -1
                    )
        else:

            analysis.eye_contact = 0
            analysis.head_stability = 0
              
        if pose_results.pose_landmarks:

            landmarks = pose_results.pose_landmarks.landmark

            left_shoulder = landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER
            ]

            right_shoulder = landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER
            ]

            shoulder_diff = abs(
                left_shoulder.y -
                right_shoulder.y
            )


            # Body tilt

            shoulder_center_x = (
                left_shoulder.x +
                right_shoulder.x
            ) / 2

            nose = landmarks[
                mp_pose.PoseLandmark.NOSE
            ]

            body_tilt = abs(
                nose.x -
                shoulder_center_x
            )

            total_error = (
                shoulder_diff * 1000
                +
                body_tilt * 300
            )


            posture_score = max(
                0,
                100 - int(total_error)
            )

            analysis.posture = posture_score

                        
            cv2.circle(
                img,
                (
                    int(left_shoulder.x * w),
                    int(left_shoulder.y * h)
                ),
                6,
                (255, 0, 0),
                -1
            )

            cv2.circle(
                img,
                (
                    int(right_shoulder.x * w),
                    int(right_shoulder.y * h)
                ),
                6,
                (255, 0, 0),
                -1
            )
        else:
                    
            analysis.posture = 0
            analysis.confidence = 0

        analysis.confidence = int(
            (
                analysis.eye_contact * 0.4
                +
                analysis.head_stability * 0.3
                +
                analysis.posture * 0.3
            )
        )

        return img