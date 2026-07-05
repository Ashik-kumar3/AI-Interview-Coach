import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Technical Vocabulary
# -----------------------------

TECHNICAL_TERMS = {

    "python",

    "variable",

    "loop",

    "function",

    "class",

    "object",

    "inheritance",

    "encapsulation",

    "polymorphism",

    "list",

    "tuple",

    "dictionary",

    "numpy",

    "pandas",

    "tensorflow",

    "keras",

    "pytorch",

    "cnn",

    "rnn",

    "ann",

    "machine learning",

    "deep learning",

    "dataset",

    "training",

    "testing",

    "model",

    "accuracy",

    "precision",

    "recall",

    "f1",

    "overfitting",

    "underfitting",

    "cross validation",

    "transfer learning",

    "mediapipe"

}

def technical_term_score(answer):

    answer = answer.lower()

    score = 0

    found = []

    for term in TECHNICAL_TERMS:

        if term in answer:

            found.append(term)

    score = min(

        len(found) * 3,

        15

    )

    return score, found

def length_score(answer):

    words = len(answer.split())

    if words >= 80:

        return 10

    elif words >= 50:

        return 8

    elif words >= 30:

        return 6

    elif words >= 15:

        return 4

    else:

        return 2

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

        return (
            0,
            [],
            [],
            "No answer key available for this question."
        )

    ideal = answer_key[question]["ideal_answer"]

    keywords = answer_key[question]["keywords"]

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

    return score, found, missing, feedback