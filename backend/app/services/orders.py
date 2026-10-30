from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Order, OrderItem, Product
from app.schemas.order import OrderCreate


class OrderError(Exception):
    pass


async def create_order(session: AsyncSession, payload: OrderCreate) -> Order:
    if payload.idempotency_key:
        existing = await session.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.idempotency_key == payload.idempotency_key)
        )
        order = existing.scalar_one_or_none()
        if order:
            return order

    product_ids = {item.product_id for item in payload.items}
    result = await session.execute(select(Product).where(Product.id.in_(product_ids)))
    products = {p.id: p for p in result.scalars().all()}
    if len(products) != len(product_ids):
        raise OrderError("One or more products not found")

    order = Order(
        customer_name=payload.customer_name.strip(),
        customer_phone=payload.customer_phone.strip(),
        idempotency_key=payload.idempotency_key,
    )
    for item in payload.items:
        product = products[item.product_id]
        order.items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=Decimal(str(product.price)),
            )
        )

    session.add(order)
    await session.commit()
    await session.refresh(order, attribute_names=["items"])
    for oi in order.items:
        await session.refresh(oi, attribute_names=["product"])
    return order


def order_total(order: Order) -> float:
    return float(sum(Decimal(str(i.unit_price)) * i.quantity for i in order.items))
