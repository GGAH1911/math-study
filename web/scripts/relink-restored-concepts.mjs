#!/usr/bin/env node
/**
 * 새로 생성된 concept .md (이전엔 누락이라 alias로 다른 concept으로 redirect
 * 된 problem들이 있는) 에 대해 problem.concepts 를 정정.
 *
 * problem 의 frontmatter `unit:` 가 새 concept slug 와 일치하면 그 concept을
 * concepts: 의 첫 번째 entry로 prepend (이미 있으면 skip).
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const PROBLEMS_DIR = join(REPO_ROOT, 'docs', 'problems');

const APPLY = process.argv.includes('--apply');

// 새로 만든 concept slug 목록 (확장 가능).
const RESTORED = ['함수의_극한과_연속성', '도함수의_활용'];

let touched = 0;
const samples = [];
for (const fname of readdirSync(PROBLEMS_DIR).filter((f) => f.endsWith('.md'))) {
  const file = join(PROBLEMS_DIR, fname);
  const raw = readFileSync(file, 'utf-8');
  const { data: fm, content } = matter(raw);
  const unitSlug = String(fm.unit ?? '').replace(/\s+/g, '_');
  if (!RESTORED.includes(unitSlug)) continue;
  const conceptPath = `docs/concepts/${unitSlug}.md`;
  const existing = Array.isArray(fm.concepts) ? fm.concepts : [];
  if (existing.some((p) => basename(String(p), '.md') === unitSlug)) continue; // already linked
  const next = [conceptPath, ...existing];
  touched++;
  if (samples.length < 10) samples.push({ file: file.replace(REPO_ROOT + '/', ''), unit: unitSlug, after: next });
  if (APPLY) {
    fm.concepts = next;
    const newFm = matter.stringify(content, fm);
    const inline = next.join(', ');
    const patched = newFm.replace(/^concepts:[\s\S]*?(?=\n[A-Za-z_]|---)/m, `concepts: [${inline}]\n`);
    writeFileSync(file, patched, 'utf-8');
  }
}

console.log(`\n=== relink-restored-concepts (${APPLY ? 'APPLY' : 'DRY-RUN'}) ===`);
console.log(`정정 대상: ${touched} problem`);
for (const s of samples) {
  console.log(`  ${s.file}  unit=${s.unit}`);
  console.log(`    after: ${JSON.stringify(s.after.slice(0, 4))}${s.after.length > 4 ? ' …' : ''}`);
}
