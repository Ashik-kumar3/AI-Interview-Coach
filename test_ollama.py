from modules.llm.ollama import OllamaLLM

llm = OllamaLLM()

result = llm.evaluate(
    question="Tell me about yourself.",
    answer="I recently graduated in Electronics and Communication Engineering and completed AI/ML internships where I worked on deep learning and computer vision projects.",
    expected_keywords=[
        "education",
        "experience",
        "skills",
        "career goals"
    ]
)

print(result)