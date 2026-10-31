import Link from 'next/link';
import type { ContentDoc } from '../lib/content-store';

export function HouseNav() {
  return (
    <nav className="flex flex-wrap gap-6 border-b border-champagne/20 px-6 py-5 text-sm text-champagne">
      <Link href="/">House of Keysha</Link>
      <Link href="/#the-house">The House</Link>
      <Link href="/blog">Journal</Link>
      <Link href="/contact">Enquiries</Link>
    </nav>
  );
}

export function Editorial({ doc }: { doc: ContentDoc }) {
  return (
    <article className="mx-auto max-w-5xl px-6 py-16">
      <p className="mb-3 text-sm uppercase tracking-widest text-champagne">
        {doc.category || 'House of Keysha'}
      </p>
      <h1 className="mb-6 font-serif text-5xl text-champagne">{doc.title}</h1>
      <p className="mb-10 max-w-3xl text-xl leading-relaxed">{doc.excerpt}</p>

      {doc.images[0] && (
        <figure className="mb-12">
          <img
            src={doc.images[0].url}
            alt={doc.images[0].alt}
            className="max-h-[700px] w-full rounded object-contain"
          />
          {doc.images[0].alt && (
            <figcaption className="mt-3 text-sm text-muted">
              {doc.images[0].alt}
            </figcaption>
          )}
        </figure>
      )}

      <div className="max-w-3xl space-y-6 text-lg leading-relaxed">
        {doc.body.split(/\n\s*\n/).filter(Boolean).map((paragraph, index) => (
          <p key={index} className="whitespace-pre-wrap">{paragraph}</p>
        ))}
      </div>

      <div className="mt-12 grid gap-6 sm:grid-cols-2">
        {doc.images.slice(1).map(image => (
          <figure key={image.url}>
            <img
              src={image.url}
              alt={image.alt}
              loading="lazy"
              className="w-full rounded object-contain"
            />
            <figcaption className="mt-2 text-sm text-muted">
              {image.alt}
            </figcaption>
          </figure>
        ))}
      </div>
    </article>
  );
}
