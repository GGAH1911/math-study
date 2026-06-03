#!/usr/bin/env node
/**
 * Force `domain:` frontmatter to match the file's location on disk.
 *
 * The concept tree is laid out as
 *   docs/concepts/<domain_en>/<grade>/<unit>/<spoke>.md
 * so the first path segment is the authoritative domain. Some spokes
 * carry a stale `domain:` (e.g. a 삼각함수 spoke under functions/ tagged
 * `도형`) — a leftover from the uncategorized/ relocation + keyword
 * backfill. Those land in the wrong domain section on /concepts and fall
 * into the per-domain "기타 (단원 미연결)" bucket because their home unit
 * lives in a different section.
 *
 * Unlike backfill-concept-domain.mjs (which only fills a MISSING domain),
 * this OVERWRITES any domain that disagrees with the path. Path wins.
 *
 * Default is dry-run. Pass `--write` to actually edit the .md files.
 *
 * Usage:
 *   node web/scripts/fix-domain-by-path.mjs            # preview
 *   node web/scripts/fix-domain-by-path.mjs --write    # apply
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const DOCS_DIR = join(REPO_ROOT, 'docs', 'concepts');

// First path segment (English dir) → 한글 domain used in frontmatter.
const EN2KO = {
  algebra: '수와식',
  equations: '방정식',
  functions: '함수',
  geometry: '도형',
  logic: '논리',
  'probability-stats': '확률통계',
};

function walkMd(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...walkMd(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function idFromFile(absPath) {
  return relative(DOCS_DIR, absPath).replace(/\.md$/, '').split(/[\\/]/).join('/');
}

function currentDomain(text) {
  const m = text.match(/^domain:\s*(.*)$/m);
  return m ? m[1].trim() : null;
}

function setDomainInFrontmatter(text, domain) {
  const existing = text.match(/^domain:\s*.*$/m);
  if (existing) return text.replace(/^domain:\s*.*$/m, `domain: ${domain}`);
  const ctMatch = text.match(/^concept_type:.*$/m);
  if (ctMatch) return text.replace(/^(concept_type:.*)$/m, `$1\ndomain: ${domain}`);
  return text.replace(/^---\n/, `---\ndomain: ${domain}\n`);
}

function main() {
  const write = process.argv.includes('--write');
  const planned = []; // { id, from, to, mdPath }
  let ok = 0, unknownDir = 0;
  const byChange = new Map();

  for (const mdPath of walkMd(DOCS_DIR)) {
    const id = idFromFile(mdPath);
    const dirEn = id.split('/')[0];
    const expected = EN2KO[dirEn];
    if (!expected) { unknownDir++; continue; }
    const text = readFileSync(mdPath, 'utf-8');
    const have = currentDomain(text);
    if (have === expected) { ok++; continue; }
    planned.push({ id, from: have, to: expected, mdPath });
    const key = `${have} → ${expected}`;
    byChange.set(key, (byChange.get(key) ?? 0) + 1);
  }

  console.log(`══ fix-domain-by-path ══`);
  console.log(`  already correct:     ${ok}`);
  console.log(`  to fix:              ${planned.length}`);
  console.log(`  unknown top dir:     ${unknownDir}`);
  if (byChange.size) {
    console.log(`\n변경 분포:`);
    for (const [k, n] of [...byChange.entries()].sort((a, b) => b[1] - a[1])) {
      console.log(`  ${String(n).padStart(3)}개:  ${k}`);
    }
  }
  console.log(`\n변경 대상 (전체):`);
  for (const p of planned) console.log(`  ${String(p.from).padEnd(8)} → ${p.to.padEnd(6)}  ${p.id}`);

  if (!write) {
    console.log(`\n(dry-run; --write 로 ${planned.length}개 적용)`);
    return;
  }
  console.log(`\nWriting ${planned.length} files...`);
  for (const p of planned) {
    const text = readFileSync(p.mdPath, 'utf-8');
    const updated = setDomainInFrontmatter(text, p.to);
    if (updated !== text) writeFileSync(p.mdPath, updated, 'utf-8');
  }
  console.log(`Done.`);
}

main();
