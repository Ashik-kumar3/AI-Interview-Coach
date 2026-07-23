import os
import json

import google.generativeai as genai
from dotenv import load_dotenv

from config import GEMINI_MODEL
from modules.llm.base import BaseLLM

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)

class GeminiLLM(BaseLLM):
    
    def evaluate(
    self,
    question: str,
    answer: str,
    expected_keywords: list
) -> dict:
        """
        Evaluate an interview answer using Gemini.
        """
        prompt = f"""
        You are an experienced technical interviewer and recruiter.

        Evaluate the candidate's interview answer objectively.

        Interview Question:
        {question}

        Candidate Answer:
        {answer}

        Expected Keywords:
        {", ".join(expected_keywords)}

        Evaluate the answer based on:

        1. Technical correctness
        2. Completeness
        3. Relevant technical concepts
        4. Communication clarity
        5. Practical understanding

        Do not score based only on the presence of keywords. Evaluate the overall quality, correctness, explanation, and completeness of the answer. Keywords are only a reference.
        Return ONLY valid JSON.

        The JSON format MUST be:

        {{
            "score": integer (0-100),
            "strengths": [
                "...",
                "..."
            ],
            "missing_concepts": [
                "...",
                "..."
            ],
            "improvements": [
                "...",
                "..."
            ],
            "recruiter_feedback": "...",
            "communication_rating": "...",
            "hiring_recommendation": "..."
        }}

        Scoring Guidelines:

        90-100 : Excellent interview answer
        75-89  : Good answer with minor improvements
        60-74  : Average answer
        40-59  : Weak answer
        0-39   : Poor answer

        The score MUST be between 0 and 100.

        Do not wrap the JSON inside ```json ... ``` code fences.
        Do not return markdown.
        Do not return explanations.
        Return JSON only.
        """
        try:

            response = model.generate_content(prompt)

            response_text = response.text.strip()

            # Remove markdown code fences if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "", 1)

            if response_text.startswith("```"):
                response_text = response_text.replace("```", "", 1)

            if response_text.endswith("```"):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            result = json.loads(response_text)

            return result

        except Exception:

            return {
                "score": None,
                "strengths": [],
                "missing_concepts": [],
                "improvements": [
                    "LLM evaluation unavailable."
                ],
                "communication_rating": "Unavailable",
                "hiring_recommendation": "Unavailable",
                "recruiter_feedback":
                "Gemini evaluation was unavailable because the API usage limit was reached. Please try again later."

            }
    
if __name__ == "__main__":

    llm = GeminiLLM()

    result = llm.evaluate(
        question="What is Python?",
        answer="Python is a high-level programming language used for web development, AI, automation and data science.",
        expected_keywords=[
            "high level",
            "interpreted",
            "object oriented",
            "libraries"
        ]
    )

    print(json.dumps(result, indent=4))