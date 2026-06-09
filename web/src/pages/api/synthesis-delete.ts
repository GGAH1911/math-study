// /api/synthesis-delete — remove a synthesis note from docs/syntheses/.
// After unlink, regenerate the byConcept reverse index so the right-side
// "이 페이지의 저장된 노트" card on concept pages and the dashboard /
// graph badges update on the next page load.
//
// Slug is the basename of docs/syntheses/<slug>.md (no extension, no
// path) — same form as the URL `/syntheses/<slug>`.

import type { APIRoute } from 'astro';
import { existsSync, unlinkSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';

export const prerender = false;

const WEB_ROOT = process.cwd();
const REPO_ROOT = resolve(WEB_ROOT, '..');
const SYNTHESES_DIR = resolve(REPO_ROOT, 'docs', 'syntheses');

// Conservative whitelist: Korean letters, ASCII letters/digits, dash,
// underscore, dot, plus optional `.md` suffix. No slash allowed —
// synthesis filenames are flat under docs/syntheses/.
const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_.\-]+$/;

type DeleteBody = { slug: string };

function json(payload: unknown, status: number): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export const POST: APIRoute = async ({ request, locals }) => {
  if (!locals.user) return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'content-type': 'application/json' } });
  let body: DeleteBody;
  try { body = (await request.json()) as DeleteBody; }
  catch { return json({ error: 'invalid json' }, 400); }

  const raw = (body.slug ?? '').trim();
  if (!raw || !SLUG_RE.test(raw) || raw.includes('..')) {
    return json({ error: 'invalid slug' }, 400);
  }
  const filename = raw.endsWith('.md') ? raw : `${raw}.md`;
  const filepath = join(SYNTHESES_DIR, filename);
  // Containment check — `path.join` already canonicalizes, but be explicit.
  if (!filepath.startsWith(SYNTHESES_DIR + '/')) {
    return json({ error: 'path traversal' }, 400);
  }
  if (!existsSync(filepath)) {
    return json({ error: 'not found' }, 404);
  }

  try {
    unlinkSync(filepath);
  } catch (e) {
    return json({ error: `unlink failed: ${(e as Error).message}` }, 500);
  }

  // Re-run the index builder so the next page load doesn't show this
  // note in concept-side cards / dashboard / graph badge.
  const indexScript = resolve(WEB_ROOT, 'scripts', 'build-syntheses-index.mjs');
  if (existsSync(indexScript)) {
    spawnSync('node', [indexScript], { cwd: WEB_ROOT, stdio: 'ignore' });
  }

  return json({ ok: true, deleted: `docs/syntheses/${filename}` }, 200);
};
