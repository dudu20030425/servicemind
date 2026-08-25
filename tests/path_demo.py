import json
from pathlib import Path
from typing import Any


def load_orders(file_path: Path) -> list[dict[str, Any]]:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print("Orders file not found.")
        return []

    except json.JSONDecodeError:
        print("Orders file is not valid JSON.")
        return []


root = Path(__file__).resolve().parent.parent
orders_file = root / "data" / "business_db" / "orders.json"

orders = load_orders(orders_file)

print("Number of orders:", len(orders))

if orders:
    print("First order:", orders[0])