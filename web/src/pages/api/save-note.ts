// /api/save-note — flush the localStorage note for a given slug into
// `docs/notes/<slug>.md`. localStorage is the truth (client owns the
// content + timestamp-based append); this endpoint just persists a snapshot
// so it survives device changes and is git-trackable.

import type { APIRoute } from 'astro';
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';

export const prerender = false;

const WEB_ROOT = process.cwd();
const NOTES_DIR = resolve(WEB_ROOT, '..', 'docs', 'notes');
// sub-dir slug 허용 ('algebra/근의_공식'). `/` 는 sanitizeFilename 이 `_` 로 변환.
const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/;
const MAX_CONTENT_CHARS = 200_000;  // ~5% of localStorage quota

type SaveNoteRequest = {
  slug: string;
  content: string;            // full markdown body (already accumulated client-side)
  collection?: 'concepts' | 'problems';
};

function sanitizeFilename(s: string): string {
  return s.replace(/[^\w가-힣ㄱ-ㅎㅏ-ㅣ_-]/g, '_').slice(0, 60);
}

export const POST: APIRoute = async ({ request }) => {
  let body: SaveNoteRequest;
  try { body = (await request.json()) as SaveNoteRequest; }
  catch { return json({ error: 'invalid json' }, 400); }

  const { slug, content, collection = 'concepts' } = body;
  if (!slug || !SLUG_RE.test(slug)) return json({ error: 'invalid slug' }, 400);
  if (typeof content !== 'string' || content.length === 0) {
    return json({ error: 'empty content' }, 400);
  }
  if (content.length > MAX_CONTENT_CHARS) {
    return json({ error: `content too long (>${MAX_CONTENT_CHARS} chars)` }, 400);
  }

  mkdirSync(NOTES_DIR, { recursive: true });
  const filename = `${sanitizeFilename(slug)}.md`;
  const filepath = join(NOTES_DIR, filename);
  const updated = new Date().toISOString();

  const fileBody = `---
concept: ${slug}
collection: ${collection}
updated: ${updated}
source: chat-derived (LLM-generated, accumulated)
---

${content.trim()}
`;
  writeFileSync(filepath, fileBody, 'utf-8');

  return json({
    ok: true,
    path: `docs/notes/${filename}`,
    bytes: fileBody.length,
  }, 200);
};

// Also expose GET so the client can re-load the persisted note when
// localStorage is empty (e.g. fresh browser).
export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get('slug');
  if (!slug || !SLUG_RE.test(slug)) return json({ error: 'invalid slug' }, 400);
  const filepath = join(NOTES_DIR, `${sanitizeFilename(slug)}.md`);
  try {
    const { readFileSync, existsSync } = await import('node:fs');
    if (!existsSync(filepath)) return json({ content: null }, 200);
    const raw = readFileSync(filepath, 'utf-8');
    // Strip frontmatter for client (which only cares about body content).
    const body = raw.replace(/^---\n[\s\S]*?\n---\n/, '').trim();
    return json({ content: body }, 200);
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
};

function json(payload: unknown, status: number): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
