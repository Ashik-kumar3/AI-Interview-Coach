def evaluate_hr_answer(question, answer):

    answer_lower = answer.lower()

    score = 0

    feedback = []

    if len(answer.split()) >= 40:
        score += 20
    else:
        feedback.append(
            "Answer is too short."
        )

    if any(
        word in answer_lower
        for word in [
            "experience",
            "project",
            "internship",
            "skill",
            "learned"
        ]
    ):
        score += 20
    else:
        feedback.append(
            "Mention your experience or projects."
        )

    if any(
        word in answer_lower
        for word in [
            "team",
            "communication",
            "problem",
            "responsibility"
        ]
    ):
        score += 20
    else:
        feedback.append(
            "Include soft skills."
        )

    if any(
        word in answer_lower
        for word in [
            "company",
            "role",
            "career",
            "growth"
        ]
    ):
        score += 20
    else:
        feedback.append(
            "Explain your motivation clearly."
        )

    score += 20

    score = min(score, 100)

    if not feedback:
        final_feedback = (
            "Excellent HR answer."
        )
    else:
        final_feedback = " ".join(feedback)

    return (
        score,
        final_feedback
    )