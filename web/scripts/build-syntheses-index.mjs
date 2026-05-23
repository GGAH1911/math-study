#!/usr/bin/env node
/**
 * Build a reverse index mapping each concept slug → the list of synthesis
 * notes that were promoted from chats on that concept page.
 *
 * Output: web/src/data/syntheses-by-concept.json
 *   {
 *     generatedAt: ISO date,
 *     total: number,
 *     byConcept: {
 *       '<concept-slug>': [
 *         { slug, title, created, review_state, excerpt },
 *         ...
 *       ],
 *     },
 *     recent: [{ slug, title, created, origin_concept, excerpt }, ...]
 *       // newest-first, full list (dashboard uses the first N).
 *   }
 *
 * Consumer pages:
 *   - /concepts/[...slug].astro — right-side "이 페이지의 저장된 노트"
 *   - /graph (via graph.astro injecting note_count into nodes) — 🗒N badge
 *   - / (dashboard) — "최근 학습 노트" card (uses `recent` array)
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const SYNTHESES_DIR = join(REPO_ROOT, 'docs', 'syntheses');
const OUT_DIR = join(WEB_ROOT, 'src', 'data');
const OUT_FILE = join(OUT_DIR, 'syntheses-by-concept.json');

// origin_concept frontmatter is `docs/concepts/<slug>.md` — strip the
// wrapping bits so we can join with concept-graph node ids directly.
function normalizeConceptRef(s) {
  if (!s) return null;
  return String(s).replace(/^docs\/concepts\//, '').replace(/\.md$/, '');
}

// Pull a short excerpt from the `## 답변` section (chat-derived promote
// files always have this header — see /api/promote.ts). Skips section
// headers and bullet-only lines to land on the first real prose chunk.
function extractExcerpt(body) {
  if (!body) return null;
  const m = body.match(/##\s*답변\s*\n+([\s\S]+)$/);
  const chunk = (m ? m[1] : body).trim();
  if (!chunk) return null;
  const lines = chunk.split('\n');
  const buf = [];
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) {
      if (buf.length) break; // first paragraph end
      continue;
    }
    if (line.startsWith('#')) continue;       // section headers
    if (line.startsWith('---')) continue;     // hr
    if (line.startsWith('>')) continue;       // blockquote
    if (/^[-*+]\s/.test(line)) {
      // first content might be a bullet list — strip marker and accept
      buf.push(line.replace(/^[-*+]\s+/, ''));
      continue;
    }
    if (line.startsWith('[학습 노트 요청]')) continue;
    buf.push(line);
  }
  const text = buf.join(' ')
    .replace(/[*_`]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  return text.slice(0, 140) || null;
}

// Derive a human-readable title. promote.ts writes `# <something>` as the
// first line of the body; we prefer that. Fall back to the filename's
// trailing segment (after the leading date and slug-leaf) if the body has
// no h1.
function deriveTitle(filename, body) {
  const m = body?.match(/^#\s+(.+?)\s*$/m);
  if (m) return m[1].trim();
  // filename: YYYY-MM-DD_<slugLeaf>_<rest>.md
  const stem = filename.replace(/\.md$/, '');
  const parts = stem.split('_');
  if (parts.length >= 3) return parts.slice(2).join(' ').replace(/_/g, ' ');
  return stem;
}

function main() {
  if (!existsSync(SYNTHESES_DIR)) {
    console.log('[syntheses-index] no docs/syntheses/ — emitting empty index');
    mkdirSync(OUT_DIR, { recursive: true });
    writeFileSync(OUT_FILE, JSON.stringify({
      generatedAt: new Date().toISOString(),
      total: 0,
      byConcept: {},
      recent: [],
    }, null, 2), 'utf-8');
    return;
  }

  const files = readdirSync(SYNTHESES_DIR).filter((f) => f.endsWith('.md'));
  const byConcept = {};
  const all = [];

  for (const f of files) {
    const abs = join(SYNTHESES_DIR, f);
    const parsed = matter(readFileSync(abs, 'utf-8'));
    const fm = parsed.data ?? {};
    const slug = f.replace(/\.md$/, '');
    const conceptRef = normalizeConceptRef(fm.origin_concept);
    const created = fm.created
      ? new Date(fm.created).toISOString().slice(0, 10)
      : (f.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? null);
    const entry = {
      slug,
      title: deriveTitle(f, parsed.content),
      created,
      review_state: fm.review_state ?? null,
      excerpt: extractExcerpt(parsed.content),
      origin_concept: conceptRef,
    };
    all.push(entry);
    if (conceptRef) {
      (byConcept[conceptRef] ??= []).push({
        slug: entry.slug,
        title: entry.title,
        created: entry.created,
        review_state: entry.review_state,
        excerpt: entry.excerpt,
      });
    }
  }

  // Sort each concept's notes newest-first.
  for (const k of Object.keys(byConcept)) {
    byConcept[k].sort((a, b) => (b.created ?? '').localeCompare(a.created ?? ''));
  }
  all.sort((a, b) => (b.created ?? '').localeCompare(a.created ?? ''));

  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify({
    generatedAt: new Date().toISOString(),
    total: all.length,
    byConcept,
    recent: all,
  }, null, 2), 'utf-8');

  console.log(`[syntheses-index] ${all.length} syntheses indexed, ${Object.keys(byConcept).length} concepts have ≥1 note → ${OUT_FILE}`);
}

main();
