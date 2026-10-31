import { notFound } from 'next/navigation';
import { publicDoc } from '../../../lib/content-store';
import { HouseNav, Editorial } from '../../../components/editorial';

export const dynamic = 'force-dynamic';

export async function generateMetadata({
  params
}: {
  params: { slug: string }
}) {
  const doc = await publicDoc('post', params.slug);
  return {
    title: doc ? `${doc.title} | House of Keysha` : 'Article not found',
    description: doc?.excerpt
  };
}

export default async function Post({
  params
}: {
  params: { slug: string }
}) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(params.slug)) notFound();
  const doc = await publicDoc('post', params.slug);
  if (!doc) notFound();

  return (
    <main className="min-h-screen bg-obsidian text-ivory">
      <HouseNav />
      <Editorial doc={doc} />
    </main>
  );
}
