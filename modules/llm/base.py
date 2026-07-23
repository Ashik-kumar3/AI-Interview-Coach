from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def evaluate(
        self,
        question: str,
        answer: str,
        expected_keywords: list
    ) -> dict:
        """
        Evaluate an interview answer and return a standardized dictionary.
        """
        pass