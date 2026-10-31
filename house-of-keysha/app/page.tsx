'use client';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';

export default function Home() {
  const personas = [
    { name: 'Mistress Keysha', icon: '👑', href: '/keysha', image: '/images/keysha/keysha-hero.jpg', tagline: 'The Empress' },
    { name: 'Becky', icon: '🌹', href: '/becky', image: '/images/becky/becky-hero.jpg', tagline: 'The Muse' },
    { name: 'Mae', icon: '🌸', href: '/mae', image: null, tagline: 'Coming Soon' },
    { name: 'Master Ron', icon: '⚔️', href: '/master-ron', image: null, tagline: 'The Guide' },
    { name: 'Mistress Pepper', icon: '🌶️', href: '/pepper', image: null, tagline: 'Coming Soon' },
  ];

  const divisions = [
    { title: 'Individual Experiences', description: 'Curated one-on-one sessions', href: '/keysha', icon: '✨' },
    { title: 'Duo Experiences', description: 'Shared encounters with multiple personas', href: '/duo', icon: '💫' },
    { title: 'Academy', description: 'Educational and training programmes', href: '/academy', icon: '📚' },
    { title: 'CEO Programme', description: 'Executive discipline and guidance', href: '/ceo', icon: '💼' },
    { title: 'Maison Privé', description: 'Luxury concierge services', href: '/concierge', icon: '🏰' },
    { title: 'Private Vault', description: 'Exclusive digital media collection', href: '/vault', icon: '🔐' },
  ];

  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      {/* HERO SECTION */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <Image
            src="/images/keysha/keysha-hero.jpg"
            alt="House of Keysha Empire"
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-t from-obsidian via-obsidian/50 to-obsidian/30"></div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="relative z-10 text-center px-4 max-w-4xl"
        >
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="font-cinzel text-6xl md:text-7xl font-bold text-gold mb-4 leading-tight"
            style={{ textShadow: '0 0 50px rgba(201,168,76,0.4)' }}
          >
            House of Keysha Empire
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.4 }}
            className="text-xl md:text-2xl text-gold-light mb-8 italic tracking-wide"
          >
            An Elegant Dominion of Luxury, Power & Transformation
          </motion.p>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.6 }}
            className="text-lg text-ivory-muted mb-12 max-w-2xl mx-auto leading-relaxed"
          >
            Dubai's most exclusive destination for discerning experiences.
            Multiple personas. Curated offerings. Absolute discretion.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.8 }}
            className="flex flex-col md:flex-row gap-6 justify-center"
          >
            <Link
              href="#meet-the-house"
              className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light hover:shadow-lg transition-all"
            >
              Explore the House
            </Link>
            <Link
              href="/contact"
              className="px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
            >
              Private Enquiry
            </Link>
          </motion.div>
        </motion.div>
      </section>

      {/* MEET THE HOUSE */}
      <section id="meet-the-house" className="py-20 md:py-32 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-cinzel text-5xl md:text-6xl text-gold mb-4">
              Meet the House
            </h2>
            <div className="w-24 h-1 bg-gradient-to-r from-burgundy via-gold to-burgundy mx-auto"></div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            {personas.map((persona, idx) => (
              <motion.div
                key={persona.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="group"
              >
                <Link href={persona.href}>
                  <div className="relative h-96 overflow-hidden border-2 border-burgundy/50 hover:border-gold transition-all duration-300">
                    {persona.image ? (
                      <Image
                        src={persona.image}
                        alt={persona.name}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full bg-burgundy/20 flex items-center justify-center">
                        <div className="text-center">
                          <div className="text-6xl mb-4">{persona.icon}</div>
                          <p className="text-gold text-sm font-cinzel">{persona.tagline}</p>
                        </div>
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-obsidian via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
                      <div>
                        <h3 className="font-cinzel text-2xl text-gold">{persona.name}</h3>
                        <p className="text-gold-light text-sm">{persona.tagline}</p>
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* EXPLORE OUR WORLD */}
      <section className="py-20 md:py-32 px-4 md:px-8 bg-obsidian">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-cinzel text-5xl md:text-6xl text-gold mb-4">
              Explore Our World
            </h2>
            <div className="w-24 h-1 bg-gradient-to-r from-burgundy via-gold to-burgundy mx-auto"></div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {divisions.map((div, idx) => (
              <motion.div
                key={div.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <Link href={div.href}>
                  <div className="p-8 border-2 border-burgundy/50 hover:border-gold bg-espresso/50 hover:bg-espresso transition-all duration-300 group">
                    <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">{div.icon}</div>
                    <h3 className="font-cinzel text-2xl text-gold mb-2">{div.title}</h3>
                    <p className="text-ivory-muted mb-4">{div.description}</p>
                    <span className="text-gold text-sm font-cinzel tracking-wider">Explore →</span>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURED EXPERIENCES */}
      <section className="py-20 md:py-32 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-cinzel text-5xl md:text-6xl text-gold mb-4">
              Featured Experiences
            </h2>
            <div className="w-24 h-1 bg-gradient-to-r from-burgundy via-gold to-burgundy mx-auto"></div>
            <p className="text-ivory-muted mt-6 max-w-2xl mx-auto">
              Curated offerings across our collective, with pricing available upon inquiry.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { name: 'Consultation Session', duration: '1 hour', persona: 'Mistress Keysha', desc: 'Initial inquiry and experience planning' },
              { name: 'Private Experience', duration: '2 hours', persona: 'Available', desc: 'Immersive personalized session' },
              { name: 'Premium Encounter', duration: '3+ hours', persona: 'Available', desc: 'Extended bespoke arrangement' },
            ].map((exp, idx) => (
              <motion.div
                key={exp.name}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="border-l-4 border-gold p-8 bg-obsidian/50"
              >
                <div className="text-sm text-gold-light font-cinzel mb-2">{exp.persona}</div>
                <h3 className="font-cinzel text-2xl text-gold mb-2">{exp.name}</h3>
                <p className="text-ivory-muted mb-4">{exp.desc}</p>
                <div className="flex justify-between items-center">
                  <span className="text-gold text-sm">{exp.duration}</span>
                  <Link href="/contact" className="text-gold hover:text-gold-light text-sm font-cinzel tracking-wider">
                    Inquire →
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* PRIVATE VAULT TEASER */}
      <section className="py-20 md:py-32 px-4 md:px-8 bg-obsidian">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="border-2 border-gold/50 p-12 text-center"
          >
            <h2 className="font-cinzel text-4xl md:text-5xl text-gold mb-4">The Private Vault</h2>
            <p className="text-ivory-muted mb-8 text-lg">
              Exclusive digital collection of curated content. Member access with verified discretion.
            </p>
            <Link
              href="/vault"
              className="inline-block px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
            >
              Explore the Vault
            </Link>
          </motion.div>
        </div>
      </section>

      {/* CONCIERGE */}
      <section className="py-20 md:py-32 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-5xl md:text-6xl text-gold mb-6">Maison Privé Concierge</h2>
            <p className="text-ivory-muted text-lg mb-12 max-w-2xl mx-auto">
              Personalized guidance through your journey. Your dedicated concierge awaits.
            </p>
            <Link
              href="/concierge"
              className="inline-block px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
            >
              Request Concierge
            </Link>
          </motion.div>
        </div>
      </section>

      {/* CONTACT CTA */}
      <section className="py-20 md:py-32 px-4 md:px-8 bg-obsidian">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-5xl md:text-6xl text-gold mb-6">Begin Your Journey</h2>
            <p className="text-ivory-muted text-lg mb-12">
              Private enquiries welcome. Discretion guaranteed. Response within 24 hours.
            </p>
            <div className="flex flex-col md:flex-row gap-6 justify-center">
              <Link
                href="/contact"
                className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
              >
                Private Enquiry Form
              </Link>
              <a
                href="https://wa.me/971567620449"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
              >
                WhatsApp
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t-2 border-burgundy/50 py-12 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto text-center">
          <h3 className="font-cinzel text-2xl text-gold mb-4">House of Keysha Empire</h3>
          <p className="text-ivory-muted mb-6">Dubai • Discretion • Excellence</p>
          <div className="flex justify-center gap-8 mb-8 text-sm">
            <Link href="/vault" className="text-gold hover:text-gold-light">Vault</Link>
            <Link href="/concierge" className="text-gold hover:text-gold-light">Concierge</Link>
            <Link href="/contact" className="text-gold hover:text-gold-light">Contact</Link>
            <Link href="/academy" className="text-gold hover:text-gold-light">Academy</Link>
          </div>
          <p className="text-ivory-muted text-xs">
            © 2026 House of Keysha Empire. All rights reserved. Content is for adults 18+.
          </p>
        </div>
      </footer>
    </main>
  );
}
