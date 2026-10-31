'use client';

import { useState } from 'react';
import type { ContentDoc } from '../../lib/content-store';

const blank = (): ContentDoc => ({
  id: '',
  kind: 'post',
  title: '',
  excerpt: '',
  body: '',
  category: '',
  images: [],
  published: false,
  updatedAt: ''
});

const field = {
  width: '100%',
  padding: 12,
  background: '#20181b',
  color: '#fff8ed',
  border: '1px solid #806957',
  borderRadius: 6,
  marginTop: 6,
  marginBottom: 16
};

export default function Admin() {
  const [key, setKey] = useState('');
  const [logged, setLogged] = useState(false);
  const [docs, setDocs] = useState<ContentDoc[]>([]);
  const [doc, setDoc] = useState<ContentDoc>(blank());
  const [savedId, setSavedId] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [dirty, setDirty] = useState(false);

  async function call(action?: unknown, form?: FormData) {
    const res = await fetch('/api/site-editor', {
      method: action || form ? 'POST' : 'GET',
      cache: 'no-store',
      headers: {
        Authorization: `Bearer ${key}`,
        ...(!form && action ? { 'Content-Type': 'application/json' } : {})
      },
      body: form || (action ? JSON.stringify(action) : undefined)
    });

    const value = await res.json();
    if (!res.ok) throw new Error(value.error || 'Request failed.');
    return value;
  }

  async function load() {
    const value = await call();
    setDocs(value.docs);
  }

  async function run(task: () => Promise<void>) {
    setBusy(true);
    setMessage('Working…');
    try {
      await task();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Operation failed.');
    } finally {
      setBusy(false);
    }
  }

  function change(patch: Partial<ContentDoc>) {
    setDoc(current => ({ ...current, ...patch }));
    setDirty(true);
  }

  function select(next: ContentDoc) {
    if (dirty && !window.confirm('Discard your unsaved changes?')) return;
    setDoc(next);
    setSavedId(next.id);
    setDirty(false);
    setMessage('');
  }

  function reorder(index: number, offset: number) {
    const images = [...doc.images];
    const target = index + offset;
    if (target < 0 || target >= images.length) return;
    [images[index], images[target]] = [images[target], images[index]];
    change({ images });
  }

  return (
    <main style={{
      minHeight: '100vh',
      background: '#110e10',
      color: '#fff8ed',
      padding: '32px 20px',
      fontFamily: 'sans-serif'
    }}>
      <div style={{ maxWidth: 1100, margin: 'auto' }}>
        <a href="/" style={{ color: '#d6bd91' }}>← View website</a>
        <h1 style={{ fontFamily: 'serif', fontSize: 40, margin: '24px 0' }}>
          House editor
        </h1>
        <p>
          Manage pages, blog drafts and photos.
          The first image is the cover; the rest form the gallery.
        </p>
        <p>
          Uploaded images have public URLs, including images attached to drafts.
          Upload only photos intended for public display.
        </p>

        {!logged ? (
          <form onSubmit={event => {
            event.preventDefault();
            void run(async () => {
              await call();
              setLogged(true);
              await load();
              setMessage('Signed in.');
            });
          }}>
            <label>
              Admin key
              <input
                type="password"
                autoComplete="off"
                value={key}
                onChange={event => setKey(event.target.value)}
                style={field}
              />
            </label>
            <button disabled={busy}>Sign in</button>
            <button
              type="button"
              disabled={busy || key.length < 32}
              onClick={() => void run(async () => {
                await call({ action: 'setup' });
                setLogged(true);
                await load();
                setMessage('Storage initialized. Choose a page to edit.');
              })}
            >
              Initialize content storage
            </button>
          </form>
        ) : (
          <>
            <div style={{
              display: 'flex',
              gap: 12,
              flexWrap: 'wrap',
              margin: '24px 0'
            }}>
              <button disabled={busy} onClick={() => {
                if (dirty && !window.confirm('Discard unsaved changes?')) return;
                setDoc(blank());
                setSavedId('');
                setDirty(false);
              }}>
                New blog post
              </button>
              <button disabled={busy} onClick={() => {
                setLogged(false);
                setKey('');
                setDoc(blank());
                setDocs([]);
                setDirty(false);
              }}>
                Sign out
              </button>
              <a
                href="/blog"
                target="_blank"
                rel="noreferrer"
                style={{ color: '#d6bd91' }}
              >
                Open journal ↗
              </a>
            </div>

            <label>
              Choose a page or post
              <select
                disabled={busy}
                style={field}
                value={savedId ? `${doc.kind}/${savedId}` : ''}
                onChange={event => {
                  const selected = docs.find(
                    item => `${item.kind}/${item.id}` === event.target.value
                  );
                  if (selected) select(selected);
                }}
              >
                <option value="">New blog post</option>
                {docs.map(item => (
                  <option
                    key={`${item.kind}/${item.id}`}
                    value={`${item.kind}/${item.id}`}
                  >
                    {item.kind === 'page' ? 'Page' : 'Blog'} · {item.title}
                    {item.published ? '' : ' (draft)'}
                  </option>
                ))}
              </select>
            </label>

            <form onSubmit={event => {
              event.preventDefault();
              void run(async () => {
                const value = await call({ action: 'save', doc });
                setDoc(value.doc);
                setSavedId(value.doc.id);
                setDirty(false);
                await load();
                setMessage(
                  value.doc.published
                    ? 'Published. Refresh the public page to see your changes.'
                    : 'Draft saved.'
                );
              });
            }}>
              <fieldset disabled={busy} style={{ border: 0, padding: 0 }}>
                <label>
                  URL slug
                  <input
                    required
                    pattern="[a-z0-9]+(-[a-z0-9]+)*"
                    maxLength={80}
                    readOnly={Boolean(savedId)}
                    value={doc.id}
                    onChange={event => change({ id: event.target.value })}
                    style={field}
                  />
                </label>
                <label>
                  Title
                  <input
                    required
                    maxLength={180}
                    value={doc.title}
                    onChange={event => change({ title: event.target.value })}
                    style={field}
                  />
                </label>
                <label>
                  Introduction / excerpt
                  <textarea
                    maxLength={600}
                    rows={3}
                    value={doc.excerpt}
                    onChange={event => change({ excerpt: event.target.value })}
                    style={field}
                  />
                </label>
                {doc.kind === 'post' && (
                  <label>
                    Category
                    <input
                      maxLength={80}
                      value={doc.category}
                      onChange={event => change({ category: event.target.value })}
                      style={field}
                    />
                  </label>
                )}
                <label>
                  Body — separate paragraphs with a blank line
                  <textarea
                    maxLength={80000}
                    rows={14}
                    value={doc.body}
                    onChange={event => change({ body: event.target.value })}
                    style={field}
                  />
                </label>
                <label style={{ display: 'block', marginBottom: 20 }}>
                  <input
                    type="checkbox"
                    checked={doc.published}
                    onChange={event => change({
                      published: event.target.checked
                    })}
                  />
                  {' '}Published — uncheck to save privately as a draft
                </label>
                <button type="submit">
                  {doc.published ? 'Save and publish' : 'Save draft'}
                </button>

                {savedId && (
                  <a
                    href={doc.kind === 'post'
                      ? `/blog/${savedId}`
                      : savedId === 'home' ? '/' : `/${savedId}`}
                    target="_blank"
                    rel="noreferrer"
                    style={{ marginLeft: 20, color: '#d6bd91' }}
                  >
                    View public page ↗
                  </a>
                )}
              </fieldset>
            </form>

            <h2 style={{ marginTop: 36 }}>Photos</h2>
            <label>
              Upload one image — JPEG, PNG or WebP, under 3 MB
              <input
                disabled={busy || doc.images.length >= 30}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                style={field}
                onChange={event => {
                  const file = event.target.files?.[0];
                  event.target.value = '';
                  if (!file) return;

                  if (file.size > 3 * 1024 * 1024) {
                    setMessage('Choose an image smaller than 3 MB.');
                    return;
                  }

                  void run(async () => {
                    const form = new FormData();
                    form.set('file', file);
                    const value = await call(undefined, form);
                    change({
                      images: [...doc.images, { url: value.url, alt: '' }]
                    });
                    setMessage(
                      'Photo uploaded. Add its description, then save the page.'
                    );
                  });
                }}
              />
            </label>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit,minmax(230px,1fr))',
              gap: 20
            }}>
              {doc.images.map((image, index) => (
                <div key={image.url}>
                  <img
                    src={image.url}
                    alt={image.alt}
                    style={{
                      width: '100%',
                      height: 240,
                      objectFit: 'contain',
                      background: '#20181b'
                    }}
                  />
                  <p>
                    {index === 0 ? 'Cover image' : `Gallery image ${index + 1}`}
                  </p>
                  <label>
                    Image description / caption
                    <input
                      disabled={busy}
                      maxLength={300}
                      value={image.alt}
                      style={field}
                      onChange={event => change({
                        images: doc.images.map((item, position) =>
                          position === index
                            ? { ...item, alt: event.target.value }
                            : item
                        )
                      })}
                    />
                  </label>
                  <button
                    disabled={busy || index === 0}
                    onClick={() => reorder(index, -1)}
                  >
                    Move up
                  </button>
                  {' '}
                  <button
                    disabled={busy || index === doc.images.length - 1}
                    onClick={() => reorder(index, 1)}
                  >
                    Move down
                  </button>
                  {' '}
                  <button
                    disabled={busy}
                    onClick={() => change({
                      images: doc.images.filter(
                        (_, position) => position !== index
                      )
                    })}
                  >
                    Remove from page
                  </button>
                </div>
              ))}
            </div>

            <p>
              After changing photos, use Save above.
              Removing a photo from a page does not delete its stored file.
            </p>

            {savedId && doc.kind === 'post' && (
              <button
                disabled={busy}
                style={{ marginTop: 32, color: '#ffb5b5' }}
                onClick={() => {
                  if (!window.confirm('Delete this blog post permanently?')) {
                    return;
                  }
                  void run(async () => {
                    await call({
                      action: 'delete',
                      kind: 'post',
                      id: savedId
                    });
                    setDoc(blank());
                    setSavedId('');
                    setDirty(false);
                    await load();
                    setMessage('Post deleted.');
                  });
                }}
              >
                Delete blog post
              </button>
            )}
          </>
        )}

        <p role="status" style={{
          marginTop: 24,
          padding: 12,
          border: '1px solid #806957',
          whiteSpace: 'pre-wrap'
        }}>
          {message || 'Enter the admin key configured in CMS_ADMIN_TOKEN.'}
          {dirty ? ' Unsaved changes.' : ''}
        </p>
        <p style={{ fontSize: 13 }}>
          Keep this key private. Edit from one browser tab at a time.
          Maxine, payment routes and enquiry handling are outside this editor.
        </p>
      </div>
    </main>
  );
}
