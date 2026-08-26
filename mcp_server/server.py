from typing import Any

from mcp.server import MCPServer

from app.tools.order_lookup import order_lookup as lookup_order_data


mcp = MCPServer("ServiceMind")


@mcp.tool()
def order_lookup(order_id: str) -> dict[str, Any]:
    """Look up customer order details by order ID."""
    return lookup_order_data(order_id)