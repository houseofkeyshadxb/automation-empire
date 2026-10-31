import type { Metadata } from "next";
import { Playfair_Display, Montserrat, Cinzel_Decorative } from "next/font/google";
import "./globals.css";
import ChatWidget from "../components/ChatWidget";

const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });
const montserrat = Montserrat({ subsets: ["latin"], variable: "--font-montserrat" });
const cinzel = Cinzel_Decorative({ weight: ["400", "700", "900"], subsets: ["latin"], variable: "--font-cinzel" });

export const metadata: Metadata = {
  title: "House of Keysha Empire",
  description: "An Empire of Elegance, Authority, and Mystery.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${playfair.variable} ${montserrat.variable} ${cinzel.variable} antialiased bg-obsidian`}>
        {children}
        <ChatWidget />
      </body>
    </html>
  );
}
