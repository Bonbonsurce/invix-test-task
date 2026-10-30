import logging
from io import BytesIO

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.backend_client import BackendClient
from app.catalog_ui import catalog_keyboard, reply_catalog_invite
from app.config import settings
from app.filters import IsAdmin
from app.parsing import parse_product_caption

logger = logging.getLogger(__name__)

router = Router()
backend = BackendClient(settings.backend_url)


@router.message(CommandStart())
@router.message(Command("catalog"))
async def cmd_start(message: Message) -> None:
    await reply_catalog_invite(message)


@router.message(Command("create_product"), IsAdmin())
@router.message(F.text == "Создать товар", IsAdmin())
async def cmd_create_product(message: Message) -> None:
    await message.answer("Отправьте фото с подписью. Пример: Кофе | 200")


@router.message(F.photo, IsAdmin())
async def admin_photo_create(message: Message) -> None:
    user = message.from_user
    if not user:
        return

    try:
        name, price = parse_product_caption(message.caption)
    except ValueError as exc:
        await message.answer(str(exc))
        return

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    buffer = BytesIO()
    await message.bot.download(file, destination=buffer)

    try:
        product = await backend.create_product(
            name=name,
            image_bytes=buffer.getvalue(),
            content_type="image/jpeg",
            telegram_user_id=user.id,
            price=price,
        )
    except Exception:
        logger.exception("create_product failed")
        await message.answer("Не удалось создать товар.")
        return

    await message.answer(
        f"Товар «{product['name']}» добавлен.",
        reply_markup=catalog_keyboard(),
    )


@router.message()
async def fallback(message: Message) -> None:
    await reply_catalog_invite(message)
