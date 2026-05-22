#!/usr/bin/env node
// Phase A4: concepts/ sub-dir 기반 hub 자동 재생성
//   - docs/hubs/concepts.md (overview + sub-hub link)
//   - docs/hubs/concepts/<domain>.md × 7 (각 도메인의 모든 concept link)
//
// 모든 concept 가 자기 sub-hub 에서 link 되므로 isolated 해소.

import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const ROOT = path.resolve('docs');
const CONCEPTS_DIR = path.join(ROOT, 'concepts');
const HUBS_DIR = path.join(ROOT, 'hubs');
const HUBS_CONCEPTS_DIR = path.join(HUBS_DIR, 'concepts');

const DOMAIN_LABEL = {
  functions: '함수',
  geometry: '도형',
  'probability-stats': '확률통계',
  algebra: '수와식',
  equations: '방정식',
  logic: '논리',
  uncategorized: '미분류',
};
const SUBDIR_ORDER = ['functions', 'geometry', 'probability-stats', 'algebra', 'equations', 'logic', 'uncategorized'];

function listSubdirs() {
  return readdirSync(CONCEPTS_DIR, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => e.name);
}

function listMd(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith('.md')).map((f) => path.join(dir, f));
}

const TYPE_ORDER = ['unit', 'definition', 'theorem', 'lemma', 'example'];
const TYPE_LABEL = { unit: '단원', definition: '정의', theorem: '정리', lemma: '보조정리', example: '예제' };

function buildSubHub(subdir) {
  const files = listMd(path.join(CONCEPTS_DIR, subdir));
  const items = files.map((p) => {
    const fm = matter(readFileSync(p, 'utf8')).data;
    return {
      slug: path.basename(p, '.md'),
      concept_type: fm.concept_type ?? 'definition',
      grade: fm.grade ?? '—',
      mastery: fm.mastery ?? 'unknown',
      unit: fm.unit ?? null,
    };
  });
  // group by concept_type
  const buckets = {};
  for (const it of items) (buckets[it.concept_type] ??= []).push(it);
  for (const k of Object.keys(buckets)) buckets[k].sort((a, b) => a.slug.localeCompare(b.slug, 'ko'));

  const orderedTypes = [
    ...TYPE_ORDER.filter((t) => buckets[t]?.length),
    ...Object.keys(buckets).filter((t) => !TYPE_ORDER.includes(t)).sort(),
  ];

  const label = DOMAIN_LABEL[subdir] ?? subdir;
  const today = new Date().toISOString().slice(0, 10);
  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: concepts-sub
domain: ${subdir}
counts:
  total: ${items.length}
---

# ${label} (${subdir})

이 도메인의 모든 concept 노드 (${items.length}개). 상위: [concepts hub](../concepts.md).

`;
  for (const t of orderedTypes) {
    body += `## ${TYPE_LABEL[t] ?? t} (${buckets[t].length})\n\n`;
    for (const it of buckets[t]) {
      const label = it.slug.replace(/_/g, ' ');
      body += `- [${label}](../../concepts/${subdir}/${it.slug}.md)${it.grade !== '—' ? ` — ${it.grade}` : ''}${it.unit ? ` · ${it.unit}` : ''} \`${it.mastery}\`\n`;
    }
    body += '\n';
  }

  return body;
}

function buildRootHub(subdirs) {
  const today = new Date().toISOString().slice(0, 10);
  const stats = {};
  let total = 0;
  for (const sd of subdirs) {
    const c = listMd(path.join(CONCEPTS_DIR, sd)).length;
    stats[sd] = c;
    total += c;
  }

  const orderedSubs = [
    ...SUBDIR_ORDER.filter((s) => subdirs.includes(s)),
    ...subdirs.filter((s) => !SUBDIR_ORDER.includes(s)).sort(),
  ];

  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: concepts
counts:
  total: ${total}
  by_subdir:
`;
  for (const sd of orderedSubs) body += `    ${sd}: ${stats[sd]}\n`;
  body += `---

# Concepts hub

총 ${total}개 concept 노드, ${orderedSubs.length}개 도메인.

`;
  for (const sd of orderedSubs) {
    const label = DOMAIN_LABEL[sd] ?? sd;
    body += `- [${label} (${sd})](./concepts/${sd}.md) — ${stats[sd]}개\n`;
  }
  body += '\n전체 graph 시각화: [/graph](../../web/) (dev server 의 graph 페이지).\n';
  return body;
}

function main() {
  const subdirs = listSubdirs();
  if (subdirs.length === 0) {
    console.error('no concept sub-dirs found — Phase A2 not run?');
    process.exit(1);
  }
  mkdirSync(HUBS_CONCEPTS_DIR, { recursive: true });

  for (const sd of subdirs) {
    const out = buildSubHub(sd);
    const outPath = path.join(HUBS_CONCEPTS_DIR, `${sd}.md`);
    writeFileSync(outPath, out, 'utf8');
    console.log(`  wrote ${path.relative(process.cwd(), outPath)}`);
  }

  const rootHub = buildRootHub(subdirs);
  writeFileSync(path.join(HUBS_DIR, 'concepts.md'), rootHub, 'utf8');
  console.log(`  wrote ${path.relative(process.cwd(), path.join(HUBS_DIR, 'concepts.md'))}`);

  console.log(`\n✓ ${subdirs.length} sub-hubs + 1 root hub generated`);
}

main();
