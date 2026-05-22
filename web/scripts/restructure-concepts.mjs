#!/usr/bin/env node
// Phase A: concepts/ flat → sub-dir (domain 기반)
//
// 사용:
//   node web/scripts/restructure-concepts.mjs           # dry-run (이동 계획 + 통계 출력만)
//   node web/scripts/restructure-concepts.mjs --apply   # 실제 git mv + frontmatter cross-ref update
//
// 영향 받는 collection (frontmatter path update):
//   - docs/concepts/*.md: prerequisites, enables
//   - docs/problems/*.md: concepts
//   - docs/syntheses/*.md: origin_concept
//   - (docs/mistakes 의 problem 은 problems 의 path 라 Phase A 영향 X)

import { readdirSync, readFileSync, writeFileSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import path from 'node:path';
import matter from 'gray-matter';

const ROOT = path.resolve('docs');
const CONCEPTS_DIR = path.join(ROOT, 'concepts');
const PROBLEMS_DIR = path.join(ROOT, 'problems');
const SYNTHESES_DIR = path.join(ROOT, 'syntheses');
const APPLY = process.argv.includes('--apply');

// domain → sub-dir (영문 slug, URL-safe). 미분류는 uncategorized.
const DOMAIN_MAP = {
  '함수': 'functions',
  '도형': 'geometry',
  '확률통계': 'probability-stats',
  '수와식': 'algebra',
  '방정식': 'equations',
  '논리': 'logic',
};
const UNCATEGORIZED = 'uncategorized';

function walk(dir) {
  if (!existsSync(dir)) return [];
  const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function classify(domain) {
  if (!domain) return UNCATEGORIZED;
  return DOMAIN_MAP[domain] ?? UNCATEGORIZED;
}

// === Step 1: 모든 concept 파일 분석 + 매핑 산출 ===
const conceptFiles = walk(CONCEPTS_DIR);
// flat 인 거만 대상 (이미 sub-dir 안에 있으면 skip — idempotent)
const flatConcepts = conceptFiles.filter((p) => path.dirname(p) === CONCEPTS_DIR);

const mapping = []; // { oldPath, newPath, oldRel, newRel, slug, domain, subdir }
const stats = {}; // subdir → count

for (const oldPath of flatConcepts) {
  const raw = readFileSync(oldPath, 'utf8');
  const { data } = matter(raw);
  const slug = path.basename(oldPath, '.md');
  const subdir = classify(data.domain);
  const newPath = path.join(CONCEPTS_DIR, subdir, slug + '.md');
  const oldRel = path.relative(process.cwd(), oldPath);
  const newRel = path.relative(process.cwd(), newPath);
  mapping.push({ oldPath, newPath, oldRel, newRel, slug, domain: data.domain ?? null, subdir });
  stats[subdir] = (stats[subdir] ?? 0) + 1;
}

console.log('=== 분류 통계 ===');
for (const [s, c] of Object.entries(stats).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${s.padEnd(20)} ${c}`);
}
console.log(`  total: ${mapping.length}`);

console.log('\n=== uncategorized list (도메인 누락 또는 매핑 외 값) ===');
const uncat = mapping.filter((m) => m.subdir === UNCATEGORIZED);
for (const m of uncat.slice(0, 30)) {
  console.log(`  ${m.slug.padEnd(40)} domain=${m.domain ?? '(none)'}`);
}
if (uncat.length > 30) console.log(`  ... and ${uncat.length - 30} more`);

// === Step 2: cross-ref path update 영향 인벤토리 ===
// 매핑 된 path 변화: oldRel = 'docs/concepts/<slug>.md' → newRel = 'docs/concepts/<subdir>/<slug>.md'
const pathReplaceMap = new Map(); // oldRelFwd → newRelFwd
for (const m of mapping) {
  // git mv 후의 정규화된 forward-slash path (cross-ref 는 항상 forward-slash)
  const oldRelFwd = `docs/concepts/${m.slug}.md`;
  const newRelFwd = `docs/concepts/${m.subdir}/${m.slug}.md`;
  if (oldRelFwd !== newRelFwd) pathReplaceMap.set(oldRelFwd, newRelFwd);
}

console.log(`\n=== 영향 받는 cross-ref path 개수: ${pathReplaceMap.size} ===`);

// concept md 안의 prerequisites/enables 카운트
let conceptRefCount = 0;
for (const p of conceptFiles) {
  const raw = readFileSync(p, 'utf8');
  for (const old of pathReplaceMap.keys()) {
    if (raw.includes(old)) conceptRefCount++;
  }
}
console.log(`  concept md 안 prerequisites/enables 참조: ${conceptRefCount}`);

// problem md 안의 concepts: 카운트
let problemRefCount = 0;
const problemFiles = walk(PROBLEMS_DIR);
for (const p of problemFiles) {
  const raw = readFileSync(p, 'utf8');
  for (const old of pathReplaceMap.keys()) {
    if (raw.includes(old)) problemRefCount++;
  }
}
console.log(`  problem md 안 concepts: 참조: ${problemRefCount} (problem 파일 ${problemFiles.length} 중)`);

// syntheses
let synthRefCount = 0;
const synthFiles = walk(SYNTHESES_DIR);
for (const p of synthFiles) {
  const raw = readFileSync(p, 'utf8');
  for (const old of pathReplaceMap.keys()) {
    if (raw.includes(old)) synthRefCount++;
  }
}
console.log(`  syntheses md 안 origin_concept 참조: ${synthRefCount} (syntheses 파일 ${synthFiles.length} 중)`);

if (!APPLY) {
  console.log('\n[dry-run] --apply 추가 시 실제 git mv + frontmatter regex update 수행.');
  process.exit(0);
}

// === Step 3: APPLY mode — git mv + frontmatter cross-ref update ===
console.log('\n=== APPLY mode 시작 ===');

// 3.1 mkdir sub-dirs
const subdirsNeeded = new Set(mapping.map((m) => m.subdir));
for (const sd of subdirsNeeded) {
  const dirPath = path.join(CONCEPTS_DIR, sd);
  if (!existsSync(dirPath)) {
    mkdirSync(dirPath, { recursive: true });
    console.log(`  mkdir ${path.relative(process.cwd(), dirPath)}`);
  }
}

// 3.2 git mv each concept
let movedCnt = 0;
for (const m of mapping) {
  try {
    execSync(`git mv "${m.oldRel}" "${m.newRel}"`, { stdio: 'pipe' });
    movedCnt++;
  } catch (e) {
    console.error(`  fail: ${m.oldRel} → ${m.newRel} — ${e.message.split('\n')[0]}`);
  }
}
console.log(`  moved ${movedCnt}/${mapping.length} concept files`);

// 3.3 모든 collection 의 cross-ref path update
function patchFile(p) {
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

let patchedConcepts = 0, patchedProblems = 0, patchedSyntheses = 0;
// concepts (자기 자신의 prerequisites/enables — 이동 후 새 path 안의 파일들)
for (const m of mapping) {
  if (patchFile(m.newPath)) patchedConcepts++;
}
// problems (concepts: field)
for (const p of problemFiles) {
  if (patchFile(p)) patchedProblems++;
}
// syntheses (origin_concept)
for (const p of synthFiles) {
  if (patchFile(p)) patchedSyntheses++;
}
console.log(`  patched: ${patchedConcepts} concepts + ${patchedProblems} problems + ${patchedSyntheses} syntheses`);

console.log('\n=== APPLY 완료 ===');
console.log('다음: A3 (web 코드 update) → A4 (hub 재작성) → A5 (검증)');
