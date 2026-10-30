import type { Metadata } from "next";
import Script from "next/script";
import { CartProvider } from "@/lib/cart";
import { SiteHeader } from "@/components/SiteHeader";
import { TelegramInit } from "@/components/TelegramInit";
import "./globals.css";

export const metadata: Metadata = {
  title: "Invix Shop",
  description: "Каталог товаров",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <Script src="https://telegram.org/js/telegram-web-app.js" strategy="beforeInteractive" />
        <CartProvider>
          <TelegramInit />
          <div className="container">
            <SiteHeader />
            {children}
          </div>
        </CartProvider>
      </body>
    </html>
  );
}
