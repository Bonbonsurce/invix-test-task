import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AddToCartButton } from "@/components/AddToCartButton";
import { fetchProduct } from "@/lib/api";

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const productId = Number(id);
  if (!Number.isFinite(productId)) notFound();

  let product;
  try {
    product = await fetchProduct(productId);
  } catch {
    notFound();
  }

  return (
    <div className="product-detail">
      <Image
        src={product.image_url}
        alt={product.name}
        width={600}
        height={600}
        className="product-image"
        unoptimized
      />
      <div>
        <h1>{product.name}</h1>
        <p className="price">{product.price.toFixed(2)} ₽</p>
        {product.description && <p>{product.description}</p>}
        <AddToCartButton product={product} />
        <p style={{ marginTop: "1rem" }}>
          <Link href="/">← Назад в каталог</Link>
        </p>
      </div>
    </div>
  );
}
