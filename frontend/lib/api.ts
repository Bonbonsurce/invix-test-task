function getApiUrl(): string {
  if (typeof window === "undefined") {
    return (
      process.env.API_URL_INTERNAL ??
      process.env.NEXT_PUBLIC_API_URL ??
      "http://localhost:8000"
    );
  }
  return "";
}

export type Product = {
  id: number;
  name: string;
  description: string | null;
  price: number;
  image_url: string;
  created_at: string;
};

export type OrderItemPayload = {
  product_id: number;
  quantity: number;
};

export type OrderPayload = {
  customer_name: string;
  customer_phone: string;
  items: OrderItemPayload[];
  idempotency_key?: string;
};

export type OrderResponse = {
  id: string;
  customer_name: string;
  customer_phone: string;
  items: {
    product_id: number;
    product_name: string;
    quantity: number;
    unit_price: number;
  }[];
  total: number;
  created_at: string;
};

function apiErrorMessage(text: string, status: number): string {
  try {
    const data = JSON.parse(text) as { detail?: unknown };
    const { detail } = data;
    if (typeof detail === "string") {
      return detail;
    }
    if (Array.isArray(detail)) {
      const labels: Record<string, string> = {
        customer_name: "имя",
        customer_phone: "телефон",
        items: "состав заказа",
      };
      const parts = new Set<string>();
      for (const item of detail) {
        if (!item || typeof item !== "object") continue;
        const field = String((item as { loc?: unknown[] }).loc?.at(-1) ?? "");
        const label = labels[field] ?? "данные";
        parts.add(`Проверьте ${label}`);
      }
      if (parts.size > 0) {
        return [...parts].join(". ");
      }
    }
  } catch {}
  if (status >= 500) {
    return "Сервер временно недоступен";
  }
  return "Не удалось выполнить запрос";
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${getApiUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(apiErrorMessage(text, res.status));
  }
  return res.json() as Promise<T>;
}

export function fetchProducts(): Promise<Product[]> {
  return apiFetch<Product[]>("/api/products");
}

export function fetchProduct(id: number): Promise<Product> {
  return apiFetch<Product>(`/api/products/${id}`);
}

export function createOrder(payload: OrderPayload): Promise<OrderResponse> {
  return apiFetch<OrderResponse>("/api/orders", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
