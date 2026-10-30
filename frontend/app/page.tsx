import { fetchProducts } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

export default async function CatalogPage() {
  let products: Awaited<ReturnType<typeof fetchProducts>> = [];
  let error: string | null = null;

  try {
    products = await fetchProducts();
  } catch (e) {
    error = e instanceof Error ? e.message : "Не удалось загрузить каталог";
  }

  return (
    <>
      <h1>Каталог</h1>
      {error && <p className="alert">{error}</p>}
      {!error && products.length === 0 && (
        <p className="muted">Товаров пока нет</p>
      )}
      <div className="grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </>
  );
}
