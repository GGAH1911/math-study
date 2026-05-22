#!/usr/bin/env node
/**
 * Move every `docs/concepts/uncategorized/*.md` into its canonical
 * `<domain-slug>/<grade-slug>/` directory, then rewrite cross-references
 * (problem files + any straggling flat-path prereqs).
 *
 * Pre-conditions:
 *   - All uncategorized files must have BOTH `domain:` and `grade:` set
 *     (see backfill-concept-domain.mjs + backfill-concept-grade.mjs).
 *
 * Default is dry-run. Pass `--write` to actually do the moves + edits.
 *
 * Usage:
 *   node web/scripts/relocate-uncategorized.mjs                 # preview
 *   node web/scripts/relocate-uncategorized.mjs --write         # apply
 */
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const DOCS_DIR = join(REPO_ROOT, 'docs');
const CONCEPTS_DIR = join(DOCS_DIR, 'concepts');
const UNCAT_DIR = join(CONCEPTS_DIR, 'uncategorized');

const DOMAIN_DIR = {
  '수와식': 'algebra',
  '방정식': 'equations',
  '함수': 'functions',
  '도형': 'geometry',
  '확률통계': 'probability-stats',
  '논리': 'logic',
};
const GRADE_DIR = {
  '중1': 'middle-1',
  '중2': 'middle-2',
  '중3': 'middle-3',
  '고1': 'high-1',
  '수학1': 'math-1',
  '수학2': 'math-2',
  '미적분': 'calculus',
  '기하': 'geometry-elective',
  '확률과통계': 'prob-stats-elective',
};

// Stale flat-path prereqs that the 3 orphan files still carry. The
// concept-graph build couldn't resolve them, so they're not in `enables`
// either. Replace with the canonical subdir path.
const STALE_FLAT_REPLACEMENTS = [
  ['docs/concepts/여러가지함수의_극한.md',  'docs/concepts/functions/calculus/여러가지함수의_극한.md'],
  ['docs/concepts/함수의_극한과_연속.md',   'docs/concepts/functions/math-2/함수의_극한과_연속.md'],
  ['docs/concepts/삼각함수.md',           'docs/concepts/functions/math-1/삼각함수.md'],
];

function parseFrontmatter(text) {
  if (!text.startsWith('---')) return {};
  const end = text.indexOf('---', 3);
  if (end < 0) return {};
  const fm = {};
  for (const line of text.slice(3, end).split('\n')) {
    const m = line.match(/^([a-zA-Z_]+):\s*(.*)$/);
    if (!m) continue;
    fm[m[1]] = m[2].trim();
  }
  return fm;
}

function walkMd(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) walkMd(p, out);
    else if (entry.endsWith('.md')) out.push(p);
  }
  return out;
}

function main() {
  const write = process.argv.includes('--write');

  if (!existsSync(UNCAT_DIR)) {
    console.log('uncategorized/ already gone — nothing to relocate.');
    return;
  }

  // ---- Phase 1: plan moves ----
  const moves = []; // { srcAbs, dstAbs, srcRel, dstRel, oldId, newId }
  const collisions = [];
  const skippedNoMeta = [];
  for (const file of readdirSync(UNCAT_DIR)) {
    if (!file.endsWith('.md')) continue;
    const srcAbs = join(UNCAT_DIR, file);
    const fm = parseFrontmatter(readFileSync(srcAbs, 'utf-8'));
    if (!fm.domain || !fm.grade) { skippedNoMeta.push(file); continue; }
    const domSlug = DOMAIN_DIR[fm.domain];
    const grdSlug = GRADE_DIR[fm.grade];
    if (!domSlug || !grdSlug) {
      console.log(`  ! unknown domain/grade for ${file}: ${fm.domain} / ${fm.grade}`);
      skippedNoMeta.push(file);
      continue;
    }
    const dstAbs = join(CONCEPTS_DIR, domSlug, grdSlug, file);
    if (existsSync(dstAbs)) { collisions.push({ file, dstAbs }); continue; }
    const srcRel = relative(REPO_ROOT, srcAbs);
    const dstRel = relative(REPO_ROOT, dstAbs);
    const oldId = `uncategorized/${file.replace(/\.md$/, '')}`;
    const newId = `${domSlug}/${grdSlug}/${file.replace(/\.md$/, '')}`;
    moves.push({ srcAbs, dstAbs, srcRel, dstRel, oldId, newId });
  }

  console.log(`══ relocate-uncategorized ══`);
  console.log(`  planned moves:       ${moves.length}`);
  console.log(`  collisions:          ${collisions.length}`);
  console.log(`  skipped (no domain/grade): ${skippedNoMeta.length}`);
  if (collisions.length) {
    console.log(`\nCollisions (manual resolution needed):`);
    for (const c of collisions) console.log(`    ${c.file} ← target ${c.dstAbs} already exists`);
  }
  if (skippedNoMeta.length) {
    console.log(`\nSkipped (missing frontmatter):`);
    for (const f of skippedNoMeta) console.log(`    ${f}`);
  }

  console.log(`\nSample moves (first 5):`);
  for (const m of moves.slice(0, 5)) {
    console.log(`  ${m.srcRel} → ${m.dstRel}`);
  }
  if (moves.length > 5) console.log(`  ... and ${moves.length - 5} more.`);

  // ---- Phase 2: build the reference replacement table ----
  // Each move generates a single old→new prefix swap. We do prefix
  // replacement, so `docs/concepts/uncategorized/foo.md` and
  // `docs/concepts/uncategorized/foo` (no extension) both get caught.
  const replacements = []; // { from, to }
  for (const m of moves) {
    replacements.push([
      `docs/concepts/${m.oldId}.md`,
      `docs/concepts/${m.newId}.md`,
    ]);
    replacements.push([
      `docs/concepts/${m.oldId}`,
      `docs/concepts/${m.newId}`,
    ]);
  }
  // Stale flat-path prereqs in the orphan files themselves.
  for (const [from, to] of STALE_FLAT_REPLACEMENTS) {
    replacements.push([from, to]);
  }

  // ---- Phase 3: scan all .md under docs/ for replacement candidates ----
  const allMd = walkMd(DOCS_DIR);
  const affected = []; // { path, hits }
  for (const p of allMd) {
    const text = readFileSync(p, 'utf-8');
    let hits = 0;
    for (const [from] of replacements) {
      if (text.includes(from)) hits += (text.split(from).length - 1);
    }
    if (hits > 0) affected.push({ path: p, hits });
  }
  console.log(`\nAffected files (with refs to update): ${affected.length}`);
  let totalHits = 0;
  for (const a of affected) totalHits += a.hits;
  console.log(`Total reference swaps: ${totalHits}`);
  if (affected.length) {
    const byDir = {};
    for (const a of affected) {
      const d = relative(DOCS_DIR, a.path).split('/')[0];
      byDir[d] = (byDir[d] ?? 0) + 1;
    }
    console.log(`  by top-level dir under docs/:`);
    for (const [d, n] of Object.entries(byDir)) console.log(`    ${d}/ — ${n} files`);
  }

  if (!write) {
    console.log(`\n(dry-run; pass --write to perform ${moves.length} git moves and ${totalHits} ref swaps)`);
    if (collisions.length || skippedNoMeta.length) {
      console.log(`\nNOTE: collisions / skipped files must be resolved manually before --write.`);
    }
    return;
  }

  if (collisions.length || skippedNoMeta.length) {
    console.error(`\nAborting: ${collisions.length} collision(s), ${skippedNoMeta.length} skipped. Resolve and re-run.`);
    process.exit(1);
  }

  // ---- Phase 4: execute. git mv, then per-file ref replacement. ----
  console.log(`\nMoving files via git mv...`);
  for (const m of moves) {
    const dstDir = dirname(m.dstAbs);
    if (!existsSync(dstDir)) mkdirSync(dstDir, { recursive: true });
    execSync(`git mv ${quote(m.srcRel)} ${quote(m.dstRel)}`, { cwd: REPO_ROOT });
  }

  console.log(`Rewriting ${affected.length} files with ${totalHits} ref swaps...`);
  // Re-walk in case git mv reshuffled paths.
  for (const p of walkMd(DOCS_DIR)) {
    let text = readFileSync(p, 'utf-8');
    let changed = false;
    for (const [from, to] of replacements) {
      if (text.includes(from)) { text = text.split(from).join(to); changed = true; }
    }
    if (changed) writeFileSync(p, text, 'utf-8');
  }
  console.log(`Done.`);
}

// Shell-escape: file paths contain Korean / spaces.
function quote(s) {
  return "'" + s.replace(/'/g, `'\\''`) + "'";
}

main();
