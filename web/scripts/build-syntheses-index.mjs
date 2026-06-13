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
 *     recent: [{ slug, title, created, origin_concept, origin_title, excerpt }, ...]
 *       // newest-first, full list (dashboard uses the first N).
 *       // title is the chat h1, or the concept-graph label when the h1 is a
 *       // raw concept path; origin_title is always the graph label (if any).
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
const CONCEPT_GRAPH_FILE = join(OUT_DIR, 'concept-graph.json');

// concept-graph.json: { nodes: [{ id, label, prerequisites: [...] }, ...] }.
// Build id → { label, prereq } so deriveTitle can swap a raw-path h1 for the
// node's human label (e.g. id '.../논리' → label '논리').
function loadConceptLabels() {
  const map = new Map();
  if (!existsSync(CONCEPT_GRAPH_FILE)) return map;
  try {
    const graph = JSON.parse(readFileSync(CONCEPT_GRAPH_FILE, 'utf-8'));
    for (const n of graph.nodes ?? []) {
      if (n?.id) map.set(n.id, { label: n.label ?? null, prereq: n.prerequisites?.[0] ?? null });
    }
  } catch (e) {
    console.warn(`[syntheses-index] could not read concept-graph.json: ${e.message}`);
  }
  return map;
}

// Resolve a concept ref to a display title via the graph: leaf node label,
// optionally prefixed with its parent unit label as '<unit> › <leaf>'.
function conceptTitle(conceptRef, conceptLabels) {
  if (!conceptRef) return null;
  const node = conceptLabels.get(conceptRef);
  if (!node?.label) return null;
  const parent = node.prereq ? conceptLabels.get(node.prereq) : null;
  return parent?.label ? `${parent.label} › ${node.label}` : node.label;
}

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
  let out = text.slice(0, 140);
  // 140자 컷이 `$…$` 한가운데를 끊으면 닫는 `$` 없는 dangling `$` 가 남아
  // KaTeX 가 못 렌더하고 리터럴 `$a < 0` 로 노출된다 → `$` 개수가 홀수면
  // 마지막 여는 `$` 이후를 잘라낸다(수식 토막 제거).
  if (((out.match(/\$/g) || []).length) % 2 === 1) out = out.slice(0, out.lastIndexOf('$')).trim();
  return out || null;
}

// A raw-path h1 is one promote.ts emitted from the concept slug rather than
// a real chat title — e.g. '학습 노트 - logic/high-1/집합과_명제/논리'. We
// detect path-ish shapes (slash segments / underscore-joined slug segments /
// ascii slug tokens like 'algebra'·'high-1') so they can be replaced by the
// concept label. A clean Korean label ('여러가지 함수의 극한과 연속') is kept.
function isRawPathTitle(h1) {
  if (!h1) return false;
  // strip the standard '학습 노트 - ' prefix before inspecting the remainder
  const rest = h1.replace(/^학습\s*노트\s*-\s*/, '');
  if (rest.includes('/')) return true;                 // slash path segments
  if (/[A-Za-z0-9가-힣]+_[A-Za-z0-9가-힣]/.test(rest)) return true; // underscore-joined slug
  if (/(^|\s)[a-z][a-z0-9-]*([/_]|$)/.test(rest)) return true;     // ascii slug token
  return false;
}

// Derive a human-readable title. promote.ts writes `# <something>` as the
// first line of the body; we prefer that, *unless* it is a raw concept-path
// h1 — then we use the concept-graph label (conceptTitle) instead. Fall back
// to the filename's trailing segment (after the leading date and slug-leaf)
// if the body has no usable h1.
function deriveTitle(filename, body, conceptTitleHint) {
  const m = body?.match(/^#\s+(.+?)\s*$/m);
  if (m) {
    const h1 = m[1].trim();
    if (!isRawPathTitle(h1)) return h1;
    if (conceptTitleHint) return conceptTitleHint;
    // no graph label: fall through to filename/leaf cleanup below
  } else if (conceptTitleHint) {
    return conceptTitleHint;
  }
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
  const conceptLabels = loadConceptLabels();
  const byConcept = {};
  const all = [];

  for (const f of files) {
    const abs = join(SYNTHESES_DIR, f);
    const parsed = matter(readFileSync(abs, 'utf-8'));
    const fm = parsed.data ?? {};
    const slug = f.replace(/\.md$/, '');
    const conceptRef = normalizeConceptRef(fm.origin_concept);
    const originTitle = conceptTitle(conceptRef, conceptLabels);
    const created = fm.created
      ? new Date(fm.created).toISOString().slice(0, 10)
      : (f.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? null);
    const entry = {
      slug,
      title: deriveTitle(f, parsed.content, originTitle),
      created,
      review_state: fm.review_state ?? null,
      excerpt: extractExcerpt(parsed.content),
      origin_concept: conceptRef,
      origin_title: originTitle,
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
