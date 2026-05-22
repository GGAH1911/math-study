#!/usr/bin/env node
// Phase A2 (level-2): docs/concepts/<domain>/*.md → docs/concepts/<domain>/<grade>/*.md
//
// grade 필드를 영문 slug 로 매핑해 추가 sub-dir 생성. uncategorized 는 grade 가
// 없어 그대로 둠. cross-ref (concept frontmatter, problem frontmatter, 본문 markdown
// 링크) 전수 패치.
//
//   node web/scripts/restructure-concepts-l2.mjs            # dry-run
//   node web/scripts/restructure-concepts-l2.mjs --apply

import { readdirSync, readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const ROOT = path.join(REPO_ROOT, 'docs');
const CONCEPTS_DIR = path.join(ROOT, 'concepts');
const APPLY = process.argv.includes('--apply');

// 영문 slug — URL-safe. 도메인명과 충돌하지 않게.
const GRADE_MAP = {
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
const MISC = '_misc';

// 도메인 sub-dir 중 grade-aware 처리할 것 (uncategorized 제외)
const DOMAINS = ['functions', 'geometry', 'probability-stats', 'algebra', 'equations', 'logic'];

function gradeSlug(grade) {
  if (!grade) return MISC;
  return GRADE_MAP[grade] ?? MISC;
}

const mapping = []; // { domain, slug, oldRel, newRel, gradeDir }
const statsPerDomain = {}; // domain → { gradeDir: count }

for (const domain of DOMAINS) {
  const dir = path.join(CONCEPTS_DIR, domain);
  if (!existsSync(dir)) continue;
  for (const f of readdirSync(dir, { withFileTypes: true })) {
    if (!f.isFile() || !f.name.endsWith('.md')) continue;
    const abs = path.join(dir, f.name);
    const fm = matter(readFileSync(abs, 'utf8')).data;
    const gradeDir = gradeSlug(fm.grade);
    const slug = f.name.replace(/\.md$/, '');
    const newAbs = path.join(dir, gradeDir, f.name);
    mapping.push({
      domain, slug, gradeDir,
      oldRel: path.relative(REPO_ROOT, abs),
      newRel: path.relative(REPO_ROOT, newAbs),
    });
    (statsPerDomain[domain] ??= {})[gradeDir] = (statsPerDomain[domain]?.[gradeDir] ?? 0) + 1;
  }
}

console.log('=== Stats ===');
for (const d of DOMAINS) {
  const s = statsPerDomain[d] ?? {};
  const total = Object.values(s).reduce((a, b) => a + b, 0);
  console.log(`  ${d} (${total})`);
  for (const [k, c] of Object.entries(s).sort((a, b) => b[1] - a[1])) {
    console.log(`    ${k.padEnd(22)} ${c}`);
  }
}

// === cross-ref replace map ===
const pathReplaceMap = new Map();
for (const m of mapping) {
  const oldFwd = `docs/concepts/${m.domain}/${m.slug}.md`;
  const newFwd = `docs/concepts/${m.domain}/${m.gradeDir}/${m.slug}.md`;
  pathReplaceMap.set(oldFwd, newFwd);
}
console.log(`\nTotal moves: ${mapping.length}, distinct cross-ref keys: ${pathReplaceMap.size}`);

// === scan for ref hits ===
function walkMd(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walkMd(p, out);
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

if (!APPLY) {
  console.log('\n[dry-run] --apply 추가 시 실제 이동 + cross-ref patch.');
  process.exit(0);
}

console.log('\n=== APPLY ===');
// 1. mkdir grade sub-dirs
const dirsNeeded = new Set(mapping.map((m) => path.dirname(path.join(REPO_ROOT, m.newRel))));
for (const d of dirsNeeded) mkdirSync(d, { recursive: true });

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

// 3. patch cross-refs (frontmatter + markdown body)
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

let patched = 0;
const all = [
  ...walkMd(path.join(ROOT, 'concepts')),
  ...walkMd(path.join(ROOT, 'problems')),
  ...walkMd(path.join(ROOT, 'syntheses')),
  ...walkMd(path.join(ROOT, 'mistakes')),
  ...walkMd(path.join(ROOT, 'hubs')),
];
for (const p of all) if (patchFile(p)) patched++;
console.log(`  patched ${patched} files (frontmatter cross-refs)`);

// 4. body markdown links: `../concepts/<domain>/<leaf>.md` → `../concepts/<domain>/<grade>/<leaf>.md`
// 추가로 일부 syntheses 가 `../concepts/<leaf>` 같은 path 일 수도 있어서 leaf-only 도 매핑.
const leafToFull = new Map(); // 'functions/leaf' → 'functions/grade/leaf'
for (const m of mapping) {
  leafToFull.set(`${m.domain}/${m.slug}`, `${m.domain}/${m.gradeDir}/${m.slug}`);
}

let mdLinksPatched = 0;
for (const p of all) {
  let raw = readFileSync(p, 'utf8');
  const orig = raw;
  // `../concepts/<domain>/<leaf>.md` form
  raw = raw.replace(/\.\.\/concepts\/([a-z-]+)\/([^/)\s"]+)\.md/g, (m0, dom, leaf) => {
    const full = leafToFull.get(`${dom}/${leaf}`);
    return full ? `../concepts/${full}.md` : m0;
  });
  // `/concepts/<domain>/<leaf>` form (wiki link inside parens)
  raw = raw.replace(/\(\/concepts\/([a-z-]+)\/([^/)\s"]+)\)/g, (m0, dom, leaf) => {
    const full = leafToFull.get(`${dom}/${leaf}`);
    return full ? `(/concepts/${full})` : m0;
  });
  if (raw !== orig) {
    writeFileSync(p, raw);
    mdLinksPatched++;
  }
}
console.log(`  body markdown link patches: ${mdLinksPatched}`);

console.log('\n=== APPLY 완료 ===');
