import Image from "next/image";
import Link from "next/link";
import type { Product } from "@/lib/api";

export function ProductCard({ product }: { product: Product }) {
  return (
    <article className="product-card">
      <Link href={`/products/${product.id}`}>
        <Image
          src={product.image_url}
          alt={product.name}
          width={400}
          height={400}
          className="product-image"
          unoptimized
        />
        <h2>{product.name}</h2>
        <p className="price">{product.price.toFixed(2)} ₽</p>
      </Link>
    </article>
  );
}
