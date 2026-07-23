from config import LLM_PROVIDER

from modules.llm.gemini import GeminiLLM
from modules.llm.ollama import OllamaLLM


def get_llm():

    if LLM_PROVIDER.lower() == "gemini":
        return GeminiLLM()

    elif LLM_PROVIDER.lower() == "ollama":
        return OllamaLLM()

    else:
        raise ValueError(
            f"Unsupported LLM provider: {LLM_PROVIDER}"
        )