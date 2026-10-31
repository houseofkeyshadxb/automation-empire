'use client';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';

export default function BeckyPage() {
  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      <nav className="sticky top-0 z-50 border-b border-burgundy/50 bg-obsidian/95 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 md:px-8 py-4 flex justify-between items-center">
          <Link href="/" className="font-cinzel text-gold text-xl hover:text-gold-light">
            ← House
          </Link>
          <h1 className="font-cinzel text-2xl text-gold">Becky</h1>
          <Link href="/contact" className="text-gold text-sm hover:text-gold-light font-cinzel uppercase">
            Inquire
          </Link>
        </div>
      </nav>

      <section className="relative min-h-[600px] flex items-end overflow-hidden">
        <Image
          src="/images/becky/becky-hero.jpg"
          alt="Becky"
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-t from-obsidian via-obsidian/40 to-transparent"></div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="relative z-10 p-8 md:p-16 w-full"
        >
          <div className="max-w-3xl">
            <div className="inline-block px-4 py-2 bg-burgundy/50 border border-gold text-gold text-xs font-cinzel mb-6">
              ALTERNATIVE • THEATRICAL • CONFIDENT • CREATIVE
            </div>
            <h1 className="font-cinzel text-6xl md:text-7xl text-gold mb-4">Becky</h1>
            <p className="text-2xl text-gold-light italic mb-6">The Muse</p>
            <p className="text-lg text-ivory-muted mb-8 max-w-2xl">
              Playful rebellion meets genuine connection. Theatrical, confident, and unapologetically authentic.
            </p>
            <div className="flex flex-col md:flex-row gap-4">
              <Link
                href="/contact?persona=becky"
                className="px-6 py-3 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all inline-block"
              >
                Book Experience
              </Link>
              <a
                href="https://wa.me/971567620449"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all inline-block text-center"
              >
                WhatsApp
              </a>
            </div>
          </div>
        </motion.div>
      </section>

      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-4xl text-gold mb-8">The Muse</h2>
            <div className="space-y-6 text-lg text-ivory leading-relaxed">
              <p>
                Becky embodies playful rebellion. Creative, theatrical, and authentically alternative, 
                she brings genuine connection to every encounter. Her approach is collaborative and imaginative.
              </p>
              <p>
                Whether it's roleplay, fashion, or pure creative expression, Becky excels at crafting 
                experiences that are memorable, fun, and deeply engaging. She celebrates individuality 
                and explores boundaries with enthusiasm.
              </p>
              <p>
                Sessions with Becky are adventures. Come ready to be surprised, delighted, and fully seen.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-16 md:py-24 px-4 md:px-8 bg-obsidian">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-cinzel text-4xl text-gold mb-12"
          >
            Gallery
          </motion.h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {['/images/becky/becky-hero.jpg', '/images/becky/becky-gallery-1.jpg', '/images/becky/becky-gallery-2.jpg', '/images/becky/becky-gallery-3.png'].map((img, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="relative h-96 overflow-hidden border-2 border-burgundy/50 hover:border-gold transition-all group"
              >
                <Image
                  src={img}
                  alt={`Becky ${idx + 1}`}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </motion.div>
            ))}
            {[5].map((i) => (
              <motion.div
                key={`placeholder-${i}`}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: (i - 1) * 0.1 }}
                className="h-96 bg-burgundy/20 border-2 border-burgundy/50 flex items-center justify-center text-ivory-muted"
              >
                <span className="text-sm font-cinzel">Photo {i} - To Be Added</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-cinzel text-4xl text-gold mb-12"
          >
            Experiences
          </motion.h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              { icon: '🎭', title: 'Roleplay & Fantasy', desc: 'Creative scenarios tailored to your imagination.' },
              { icon: '👗', title: 'Fashion & Styling', desc: 'Collaborative wardrobe exploration and makeover.' },
              { icon: '💋', title: 'Intimate Connection', desc: 'Genuine sensuality and personal presence.' },
              { icon: '🎨', title: 'Creative Sessions', desc: 'Art, expression, and authentic exploration.' },
              { icon: '🎉', title: 'Social Experiences', desc: 'Events, outings, and social companionship.' },
              { icon: '🔮', title: 'Bespoke Encounters', desc: 'Custom experiences designed just for you.' },
            ].map((exp, idx) => (
              <motion.div
                key={exp.title}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="p-8 border-l-4 border-gold bg-obsidian/50"
              >
                <div className="text-4xl mb-4">{exp.icon}</div>
                <h3 className="font-cinzel text-2xl text-gold mb-3">{exp.title}</h3>
                <p className="text-ivory-muted">{exp.desc}</p>
                <div className="mt-4 pt-4 border-t border-burgundy/30">
                  <Link href="/contact?persona=becky" className="text-gold text-sm font-cinzel hover:text-gold-light">
                    Explore this experience →
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 md:py-24 px-4 md:px-8 bg-obsidian">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-cinzel text-4xl text-gold mb-12"
          >
            Packages
          </motion.h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { name: 'Coffee Date', duration: '1 hour', features: ['Casual meetup', 'Get to know each other', 'Low-pressure'], featured: false },
              { name: 'Adventure', duration: '3 hours', features: ['Outing or activity', 'Social experience', 'Full attention'], featured: true },
              { name: 'Experience', duration: '4+ hours', features: ['Immersive encounter', 'Multiple activities', 'Premium treatment'], featured: false },
            ].map((pkg, idx) => (
              <motion.div
                key={pkg.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className={`p-8 border-2 transition-all ${
                  pkg.featured ? 'border-gold bg-burgundy/20' : 'border-burgundy/50 bg-espresso/50'
                }`}
              >
                {pkg.featured && (
                  <div className="inline-block px-3 py-1 bg-gold text-obsidian text-xs font-cinzel mb-4">
                    POPULAR
                  </div>
                )}
                <h3 className="font-cinzel text-2xl text-gold mb-2">{pkg.name}</h3>
                <p className="text-ivory-muted mb-6">{pkg.duration}</p>
                <ul className="space-y-3 mb-8">
                  {pkg.features.map((feat, i) => (
                    <li key={i} className="text-sm text-ivory flex gap-3">
                      <span className="text-gold">✦</span> {feat}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/contact?persona=becky"
                  className="block text-center py-3 border border-gold text-gold font-cinzel uppercase text-xs tracking-widest hover:bg-gold/10 transition-all"
                >
                  Inquire
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-4xl md:text-5xl text-gold mb-6">Let's Create Something</h2>
            <p className="text-ivory-muted mb-8">
              Private inquiry welcomed. Let's explore what you're looking for.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <Link
                href="/contact?persona=becky"
                className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
              >
                Send Inquiry
              </Link>
              <a
                href="https://wa.me/971567620449"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
              >
                Message WhatsApp
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      <footer className="border-t border-burgundy/50 py-8 px-4 md:px-8 bg-espresso text-center">
        <Link href="/" className="text-gold hover:text-gold-light font-cinzel mb-4 inline-block">
          ← Back to House
        </Link>
      </footer>
    </main>
  );
}
