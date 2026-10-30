def parse_product_caption(caption: str | None) -> tuple[str, float]:
    if not caption or not caption.strip():
        raise ValueError("Нужна подпись к фото с названием товара")

    text = caption.strip()
    if "|" not in text:
        return text, 0.0

    name_part, price_part = text.split("|", 1)
    name = name_part.strip()
    if not name:
        raise ValueError("Укажите название товара")

    price_str = price_part.strip().replace(",", ".")
    try:
        price = float(price_str)
    except ValueError as exc:
        raise ValueError("Неверная цена") from exc
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    return name, price
