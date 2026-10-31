import { unstable_noStore as noStore } from 'next/cache';
import { getDb } from './supabase/server';

export type ContentDoc = {
  id: string;
  kind: 'page' | 'post';
  title: string;
  excerpt: string;
  body: string;
  category: string;
  images: { url: string; alt: string }[];
  published: boolean;
  updatedAt: string;
};

export const CONTENT_BUCKET = 'hok-site-content';
export const IMAGE_BUCKET = 'hok-site-images';

export const pageNames: Record<string, string> = {
  home: 'House of Keysha',
  keysha: 'Mistress Keysha',
  becky: 'Becky',
  mae: 'Mae',
  pepper: 'Pepper',
  'master-ron': 'Master Ron',
  duo: 'Duo Experiences',
  academy: 'Academy',
  ceo: 'CEO Programme',
  concierge: 'Maison Privé Concierge',
  vault: 'Private Vault'
};

export async function readDoc(
  kind: 'page' | 'post',
  id: string
): Promise<ContentDoc | null> {
  noStore();
  const { data, error } = await getDb().storage
    .from(CONTENT_BUCKET)
    .download(`${kind}/${id}.json`);

  if (error) {
    const status = String((error as { statusCode?: string }).statusCode);
    if (['404', '400'].includes(status)) return null;
    throw new Error('Content could not be loaded. Check Supabase Storage.');
  }

  return JSON.parse(await data.text()) as ContentDoc;
}

export async function listDocs(
  kind: 'page' | 'post'
): Promise<ContentDoc[]> {
  noStore();
  const { data, error } = await getDb().storage
    .from(CONTENT_BUCKET)
    .list(kind, {
      limit: 1000,
      sortBy: { column: 'name', order: 'asc' }
    });

  if (error) {
    throw new Error('Content storage is unavailable. Initialize it in /admin.');
  }

  const docs = await Promise.all(
    (data || [])
      .filter(file => file.name.endsWith('.json'))
      .map(file => readDoc(kind, file.name.slice(0, -5)))
  );

  return docs.filter((doc): doc is ContentDoc => Boolean(doc));
}

export async function writeDoc(doc: ContentDoc) {
  const { error } = await getDb().storage
    .from(CONTENT_BUCKET)
    .upload(`${doc.kind}/${doc.id}.json`, JSON.stringify(doc), {
      contentType: 'application/json',
      cacheControl: '0',
      upsert: true
    });

  if (error) throw new Error('Content was not saved. Check Storage permissions.');
}

export async function publicDoc(kind: 'page' | 'post', id: string) {
  const doc = await readDoc(kind, id);
  return doc?.published ? doc : null;
}
