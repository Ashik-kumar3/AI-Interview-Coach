from modules.answer_evaluator import evaluate_answer

score, found, missing, feedback = evaluate_answer(
    "What is Python?",
    "Python is a high level programming language used in AI and data science."
)

print("Answer Score:", score)
print("Keywords Found:", found)
print("Missing Keywords:", missing)
print("Feedback:", feedback)
