import pytest

from app.parsing import parse_product_caption


def test_parse_name_only() -> None:
    assert parse_product_caption("  Кофе  ") == ("Кофе", 0.0)


def test_parse_name_and_price() -> None:
    assert parse_product_caption("Кофе | 199.99") == ("Кофе", 199.99)


def test_parse_empty_raises() -> None:
    with pytest.raises(ValueError):
        parse_product_caption("   ")


def test_parse_bad_price_raises() -> None:
    with pytest.raises(ValueError):
        parse_product_caption("Кофе | abc")
