#!/usr/bin/env node
// Phase B: problems/ flat → <year>/<round_label>/
//
//   node web/scripts/restructure-problems.mjs           # dry-run
//   node web/scripts/restructure-problems.mjs --apply   # 실제 git mv + cross-ref patch
//
// slug 패턴: `<year>_<round_parts>_<subject>_<number>`
//   subject ∈ {공통, 기하, 미적분, 확률과통계, 단일}
//   round_label = <year>_<round_parts> (예: '2025_수능', '2025_고3_3월모의고사', '2024_고졸_1회_단일')
//   target dir = docs/problems/<year>/<round_label_without_year>/
//
// 영향 받는 path-bearing 필드:
//   - docs/mistakes/*.md `problem: docs/problems/<slug>.md`
//   - (problem md 의 frontmatter `concepts:` 는 Phase A 에서 처리됨, 영향 X)

import { readdirSync, readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import path from 'node:path';

const ROOT = path.resolve('docs');
const PROBLEMS_DIR = path.join(ROOT, 'problems');
const MISTAKES_DIR = path.join(ROOT, 'mistakes');
const APPLY = process.argv.includes('--apply');

const SUBJECT = '(?:공통|기하|미적분|확률과통계|단일)';
const SLUG_RE = new RegExp(`^(\\d{4})_(.+)_${SUBJECT}_\\d+$`);

function listFlatProblems() {
  return readdirSync(PROBLEMS_DIR, { withFileTypes: true })
    .filter((e) => e.isFile() && e.name.endsWith('.md'))
    .map((e) => e.name);
}

const mapping = []; // { fname, slug, year, round, targetDir, oldRel, newRel }
const skipped = [];
const stats = {};

for (const fname of listFlatProblems()) {
  const slug = fname.replace(/\.md$/, '');
  const m = slug.match(SLUG_RE);
  if (!m) {
    skipped.push(slug);
    continue;
  }
  const [, year, roundParts] = m;
  // roundParts 안에 한국어 round descriptor (예: '수능', '고3_3월모의고사', '고졸_1회_단일')
  const targetDir = path.join(PROBLEMS_DIR, year, roundParts);
  const oldRel = path.relative(process.cwd(), path.join(PROBLEMS_DIR, fname));
  const newRel = path.relative(process.cwd(), path.join(targetDir, fname));
  mapping.push({ fname, slug, year, round: roundParts, targetDir, oldRel, newRel });
  const k = `${year}/${roundParts}`;
  stats[k] = (stats[k] ?? 0) + 1;
}

console.log('=== Round distribution ===');
const top = Object.entries(stats).sort((a, b) => a[0].localeCompare(b[0]));
for (const [k, c] of top.slice(0, 20)) console.log(`  ${k.padEnd(40)} ${c}`);
if (top.length > 20) console.log(`  ...${top.length - 20} more rounds`);
console.log(`  total mappings: ${mapping.length} (skipped non-standard: ${skipped.length})`);
if (skipped.length) {
  console.log('\nSkipped (non-standard slug):');
  for (const s of skipped.slice(0, 10)) console.log(`  ${s}`);
}

// === path replace map: 'docs/problems/<slug>.md' → 'docs/problems/<year>/<round>/<slug>.md'
const pathReplaceMap = new Map();
for (const m of mapping) {
  const oldFwd = `docs/problems/${m.slug}.md`;
  const newFwd = `docs/problems/${m.year}/${m.round}/${m.slug}.md`;
  pathReplaceMap.set(oldFwd, newFwd);
}

// === count cross-ref hits (mistakes is the main consumer)
let mistakeRefCount = 0;
if (existsSync(MISTAKES_DIR)) {
  for (const f of readdirSync(MISTAKES_DIR)) {
    if (!f.endsWith('.md')) continue;
    const raw = readFileSync(path.join(MISTAKES_DIR, f), 'utf8');
    for (const old of pathReplaceMap.keys()) if (raw.includes(old)) mistakeRefCount++;
  }
}
console.log(`\nmistakes md 안 problem path 참조: ${mistakeRefCount}`);

if (!APPLY) {
  console.log('\n[dry-run] --apply 추가 시 실제 git mv + cross-ref patch.');
  process.exit(0);
}

console.log('\n=== APPLY mode ===');
// 1. mkdir all target dirs
const dirsToMake = new Set(mapping.map((m) => m.targetDir));
for (const d of dirsToMake) mkdirSync(d, { recursive: true });

// 2. git mv each
let moved = 0;
for (const m of mapping) {
  try {
    execSync(`git mv "${m.oldRel}" "${m.newRel}"`, { stdio: 'pipe' });
    moved++;
  } catch (e) {
    console.error(`  fail: ${m.oldRel} — ${e.message.split('\n')[0]}`);
  }
}
console.log(`  moved ${moved}/${mapping.length}`);

// 3. patch cross-refs (mistakes / syntheses / hubs)
function patch(p) {
  let raw = readFileSync(p, 'utf8');
  let changed = false;
  for (const [old, neu] of pathReplaceMap.entries()) {
    if (raw.includes(old)) {
      raw = raw.replaceAll(old, neu);
      changed = true;
    }
  }
  if (changed) writeFileSync(p, raw);
  return changed;
}

let patched = 0;
function patchTree(dir) {
  if (!existsSync(dir)) return;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) patchTree(p);
    else if (e.name.endsWith('.md') && patch(p)) patched++;
  }
}
patchTree(MISTAKES_DIR);
patchTree(path.join(ROOT, 'syntheses'));
patchTree(path.join(ROOT, 'hubs'));
console.log(`  patched ${patched} cross-ref files`);

console.log('\n=== APPLY 완료 ===');
console.log('다음: web 코드 update (problems route) → hub 재작성 → 검증');
