from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderItemRead, OrderRead
from app.services import orders as order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate, session: AsyncSession = Depends(get_db)
) -> OrderRead:
    try:
        order = await order_service.create_order(session, payload)
    except order_service.OrderError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return OrderRead(
        id=order.id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        items=[
            OrderItemRead(
                product_id=i.product_id,
                product_name=i.product.name,
                quantity=i.quantity,
                unit_price=float(i.unit_price),
            )
            for i in order.items
        ],
        total=order_service.order_total(order),
        created_at=order.created_at,
    )
