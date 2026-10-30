from aiogram.types import InlineKeyboardMarkup, Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def catalog_keyboard() -> InlineKeyboardMarkup | None:
    url = settings.webapp_url.rstrip("/")
    if not url.lower().startswith("https://"):
        return None
    builder = InlineKeyboardBuilder()
    builder.button(text="Открыть каталог", web_app=WebAppInfo(url=url))
    return builder.as_markup()


def catalog_message_text() -> str:
    url = settings.webapp_url.rstrip("/")
    if url.lower().startswith("https://"):
        return "У меня есть товар"
    return f"У меня есть товар\n\n{url}"


async def reply_catalog_invite(message: Message) -> None:
    await message.answer(catalog_message_text(), reply_markup=catalog_keyboard())
