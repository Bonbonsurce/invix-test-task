from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.services.storage import storage_service


async def list_products(session: AsyncSession) -> list[Product]:
    result = await session.execute(select(Product).order_by(Product.created_at.desc()))
    return list(result.scalars().all())


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(
    session: AsyncSession,
    *,
    name: str,
    image_data: bytes,
    content_type: str,
    description: str | None = None,
    price: float = 0,
) -> Product:
    key = storage_service.upload_image(image_data, content_type)
    product = Product(
        name=name.strip(),
        description=description,
        price=price,
        image_key=key,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


def product_image_url(product: Product) -> str:
    return storage_service.public_url(product.image_key)
