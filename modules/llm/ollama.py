import json
import ollama

from config import OLLAMA_MODEL
from modules.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def evaluate(
        self,
        question: str,
        answer: str,
        expected_keywords: list
    ) -> dict:

        prompt = f"""
You are an expert AI recruiter.

Evaluate the candidate's interview answer.

Question:
{question}

Candidate Answer:
{answer}

Expected Keywords:
{", ".join(expected_keywords)}

Return ONLY valid JSON in this format:

{{
    "score": 0,
    "strengths": [],
    "missing_concepts": [],
    "improvements": [],
    "communication_rating": "",
    "hiring_recommendation": "",
    "recruiter_feedback": ""
}}

Do not include markdown.
Do not include explanations.
Only output JSON.
"""

        try:

            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response["message"]["content"].strip()

            if content.startswith("```"):
                content = content.replace("```json", "")
                content = content.replace("```", "").strip()

            return json.loads(content)

        except Exception as e:

            print("=" * 80)
            print("OLLAMA ERROR")
            print(e)
            print("=" * 80)

            return {
                "score": None,
                "strengths": [],
                "missing_concepts": [],
                "improvements": [
                    "Local LLM evaluation failed."
                ],
                "communication_rating": "Unavailable",
                "hiring_recommendation": "Unavailable",
                "recruiter_feedback": str(e)
            }