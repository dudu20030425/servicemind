import json
from pathlib import Path
from typing import Any


ORDERS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "business_db"
    / "orders.json"
)


def order_lookup(order_id: str) -> dict[str, Any]:
    normalized_id = order_id.strip().upper()

    if not normalized_id:
        return {
            "success": False,
            "tool": "order_lookup",
            "message": "Order ID is required.",
        }

    with ORDERS_FILE.open(encoding="utf-8") as file:
        orders = json.load(file)

    for order in orders:
        if order["order_id"].upper() == normalized_id:
            return {
                "success": True,
                "tool": "order_lookup",
                "data": order,
            }

    return {
        "success": False,
        "tool": "order_lookup",
        "message": f"Order {normalized_id} was not found.",
    }