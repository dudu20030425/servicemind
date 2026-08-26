from typing import Any

from app.llm.provider import analyze, generate
from app.rag.service import answer_with_rag
from app.tools.order_lookup import order_lookup


def run_agent(message: str) -> dict[str, Any]:
    intent_result = analyze(message)
    intent = intent_result["intent"]

    if intent == "order_query":
        order_id = intent_result.get("order_id")

        if not order_id:
            return {
                "answer": "请提供需要查询的订单号，例如 ORD10001。",
                "intent": intent,
                "route": "tool",
                "tool_name": "order_lookup",
                "data": None,
                "provider": None,
                "model": None,
                "sources": [],
            }

        tool_result = order_lookup(order_id)

        if not tool_result["success"]:
            return {
                "answer": f"未查询到订单 {order_id}，请检查订单号是否正确。",
                "intent": intent,
                "route": "tool",
                "tool_name": "order_lookup",
                "data": None,
                "provider": None,
                "model": None,
                "sources": [],
            }

        order = tool_result["data"]
        status_map = {
            "shipped": "已发货",
            "delivered": "已送达",
        }
        status = status_map.get(order["status"], order["status"])

        return {
            "answer": (
                f"订单 {order['order_id']} 当前状态为{status}，"
                f"物流单号为 {order['tracking_number']}。"
            ),
            "intent": intent,
            "route": "tool",
            "tool_name": "order_lookup",
            "data": order,
            "provider": None,
            "model": None,
            "sources": [],
        }

    if intent in {"refund_query", "product_query"}:
        result = answer_with_rag(message)

        return {
            "answer": result["answer"],
            "intent": intent,
            "route": "rag",
            "tool_name": None,
            "data": None,
            "provider": result["provider"],
            "model": result["model"],
            "sources": result["sources"],
        }

    result = generate(message)

    return {
        "answer": result["answer"],
        "intent": intent,
        "route": "chat",
        "tool_name": None,
        "data": None,
        "provider": result["provider"],
        "model": result["model"],
        "sources": [],
    }