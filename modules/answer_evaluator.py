import json

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def evaluate_answer(question, candidate_answer):

    with open(
        "assets/answer_key.json",
        "r",
        encoding="utf-8"
    ) as file:

        answer_key = json.load(file)

    if question not in answer_key:

        return 0, [], []

    ideal = answer_key[question]["ideal_answer"]

    keywords = answer_key[question]["keywords"]

    print("Keywords from JSON:", keywords)

    embeddings = model.encode(
        [
            ideal,
            candidate_answer
        ]
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = round(score * 100, 2)

    found = []

    missing = []

    candidate_lower = candidate_answer.lower()

    for word in keywords:

        if word.lower() in candidate_lower:

            found.append(word)

        else:

            missing.append(word)

    # Generate feedback based on score

    if score >= 85:

        feedback = (
            "Excellent answer. You covered most of the important concepts."
        )

    elif score >= 70:

        feedback = (
            "Good answer. Try including a few more technical details."
        )

    elif score >= 50:

        feedback = (
            "Average answer. Some important concepts are missing."
        )

    else:

        feedback = (
            "Needs improvement. Review the topic and include more key concepts."
        )
        
    print("Found:", found)
    print("Missing:", missing)

    return score, found, missing, feedback