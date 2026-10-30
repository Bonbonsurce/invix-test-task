from decimal import Decimal

from app.services.orders import order_total
from app.models import Order, OrderItem, Product


def test_order_total_sums_line_items() -> None:
    order = Order(customer_name="A", customer_phone="+1")
    p = Product(name="X", price=Decimal("10.00"), image_key="k")
    p.id = 1
    order.items = [
        OrderItem(product_id=1, quantity=2, unit_price=Decimal("10.00"), product=p),
        OrderItem(product_id=1, quantity=1, unit_price=Decimal("5.50"), product=p),
    ]
    assert order_total(order) == 25.5
