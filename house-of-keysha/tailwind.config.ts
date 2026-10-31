import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#0A0608',
        espresso: '#100D0E',
        burgundy: '#6B1D2A',
        'burgundy-light': '#8B2535',
        gold: '#C9A84C',
        'gold-light': '#E2C97E',
        ivory: '#e8ddd0',
        'ivory-muted': '#9a8e84',
      },
      fontFamily: {
        serif: ['var(--font-playfair)', 'serif'],
        sans: ['var(--font-montserrat)', 'sans-serif'],
        cinzel: ['Cinzel Decorative', 'serif'],
        cormorant: ['Cormorant Garamond', 'serif'],
      },
    },
  },
  plugins: [],
};
export default config;
