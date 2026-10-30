from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_admin(x_telegram_user_id: str | None = Header(default=None)) -> int:
    if not x_telegram_user_id or not x_telegram_user_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-Telegram-User-Id header",
        )
    user_id = int(x_telegram_user_id)
    if user_id not in settings.admin_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user_id
