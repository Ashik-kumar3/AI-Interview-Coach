def evaluate_hr_answer(question, answer):

    answer_lower = answer.lower()

    if not answer.strip():
        return (
            0,
            "No answer detected. Please provide a response to receive feedback."
        )

    score = 0

    feedback = []
    strengths = []

    if len(answer.split()) >= 40:
        score += 20
        strengths.append(
            "Provided a detailed response"
        )
    else:
        feedback.append(
            "Expand your answer with more details"
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
        strengths.append(
            "Mentioned relevant experience or projects."
        )
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
        strengths.append(
            "Highlighted important soft skills."
        )
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
        strengths.append(
            "Clearly explained career motivation."
        )
    else:
        feedback.append(
            "Explain your motivation clearly."
        )

    score += 20

    score = min(score, 100)

    final_feedback = ""

    if strengths:
        final_feedback += (
            "Good job: "
            + ", ".join(strengths)
            + ". "
        )

    if feedback:
        final_feedback += (
            "Suggestions: "
            + " ".join(feedback)
        )

    if not strengths and not feedback:
        final_feedback = (
            "Excellent HR answer."
        )

    return (
        score,
        final_feedback
    )