"use client";

import Link from "next/link";
import { useState } from "react";
import { createOrder } from "@/lib/api";
import { useCart } from "@/lib/cart";

export default function CartPage() {
  const { lines, setQuantity, removeItem, clear, total } = useCart();
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [orderId, setOrderId] = useState<string | null>(null);

  async function submitOrder(e: React.FormEvent) {
    e.preventDefault();
    if (lines.length === 0) return;
    setLoading(true);
    setError(null);
    try {
      const idempotencyKey =
        typeof crypto !== "undefined" && crypto.randomUUID
          ? crypto.randomUUID()
          : `${Date.now()}`;
      const order = await createOrder({
        customer_name: name.trim(),
        customer_phone: phone.trim(),
        items: lines.map((l) => ({ product_id: l.productId, quantity: l.quantity })),
        idempotency_key: idempotencyKey,
      });
      clear();
      setOrderId(order.id);
      setName("");
      setPhone("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка оформления заказа");
    } finally {
      setLoading(false);
    }
  }

  if (orderId) {
    return (
      <>
        <h1>Заказ оформлен</h1>
        <p className="alert">Номер заказа: {orderId}</p>
        <Link href="/" className="button">
          В каталог
        </Link>
      </>
    );
  }

  return (
    <>
      <h1>Корзина</h1>
      {lines.length === 0 ? (
        <p className="muted">
          Корзина пуста. <Link href="/">Перейти в каталог</Link>
        </p>
      ) : (
        <>
          <table className="cart-table">
            <thead>
              <tr>
                <th>Товар</th>
                <th>Цена</th>
                <th>Кол-во</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {lines.map((line) => (
                <tr key={line.productId}>
                  <td>{line.name}</td>
                  <td>{line.price.toFixed(2)} ₽</td>
                  <td>
                    <input
                      type="number"
                      min={1}
                      max={99}
                      value={line.quantity}
                      onChange={(e) => setQuantity(line.productId, Number(e.target.value))}
                      style={{ width: "4rem" }}
                    />
                  </td>
                  <td>
                    <button
                      type="button"
                      className="button secondary"
                      onClick={() => removeItem(line.productId)}
                    >
                      Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p>
            <strong>Итого: {total.toFixed(2)} ₽</strong>
          </p>
          {error && <p className="alert">{error}</p>}
          <form className="form" onSubmit={submitOrder}>
            <label>
              Имя
              <input value={name} onChange={(e) => setName(e.target.value)} required />
            </label>
            <label>
              Телефон
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                minLength={3}
              />
            </label>
            <button type="submit" className="button" disabled={loading}>
              {loading ? "Отправка…" : "Оформить заказ"}
            </button>
          </form>
        </>
      )}
    </>
  );
}
