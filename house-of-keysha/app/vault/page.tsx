'use client';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function VaultPage() {
  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      <nav className="sticky top-0 z-50 border-b border-burgundy/50 bg-obsidian/95">
        <div className="max-w-6xl mx-auto px-4 md:px-8 py-4">
          <Link href="/" className="font-cinzel text-gold hover:text-gold-light">
            ← House
          </Link>
        </div>
      </nav>

      <section className="py-20 md:py-32 px-4 md:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="text-6xl mb-6">🔐</div>
            <h1 className="font-cinzel text-5xl md:text-6xl text-gold mb-6">The Private Vault</h1>
            <p className="text-ivory-muted text-lg mb-12 max-w-2xl mx-auto">
              Exclusive digital collection featuring curated content from House of Keysha Empire.
            </p>

            <div className="bg-espresso border-2 border-burgundy/50 p-12 mb-12">
              <h2 className="font-cinzel text-2xl text-gold mb-6">Member Access Required</h2>
              <p className="text-ivory-muted mb-8">
                The Private Vault is an exclusive digital collection available to verified members only.
              </p>
              <div className="flex flex-col md:flex-row gap-4 justify-center">
                <Link
                  href="/contact"
                  className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
                >
                  Request Access
                </Link>
                <a
                  href="https://wa.me/971567620449"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
                >
                  Ask on WhatsApp
                </a>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="p-8 border border-burgundy/50 bg-espresso/50">
                <h3 className="font-cinzel text-gold text-lg mb-4">Featured Collections</h3>
                <ul className="text-ivory-muted space-y-2 text-sm">
                  <li>✓ Exclusive photoshoots</li>
                  <li>✓ Behind-the-scenes content</li>
                  <li>✓ Editorial galleries</li>
                  <li>✓ Member-only updates</li>
                </ul>
              </div>
              <div className="p-8 border border-burgundy/50 bg-espresso/50">
                <h3 className="font-cinzel text-gold text-lg mb-4">How It Works</h3>
                <ul className="text-ivory-muted space-y-2 text-sm">
                  <li>✓ Secure member login</li>
                  <li>✓ Age-verified access</li>
                  <li>✓ Discreet streaming</li>
                  <li>✓ New content regularly</li>
                </ul>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
