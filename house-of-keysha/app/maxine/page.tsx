'use client';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function Page() {
  return (
    <main className="min-h-screen bg-obsidian text-ivory flex items-center justify-center">
      <nav className="absolute top-0 w-full border-b border-burgundy/50 bg-obsidian/95">
        <div className="max-w-6xl mx-auto px-4 md:px-8 py-4">
          <Link href="/" className="font-cinzel text-gold hover:text-gold-light">
            ← House
          </Link>
        </div>
      </nav>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center px-4"
      >
        <div className="text-6xl mb-6">✨</div>
        <h1 className="font-cinzel text-5xl text-gold mb-6">Maxine</h1>
        <p className="text-ivory-muted text-lg mb-8 max-w-xl mx-auto">
          This page is being developed. Check back soon for exclusive content and experiences.
        </p>
        <Link
          href="/"
          className="inline-block px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
        >
          Back to House
        </Link>
      </motion.div>
    </main>
  );
}
