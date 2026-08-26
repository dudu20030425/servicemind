import pytest
from mcp import Client

from mcp_server.server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_order_lookup_through_mcp():
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool(
            "order_lookup",
            {"order_id": "ORD10001"},
        )

    assert result.is_error is False
    assert result.structured_content["success"] is True
    assert result.structured_content["data"]["order_id"] == "ORD10001"


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("order_id", "expected_message"),
    [
        ("ORD-NOT-EXIST", "Order ORD-NOT-EXIST was not found."),
        ("   ", "Order ID is required."),
    ],
)
async def test_order_lookup_failure_through_mcp(
    order_id: str,
    expected_message: str,
):
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool(
            "order_lookup",
            {"order_id": order_id},
        )

    assert result.is_error is False
    assert result.structured_content["success"] is False
    assert result.structured_content["message"] == expected_message