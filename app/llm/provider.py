import os

from openai import OpenAIError

from app.llm.qwen import (
    analyze_intent as qwen_analyze_intent,
    chat as qwen_chat,
)


class LLMServiceError(Exception):
    pass


class UnsupportedProviderError(Exception):
    pass


def generate(message: str) -> dict:
    provider = os.getenv("LLM_PROVIDER", "qwen").lower()

    if provider != "qwen":
        raise UnsupportedProviderError(
            f"Unsupported LLM provider: {provider}"
        )

    try:
        answer = qwen_chat(message)
    except OpenAIError as exc:
        raise LLMServiceError("Qwen request failed") from exc

    return {
        "answer": answer,
        "provider": "qwen",
        "model": os.getenv("QWEN_MODEL", "qwen-plus"),
    }


def analyze(message: str) -> dict:
    provider = os.getenv("LLM_PROVIDER", "qwen").lower()

    if provider != "qwen":
        raise UnsupportedProviderError(
            f"Unsupported LLM provider: {provider}"
        )

    try:
        return qwen_analyze_intent(message)
    except OpenAIError as exc:
        raise LLMServiceError("Qwen request failed") from exc