'use client';
import Link from 'next/link';
import { useState } from 'react';
import { motion } from 'framer-motion';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    persona: '',
    offering: '',
    name: '',
    email: '',
    phone: '',
    date: '',
    time: '',
    message: '',
  });

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        alert('Inquiry sent. Response within 24 hours.');
        setFormData({ persona: '', offering: '', name: '', email: '', phone: '', date: '', time: '', message: '' });
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      <nav className="border-b border-burgundy/50 bg-obsidian/95">
        <div className="max-w-3xl mx-auto px-4 md:px-8 py-4">
          <Link href="/" className="font-cinzel text-gold hover:text-gold-light">
            ← House
          </Link>
        </div>
      </nav>

      <section className="py-20 md:py-32 px-4 md:px-8">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="font-cinzel text-5xl md:text-6xl text-gold mb-6">Private Enquiry</h1>
            <p className="text-ivory-muted mb-12 text-lg">
              Complete discretion guaranteed. Response within 24 hours.
            </p>

            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">Who are you interested in?</label>
                  <select
                    name="persona"
                    value={formData.persona}
                    onChange={handleChange}
                    required
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  >
                    <option value="">Select persona</option>
                    <option value="keysha">Mistress Keysha</option>
                    <option value="becky">Becky</option>
                    <option value="mae">Mae</option>
                    <option value="pepper">Mistress Pepper</option>
                    <option value="master-ron">Master Ron</option>
                    <option value="other">Other / Unsure</option>
                  </select>
                </div>

                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">What are you interested in?</label>
                  <input
                    type="text"
                    name="offering"
                    placeholder="e.g., Consultation, Session, Experience"
                    value={formData.offering}
                    onChange={handleChange}
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  />
                </div>
              </div>

              <div>
                <label className="block text-gold font-cinzel text-sm mb-2">Your name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  />
                </div>
                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">Phone</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">Preferred date</label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  />
                </div>
                <div>
                  <label className="block text-gold font-cinzel text-sm mb-2">Preferred time</label>
                  <input
                    type="time"
                    name="time"
                    value={formData.time}
                    onChange={handleChange}
                    className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition"
                  />
                </div>
              </div>

              <div>
                <label className="block text-gold font-cinzel text-sm mb-2">Additional details</label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  rows={5}
                  placeholder="Tell us more about what you're looking for..."
                  className="w-full bg-espresso border border-burgundy/50 text-ivory p-3 font-cormorant focus:border-gold outline-none transition resize-none"
                />
              </div>

              <div className="flex gap-4">
                <button
                  type="submit"
                  className="px-8 py-4 bg-burgundy text-gold border-2 border-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-burgundy-light transition-all"
                >
                  Send Inquiry
                </button>
                <Link
                  href="/"
                  className="px-8 py-4 border-2 border-gold text-gold font-cinzel uppercase tracking-widest text-sm font-bold hover:bg-gold/10 transition-all"
                >
                  Cancel
                </Link>
              </div>

              <p className="text-ivory-muted text-sm">
                ✓ Discretion guaranteed • ✓ Discreet billing • ✓ Secure encryption • ✓ No spam
              </p>
            </form>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
