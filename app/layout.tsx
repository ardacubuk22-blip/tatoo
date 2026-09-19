import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TATOO Studio",
  description: "Dövme stüdyosu portföy ve galeri sitesi",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <body className="bg-ink text-white">{children}</body>
    </html>
  );
}
