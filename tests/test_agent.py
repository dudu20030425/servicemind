from unittest.mock import patch

from fastapi.testclient import TestClient

from app.agents.customer_service_agent import run_agent
from app.main import app


client = TestClient(app)


def test_agent_order_route():
    intent = {
        "intent": "order_query",
        "order_id": "ORD10001",
        "need_tool": True,
    }

    with patch(
        "app.agents.customer_service_agent.analyze",
        return_value=intent,
    ):
        result = run_agent("查询订单 ORD10001")

    assert result["intent"] == "order_query"
    assert result["route"] == "tool"
    assert result["tool_name"] == "order_lookup"
    assert result["data"]["order_id"] == "ORD10001"


def test_agent_missing_order_id():
    intent = {
        "intent": "order_query",
        "order_id": None,
        "need_tool": True,
    }

    with patch(
        "app.agents.customer_service_agent.analyze",
        return_value=intent,
    ):
        result = run_agent("帮我查询订单")

    assert result["route"] == "tool"
    assert result["data"] is None
    assert "订单号" in result["answer"]


def test_agent_rag_route():
    intent = {
        "intent": "refund_query",
        "order_id": None,
        "need_tool": False,
    }
    rag_result = {
        "answer": "支持符合条件的七天无理由退货。",
        "provider": "qwen",
        "model": "qwen3.7-plus",
        "sources": [],
    }

    with (
        patch(
            "app.agents.customer_service_agent.analyze",
            return_value=intent,
        ),
        patch(
            "app.agents.customer_service_agent.answer_with_rag",
            return_value=rag_result,
        ),
    ):
        result = run_agent("支持七天无理由退货吗？")

    assert result["intent"] == "refund_query"
    assert result["route"] == "rag"
    assert result["answer"] == rag_result["answer"]


def test_agent_chat_route():
    intent = {
        "intent": "general_chat",
        "order_id": None,
        "need_tool": False,
    }
    chat_result = {
        "answer": "你好，我是 ServiceMind。",
        "provider": "qwen",
        "model": "qwen3.7-plus",
    }

    with (
        patch(
            "app.agents.customer_service_agent.analyze",
            return_value=intent,
        ),
        patch(
            "app.agents.customer_service_agent.generate",
            return_value=chat_result,
        ),
    ):
        result = run_agent("你好")

    assert result["intent"] == "general_chat"
    assert result["route"] == "chat"
    assert result["answer"] == chat_result["answer"]


def test_agent_endpoint():
    fake_result = {
        "answer": "订单 ORD10001 当前状态为已发货。",
        "intent": "order_query",
        "route": "tool",
        "tool_name": "order_lookup",
        "data": {"order_id": "ORD10001"},
        "provider": None,
        "model": None,
        "sources": [],
    }

    with patch(
        "app.api.routes.run_agent",
        return_value=fake_result,
    ):
        response = client.post(
            "/agent",
            json={"message": "查询订单 ORD10001"},
        )

    assert response.status_code == 200
    assert response.json() == fake_result