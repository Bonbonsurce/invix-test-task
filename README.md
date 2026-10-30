# Invix Shop

Тестовое задание: каталог на Next.js, API на FastAPI, Telegram-бот на aiogram, PostgreSQL, MinIO (`pgsty/minio` — форк, образ `minio/minio` с Docker Hub снят).

## Запуск

```bash
cp .env.example .env
# BOT_TOKEN, ADMIN_TELEGRAM_IDS
docker compose up --build
```

- Каталог: http://localhost:3000  
- API: http://localhost:8000/docs  

## Бот

- `/start` — «У меня есть товар», кнопка Mini App (если `WEBAPP_URL` с `https://`)
- Админ: `/create_product` или «Создать товар», затем **фото с подписью** (`Название` или `Название | 199.99`)

## Mini App через один туннель (tuna и т.п.)

```bash
tuna http 3000
```

В `.env`:

```env
WEBAPP_URL=https://туннель
MINIO_PUBLIC_URL=https://туннель/s3
```

```bash
docker compose up --build -d frontend backend bot
```

В BotFather → Menu Button / Web App — тот же URL, что `WEBAPP_URL`.

## API

- `GET /api/products`, `GET /api/products/{id}`
- `POST /api/products` — multipart, заголовок `X-Telegram-User-Id` (админ)
- `POST /api/orders`

## Тесты

```bash
cd backend && pip install -r requirements.txt && pytest
cd bot && pip install -r requirements.txt && pytest
```
