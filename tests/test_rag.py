from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rag_answer():
    fake_result = {
        "answer": "Reset the Bluetooth connection.",
        "provider": "qwen",
        "model": "qwen3.7-plus",
        "sources": [
            {
                "id": "PRODUCT003",
                "text": "Bluetooth earbud troubleshooting guide.",
                "source": "product_guide.json",
                "score": 0.9348,
            }
        ],
    }

    with patch(
        "app.api.routes.answer_with_rag",
        return_value=fake_result,
    ):
        response = client.post(
            "/rag",
            json={
                "query": "How do I fix my earbuds?",
                "top_k": 3,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "query": "How do I fix my earbuds?",
        **fake_result,
    }


def test_rag_no_relevant_knowledge():
    fake_result = {
        "answer": "No relevant information was found.",
        "provider": None,
        "model": None,
        "sources": [],
    }

    with patch(
        "app.api.routes.answer_with_rag",
        return_value=fake_result,
    ):
        response = client.post(
            "/rag",
            json={
                "query": "Unknown question",
                "top_k": 3,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "query": "Unknown question",
        **fake_result,
    }