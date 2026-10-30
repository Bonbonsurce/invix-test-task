"use client";

import Link from "next/link";
import { useCart } from "@/lib/cart";

export function SiteHeader() {
  const { count } = useCart();

  return (
    <header className="site-header">
      <Link href="/" className="logo">
        Invix Shop
      </Link>
      <nav>
        <Link href="/">Каталог</Link>
        <Link href="/cart">Корзина ({count})</Link>
      </nav>
    </header>
  );
}
