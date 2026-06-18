from modules.eye_contact import get_eye_contact
from modules.head_pose import get_head_pose
from modules.posture import get_posture
from modules.confidence import calculate_confidence
from modules.report import generate_report

print("All modules imported successfully!")

from modules.confidence import calculate_confidence

score = calculate_confidence(
    eye_score=90,
    head_score=80,
    posture_score=85
)

print(score)

from modules.report import generate_report

generate_report(
    eye_score=88,
    head_score=84,
    posture_score=91,
    confidence_score=88
)