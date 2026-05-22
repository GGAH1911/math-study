#!/usr/bin/env node
// LWIP entropy audit — Shutdown gate 기준 체크.
//
// 측정:
//   - flat dirs: 단일 level 에 50+ md (sub-dir 정리 필요)
//   - congested hubs: hub md 가 100+ link
//   - isolated concepts: 어떤 hub / cross-ref 에서도 가리키지 않는 concept md
//   - missing fm: required field 누락 concept/problem
//
// 출력: count entropy + 샘플 목록 (CI/log 친화)

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const ROOT = path.join(REPO_ROOT, 'docs');
const OUT_FILE = path.join(REPO_ROOT, 'web', 'src', 'data', 'lwip-audit.json');

function walkMd(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walkMd(p, out);
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function dirMdCount(dir) {
  if (!existsSync(dir)) return 0;
  return readdirSync(dir).filter((f) => f.endsWith('.md')).length;
}

// === thresholds ===
// FLAT/CONGESTED_WARN: 정보용 (size 가 큰 도메인은 자연). entropy 에 포함 X.
// FLAT/CONGESTED_HARD: 진짜 navigation 불가 — entropy++.
const FLAT_THRESHOLD = 50;            // warn
const FLAT_HARD_THRESHOLD = 1500;     // hard fail
const CONGESTED_THRESHOLD = 100;      // warn
const CONGESTED_HARD_THRESHOLD = 2000; // hard fail

// === 1. flat dirs ===
const flatDirs = [];
function checkFlat(dir, rel) {
  if (!existsSync(dir)) return;
  const c = dirMdCount(dir);
  if (c >= FLAT_THRESHOLD) flatDirs.push({ rel, count: c });
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) checkFlat(path.join(dir, e.name), `${rel}/${e.name}`);
  }
}
checkFlat(path.join(ROOT, 'concepts'), 'docs/concepts');
checkFlat(path.join(ROOT, 'problems'), 'docs/problems');
checkFlat(path.join(ROOT, 'hubs'), 'docs/hubs');
checkFlat(path.join(ROOT, 'syntheses'), 'docs/syntheses');
checkFlat(path.join(ROOT, 'mistakes'), 'docs/mistakes');

// === 2. congested hubs ===
const congestedHubs = [];
for (const p of walkMd(path.join(ROOT, 'hubs'))) {
  const raw = readFileSync(p, 'utf8');
  // count markdown links `](...)` — rough proxy
  const links = (raw.match(/\]\(/g) || []).length;
  if (links >= CONGESTED_THRESHOLD) {
    congestedHubs.push({ path: path.relative(ROOT, p), links });
  }
}

// === 3. isolated concepts ===
const conceptFiles = walkMd(path.join(ROOT, 'concepts'));
const conceptSlugs = new Set(
  conceptFiles.map((p) => path.relative(path.join(ROOT, 'concepts'), p).replace(/\.md$/, '').split(/[\\/]/).join('/'))
);
// scan all md (concepts + problems + hubs + syntheses + mistakes) for references
const referencedSlugs = new Set();
// slug 에는 한국어/영문/숫자/`_-` 외에 그리스 (θ, π, …) + 일부 기호 (·, ,) 가 등장.
// 가능한 한 너그럽게 — 화이트리스트로 깨진 char 만 차단.
const SLUG_CHARS = '[^\\s)\\]"`<>(]+';
const refRe = new RegExp(`docs/concepts/(${SLUG_CHARS})\\.md`, 'g');
const refMdRe = new RegExp(`\\.\\.\\/(?:\\.\\.\\/)*concepts\\/(${SLUG_CHARS})\\.md`, 'g');
const allMd = [
  ...conceptFiles,
  ...walkMd(path.join(ROOT, 'problems')),
  ...walkMd(path.join(ROOT, 'hubs')),
  ...walkMd(path.join(ROOT, 'syntheses')),
  ...walkMd(path.join(ROOT, 'mistakes')),
];
for (const p of allMd) {
  const raw = readFileSync(p, 'utf8');
  let m;
  while ((m = refRe.exec(raw))) referencedSlugs.add(m[1]);
  refMdRe.lastIndex = 0;
  while ((m = refMdRe.exec(raw))) referencedSlugs.add(m[1]);
}
const isolatedConcepts = [...conceptSlugs].filter((s) => !referencedSlugs.has(s));

// === 4. missing fm ===
const missingFm = [];
for (const p of conceptFiles) {
  const fm = matter(readFileSync(p, 'utf8')).data;
  if (!fm.concept_type) missingFm.push({ kind: 'concept', path: path.relative(ROOT, p), missing: 'concept_type' });
  if (!fm.mastery) missingFm.push({ kind: 'concept', path: path.relative(ROOT, p), missing: 'mastery' });
}
for (const p of walkMd(path.join(ROOT, 'problems'))) {
  const fm = matter(readFileSync(p, 'utf8')).data;
  if (!fm.source) missingFm.push({ kind: 'problem', path: path.relative(ROOT, p), missing: 'source' });
  if (!fm.status) missingFm.push({ kind: 'problem', path: path.relative(ROOT, p), missing: 'status' });
}

// === Report ===
const flatHard = flatDirs.filter((d) => d.count >= FLAT_HARD_THRESHOLD);
const congestedHard = congestedHubs.filter((h) => h.links >= CONGESTED_HARD_THRESHOLD);
const entropy = flatHard.length + congestedHard.length
  + (isolatedConcepts.length > 0 ? isolatedConcepts.length : 0)
  + (missingFm.length > 0 ? missingFm.length : 0);

console.log('=== LWIP entropy audit ===');
console.log(`flat dirs (>=${FLAT_THRESHOLD} md, warn / >=${FLAT_HARD_THRESHOLD} hard): ${flatDirs.length} warn, ${flatHard.length} hard`);
for (const d of flatDirs.slice(0, 10)) console.log(`  ${d.rel.padEnd(40)} ${d.count}${d.count >= FLAT_HARD_THRESHOLD ? ' (HARD)' : ''}`);

console.log(`congested hubs (>=${CONGESTED_THRESHOLD} links, warn / >=${CONGESTED_HARD_THRESHOLD} hard): ${congestedHubs.length} warn, ${congestedHard.length} hard`);
for (const h of congestedHubs.slice(0, 10)) console.log(`  ${h.path.padEnd(50)} ${h.links}${h.links >= CONGESTED_HARD_THRESHOLD ? ' (HARD)' : ''}`);

console.log(`isolated concepts: ${isolatedConcepts.length}`);
for (const s of isolatedConcepts.slice(0, 10)) console.log(`  ${s}`);
if (isolatedConcepts.length > 10) console.log(`  ... and ${isolatedConcepts.length - 10} more`);

console.log(`missing frontmatter: ${missingFm.length}`);
for (const m of missingFm.slice(0, 10)) console.log(`  ${m.path.padEnd(50)} (${m.missing})`);

console.log(`\n=== entropy: ${entropy} ===`);
console.log(`  isolated:        ${isolatedConcepts.length}`);
console.log(`  missing fm:      ${missingFm.length}`);
console.log(`  flat hard:       ${flatHard.length}`);
console.log(`  congested hard:  ${congestedHard.length}`);

// emit JSON for dashboard (file + stdout)
const auditJson = JSON.stringify({
  generatedAt: new Date().toISOString(),
  entropy,
  thresholds: {
    flatWarn: FLAT_THRESHOLD, flatHard: FLAT_HARD_THRESHOLD,
    congestedWarn: CONGESTED_THRESHOLD, congestedHard: CONGESTED_HARD_THRESHOLD,
  },
  flatDirs, flatHardCount: flatHard.length,
  congestedHubs, congestedHardCount: congestedHard.length,
  isolatedConceptCount: isolatedConcepts.length,
  isolatedConcepts: isolatedConcepts.slice(0, 50),
  missingFmCount: missingFm.length,
  missingFm: missingFm.slice(0, 50),
}, null, 2);

mkdirSync(path.dirname(OUT_FILE), { recursive: true });
writeFileSync(OUT_FILE, auditJson);
console.log(`\n[lwip-audit] wrote ${path.relative(REPO_ROOT, OUT_FILE)}`);

if (entropy > 0) process.exit(0); // non-blocking — dashboard renders
