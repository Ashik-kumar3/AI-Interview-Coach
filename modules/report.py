from datetime import datetime
import os

def generate_report(
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
        feedback):
    

    if confidence_score >= 85:
        rating = "Excellent"

    elif confidence_score >= 70:
        rating = "Good"

    elif confidence_score >= 50:
        rating = "Average"

    else:
        rating = "Needs Improvement"

    questions_text = "\n".join(
        f"- {q}" for q in asked_questions
    )

    feedback_test = "\n".join(
        f"- {item}" for item in feedback
    )

    report = f"""
===================================
INTERVIEW REPORT
===================================

Interview Type : {interview_type}
Interview Duration : {interview_duration} seconds
Eye Contact Score : {eye_score}%
Head Stability Score : {head_score}%
Posture Score : {posture_score}%
Confidence Score : {confidence_score}%
Speech Analysis

Speaking Speed : {wpm} WPM
Filler Words : {fillers}
Communication Score : {communication_score}%

Interview Questions Asked:

{questions_text}

Personalized Feedback:

{feedback_test}

Overall Rating : {rating}

===================================
"""
    # Print on terminal
    print(report)

    # Create reports folder if missing
    os.makedirs("reports", exist_ok=True)

    # Generate filename using current time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/report_{timestamp}.txt"

    # Save report
    with open(filename, "w") as file:
        file.write(report)

    print(f"Report saved: {filename}")

    return report, filename