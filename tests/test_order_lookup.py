from app.tools.order_lookup import order_lookup


def test_order_lookup_found():
    result = order_lookup("ORD10001")

    assert result["success"] is True
    assert result["tool"] == "order_lookup"
    assert result["data"]["order_id"] == "ORD10001"
    assert result["data"]["status"] == "shipped"


def test_order_lookup_normalizes_id():
    result = order_lookup("ord10002")

    assert result["success"] is True
    assert result["data"]["order_id"] == "ORD10002"


def test_order_lookup_not_found():
    result = order_lookup("ORD99999")

    assert result["success"] is False
    assert result["tool"] == "order_lookup"
    assert "ORD99999" in result["message"]


def test_order_lookup_empty_id():
    result = order_lookup("   ")

    assert result["success"] is False
    assert result["message"] == "Order ID is required."