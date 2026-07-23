import json

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

    semantic_score = round(
        score * 75,
        2
    )

    tech_score, tech_terms = technical_term_score(
        candidate_answer
    )

    length = length_score(
        candidate_answer
    )

    final_score = min(
        round(semantic_score + tech_score + length),
        100
    )

    found = []

    missing = []

    candidate_lower = candidate_answer.lower()

    for word in keywords:

        if word.lower() in candidate_lower:

            found.append(word)

        else:

            missing.append(word)

    # Generate dynamic feedback

    feedback = []

    # Positive feedback
    if found:
        feedback.append(
            f"Good job mentioning: {', '.join(found[:3])}."
        )
 
    #Missing keywords
    if len(missing) > 0:
        feedback.append(
            f"Include concepts such as: {', '.join(missing[:3])}."
        )

    if tech_score < 6:
        feedback.append(
            "Mention more relevant technical terms."
        )

    if length < 6:
        feedback.append(
            "Expand your answer with more details."
        )

    if not feedback:
        feedback.append(
            "Excellent answer. Well structured and relevant."
        )

    feedback = " ".join(feedback)

    
    return (
        final_score,
        found,
        missing,
        tech_terms,
        feedback
    )