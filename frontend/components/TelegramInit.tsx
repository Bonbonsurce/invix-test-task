"use client";

import { useEffect } from "react";
import { initTelegramWebApp } from "@/lib/telegram";

export function TelegramInit() {
  useEffect(() => {
    initTelegramWebApp();
  }, []);
  return null;
}
