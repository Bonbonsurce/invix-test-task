from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models import Product
from app.schemas.product import ProductRead
from app.services import products as product_service

router = APIRouter(prefix="/products", tags=["products"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


def _product_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        name=product.name,
        description=product.description,
        price=float(product.price),
        image_url=product_service.product_image_url(product),
        created_at=product.created_at,
    )


@router.get("", response_model=list[ProductRead])
async def list_products(session: AsyncSession = Depends(get_db)) -> list[ProductRead]:
    items = await product_service.list_products(session)
    return [_product_read(p) for p in items]


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: AsyncSession = Depends(get_db)) -> ProductRead:
    product = await product_service.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return _product_read(product)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    _: int = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
    name: str = Form(...),
    image: UploadFile = File(...),
    description: str | None = Form(default=None),
    price: float = Form(default=0),
) -> ProductRead:
    if not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")
    content_type = image.content_type or "application/octet-stream"
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")
    data = await image.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty image")
    product = await product_service.create_product(
        session,
        name=name,
        image_data=data,
        content_type=content_type,
        description=description,
        price=price,
    )
    return _product_read(product)
