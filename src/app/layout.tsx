import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Color Pop Game",
  description:
    "Color Pop — puzzle viciante: deixe todas as bolinhas da mesma cor. Singleplayer, PvP local e vs Bot.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}
