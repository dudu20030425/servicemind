from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.llm.provider import (
    LLMServiceError,
    UnsupportedProviderError,
)

client = TestClient(app)


def test_chat():
    fake_result = {
        "answer": "mock answer",
        "provider": "qwen",
        "model": "qwen3.7-plus",
    }

    with patch(
        "app.api.routes.generate",
        return_value=fake_result,
    ):
        response = client.post(
            "/chat",
            json={"message": "你好"},
        )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "mock answer",
        "provider": "qwen",
        "model": "qwen3.7-plus",
    }
    
def test_chat_unsupported_provider():
    with patch(
        "app.api.routes.generate",
        side_effect=UnsupportedProviderError(
            "Unsupported LLM provider: abc"
        ),
    ):
        response = client.post(
            "/chat",
            json={"message": "你好"},
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Unsupported LLM provider: abc"
    }
    
def test_chat_llm_service_error():
    with patch(
        "app.api.routes.generate",
        side_effect=LLMServiceError(
            "Qwen request failed"
        ),
    ):
        response = client.post(
            "/chat",
            json={"message": "你好"},
        )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "LLM service unavailable"
    }