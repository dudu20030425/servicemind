from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_intent():
    fake_result = {
        "intent": "order_query",
        "order_id": "ORD10001",
        "need_tool": True,
    }

    with patch(
        "app.api.routes.analyze",
        return_value=fake_result,
    ):
        response = client.post(
            "/intent",
            json={
                "message": "我的 ORD10001 到哪里了？"
            },
        )

    assert response.status_code == 200

    assert response.json() == {
        "intent": "order_query",
        "order_id": "ORD10001",
        "need_tool": True,
    }