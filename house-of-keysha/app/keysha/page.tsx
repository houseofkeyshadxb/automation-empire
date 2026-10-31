'use client';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';

export default function KeyshaPage() {
  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      {/* NAV */}
      <nav className="sticky top-0 z-50 border-b border-burgundy/50 bg-obsidian/95 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 md:px-8 py-4 flex justify-between items-center">
          <Link href="/" className="font-cinzel text-gold text-xl hover:text-gold-light">
            ← House
          </Link>
          <h1 className="font-cinzel text-2xl text-gold">Mistress Keysha</h1>
          <Link href="/contact" className="text-gold text-sm hover:text-gold-light font-cinzel uppercase">
            Inquire
          </Link>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative min-h-[600px] flex items-end overflow-hidden">
        <Image
          src="/images/keysha/keysha-hero.jpg"
          alt="Mistress Keysha"
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
              DOMINATRIX • BDSM • FEMDOM • ELITE
            </div>
            <h1 className="font-cinzel text-6xl md:text-7xl text-gold mb-4">Mistress Keysha</h1>
            <p className="text-2xl text-gold-light italic mb-6">Ruler of the House</p>
            <p className="text-lg text-ivory-muted mb-8 max-w-2xl">
              Psychological mastery meets physical discipline. Real power. Real transformation. No time-wasters.
            </p>
            <div className="flex flex-col md:flex-row gap-4">
              <Link
                href="/contact?persona=keysha"
                className="px-6 py-3 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all inline-block"
              >
                Book Consultation
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

      {/* ABOUT */}
      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-4xl text-gold mb-8">The Dominant</h2>
            <div className="space-y-6 text-lg text-ivory leading-relaxed">
              <p>
                Mistress Keysha does not play at power. She embodies it. With years of experience in psychological
                domination, physical discipline, and the art of absolute control, she has established an Empire
                built on precision, respect, and transformation.
              </p>
              <p>
                Her sessions are not scenes. They are reconstructions. You arrive with assumptions about yourself.
                You leave with clarity about exactly what you are.
              </p>
              <p>
                Serving Mistress Keysha is a privilege that must be earned. Seriousness is non-negotiable.
                Those prepared to surrender completely will find no equal in Dubai.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* GALLERY */}
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
            {['/images/keysha/keysha-hero.jpg', '/images/keysha/keysha-primary.jpg'].map((img, idx) => (
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
                  alt={`Mistress Keysha ${idx + 1}`}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </motion.div>
            ))}
            {[3, 4, 5].map((i) => (
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

      {/* SERVICES */}
      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-cinzel text-4xl text-gold mb-12"
          >
            Services & Experiences
          </motion.h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              { icon: '🧠', title: 'Psychological Domination', desc: 'Mind-bending control. Total mental submission.' },
              { icon: '⛓️', title: 'Bondage & Restraint', desc: 'Complete immobilization in luxury dungeonspace.' },
              { icon: '👠', title: 'Foot Worship', desc: 'The privilege of devotion. For the worthy only.' },
              { icon: '💸', title: 'Financial Domination', desc: 'Your resources are her leash. Serious tributers only.' },
              { icon: '🎓', title: 'Sissy Training', desc: 'Multi-phase transformation and feminization.' },
              { icon: '🔥', title: 'Custom Scenarios', desc: 'Specialized sessions tailored to your surrender.' },
            ].map((service, idx) => (
              <motion.div
                key={service.title}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="p-8 border-l-4 border-gold bg-obsidian/50"
              >
                <div className="text-4xl mb-4">{service.icon}</div>
                <h3 className="font-cinzel text-2xl text-gold mb-3">{service.title}</h3>
                <p className="text-ivory-muted">{service.desc}</p>
                <div className="mt-4 pt-4 border-t border-burgundy/30">
                  <Link href="/contact?persona=keysha" className="text-gold text-sm font-cinzel hover:text-gold-light">
                    Inquire about this service →
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* PACKAGES */}
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
              { name: 'Consultation', duration: '30 min', features: ['Intake & boundaries', 'Scenario customization', 'Schedule planning'], featured: false },
              { name: 'Premium Session', duration: '2 hours', features: ['Full dungeon access', 'Customized scenario', 'Professional documentation'], featured: true },
              { name: 'VIP Experience', duration: '4 hours', features: ['Extended immersion', 'Luxury suite', 'Multiple scenarios', 'Premium aftercare'], featured: false },
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
                    MOST POPULAR
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
                  href="/contact?persona=keysha"
                  className="block text-center py-3 border border-gold text-gold font-cinzel uppercase text-xs tracking-widest hover:bg-gold/10 transition-all"
                >
                  Inquire
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 md:py-24 px-4 md:px-8 bg-espresso">
        <div className="max-w-3xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-cinzel text-4xl text-gold mb-12"
          >
            Frequently Asked Questions
          </motion.h2>
          <div className="space-y-8">
            {[
              { q: 'What is your cancellation policy?', a: 'Cancellations must be made 48 hours in advance for full credit.' },
              { q: 'Is discretion guaranteed?', a: 'Absolute discretion is guaranteed. Discreet billing and complete privacy assured.' },
              { q: 'Are deposits required?', a: 'A 25% deposit is required to secure your appointment, credited toward your final amount.' },
              { q: 'How do I book?', a: 'Complete the inquiry form or message via WhatsApp. Response within 24 hours.' },
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
              >
                <h3 className="font-cinzel text-lg text-gold mb-3">{item.q}</h3>
                <p className="text-ivory-muted">{item.a}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24 px-4 md:px-8 bg-obsidian">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-cinzel text-4xl md:text-5xl text-gold mb-6">Begin Your Submission</h2>
            <p className="text-ivory-muted mb-8">
              Private inquiry welcomed. Discretion guaranteed. Response within 24 hours.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <Link
                href="/contact?persona=keysha"
                className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
              >
                Send Private Enquiry
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

      {/* FOOTER */}
      <footer className="border-t border-burgundy/50 py-8 px-4 md:px-8 bg-espresso text-center">
        <Link href="/" className="text-gold hover:text-gold-light font-cinzel mb-4 inline-block">
          ← Back to House
        </Link>
      </footer>
    </main>
  );
}
