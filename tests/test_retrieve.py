from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_retrieve():
    fake_results = [
        {
            "id": "PRODUCT003",
            "chunk_id": "PRODUCT003_chunk_0",
            "text": "Bluetooth earbud troubleshooting guide.",
            "category": "product",
            "source": "product_guide.json",
            "score": 0.9348,
        }
    ]

    with patch(
        "app.api.routes.retrieve",
        return_value=fake_results,
    ):
        response = client.post(
            "/retrieve",
            json={
                "query": "How do I fix my earbuds?",
                "top_k": 3,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "query": "How do I fix my earbuds?",
        "results": fake_results,
    }


def test_retrieve_invalid_top_k():
    response = client.post(
        "/retrieve",
        json={
            "query": "Test query",
            "top_k": 0,
        },
    )

    assert response.status_code == 422