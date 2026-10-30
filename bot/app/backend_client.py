import httpx


class BackendClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    async def create_product(
        self,
        *,
        name: str,
        image_bytes: bytes,
        content_type: str,
        telegram_user_id: int,
        price: float = 0,
        description: str | None = None,
    ) -> dict:
        files = {"image": ("product.jpg", image_bytes, content_type)}
        data: dict[str, str] = {"name": name, "price": str(price)}
        if description:
            data["description"] = description
        headers = {"X-Telegram-User-Id": str(telegram_user_id)}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self._base_url}/api/products",
                data=data,
                files=files,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
