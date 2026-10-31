import Link from 'next/link';
import { listDocs } from '../../lib/content-store';
import { HouseNav } from '../../components/editorial';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Journal | House of Keysha' };

export default async function Blog({
  searchParams
}: {
  searchParams: { q?: string; category?: string }
}) {
  let unavailable = false;
  const docs = await listDocs('post').catch(() => {
    unavailable = true;
    return [];
  });

  const posts = docs
    .filter(doc => doc.published)
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));

  const q = typeof searchParams.q === 'string'
    ? searchParams.q.toLowerCase()
    : '';

  const category = typeof searchParams.category === 'string'
    ? searchParams.category
    : '';

  const filtered = posts.filter(post =>
    (!category || post.category === category)
    && `${post.title} ${post.excerpt} ${post.body}`.toLowerCase().includes(q)
  );

  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      <HouseNav />
      <section className="mx-auto max-w-7xl px-6 py-16">
        <p className="text-sm uppercase tracking-widest text-champagne">
          Stories from the House
        </p>
        <h1 className="my-5 font-serif text-6xl text-champagne">The Journal</h1>

        <form className="my-10 flex flex-wrap gap-3">
          <input
            name="q"
            aria-label="Search articles"
            defaultValue={q}
            placeholder="Search articles"
            className="rounded border border-champagne/30 bg-espresso p-3"
          />
          <select
            name="category"
            aria-label="Category"
            defaultValue={category}
            className="rounded border border-champagne/30 bg-espresso p-3"
          >
            <option value="">All categories</option>
            {Array.from(
              new Set(posts.map(post => post.category).filter(Boolean))
            ).map(value => <option key={value}>{value}</option>)}
          </select>
          <button className="bg-burgundy px-6 py-3">Search</button>
        </form>

        {unavailable ? (
          <p>The journal is temporarily unavailable. Please try again later.</p>
        ) : filtered.length ? (
          <div className="grid gap-8 md:grid-cols-3">
            {filtered.map(post => (
              <Link
                key={post.id}
                href={`/blog/${post.id}`}
                className="overflow-hidden rounded border border-champagne/20 bg-espresso"
              >
                {post.images[0] && (
                  <img
                    src={post.images[0].url}
                    alt={post.images[0].alt}
                    loading="lazy"
                    className="aspect-[4/3] w-full object-cover"
                  />
                )}
                <div className="p-6">
                  <p className="text-sm text-champagne">{post.category}</p>
                  <h2 className="my-3 font-serif text-2xl">{post.title}</h2>
                  <p>{post.excerpt}</p>
                  <p className="mt-6 text-sm text-champagne">Read article →</p>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <p>
            {posts.length
              ? 'No matching articles.'
              : 'Our first stories are on their way.'}
          </p>
        )}
      </section>
    </main>
  );
}
