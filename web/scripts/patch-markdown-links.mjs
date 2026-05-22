#!/usr/bin/env node
// problem/synthesis/mistake 본문의 markdown link `../concepts/<slug>.md` →
// `../concepts/<domain>/<slug>.md` 자동 업데이트.
// restructure-concepts.mjs 가 frontmatter 만 patch 했으므로 본문 link 는 따로.

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('docs');
const CONCEPTS_DIR = path.join(ROOT, 'concepts');

// concept slug (sub-dir 포함, e.g. 'algebra/근의_공식') → full new path 'algebra/근의_공식'
// 기존 flat slug 'algebra' 매핑 만들기 위해 leaf-only key 도 함께.
function walkConcepts() {
  const out = new Map(); // leaf → 'subdir/leaf'
  for (const sd of readdirSync(CONCEPTS_DIR, { withFileTypes: true })) {
    if (!sd.isDirectory()) continue;
    const dir = path.join(CONCEPTS_DIR, sd.name);
    for (const f of readdirSync(dir)) {
      if (!f.endsWith('.md')) continue;
      const leaf = f.replace(/\.md$/, '');
      out.set(leaf, `${sd.name}/${leaf}`);
    }
  }
  return out;
}

const leafToPath = walkConcepts();

function walkMd(dir, list = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walkMd(p, list);
    else if (e.name.endsWith('.md')) list.push(p);
  }
  return list;
}

const targets = [
  ...walkMd(path.join(ROOT, 'problems')),
  ...walkMd(path.join(ROOT, 'syntheses')),
  existsSync(path.join(ROOT, 'mistakes')) ? walkMd(path.join(ROOT, 'mistakes')) : [],
].flat();

let patched = 0, refsFixed = 0;
for (const p of targets) {
  let raw = readFileSync(p, 'utf8');
  const orig = raw;
  // `../concepts/<leaf>.md` form (markdown link in body)
  raw = raw.replace(/\.\.\/concepts\/([가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_-]+)\.md/g, (m, leaf) => {
    const np = leafToPath.get(leaf);
    if (!np) return m;
    refsFixed++;
    return `../concepts/${np}.md`;
  });
  // `(/concepts/<leaf>)` form (wiki link with absolute path)
  raw = raw.replace(/\(\/concepts\/([가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_-]+)\)/g, (m, leaf) => {
    const np = leafToPath.get(leaf);
    if (!np) return m;
    refsFixed++;
    return `(/concepts/${np})`;
  });
  if (raw !== orig) {
    writeFileSync(p, raw);
    patched++;
  }
}

console.log(`patched ${patched} files, ${refsFixed} link references updated`);
