from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_retrieve():
    fake_results = [
        {
            "id": "POLICY006",
            "chunk_id": "POLICY006_chunk_0",
            "text": "超过七天后仍可申请质量问题售后。",
            "category": "return_policy",
            "source": "return_policy.json",
            "score": 0.7332,
        }
    ]

    with patch(
        "app.api.routes.retrieve",
        return_value=fake_results,
    ):
        response = client.post(
            "/retrieve",
            json={
                "query": "超过七天还能申请售后吗？",
                "top_k": 3,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "query": "超过七天还能申请售后吗？",
        "results": fake_results,
    }


def test_retrieve_invalid_top_k():
    response = client.post(
        "/retrieve",
        json={
            "query": "如何退货？",
            "top_k": 0,
        },
    )

    assert response.status_code == 422