#!/usr/bin/env node
// Phase A4: concepts/ sub-dir 기반 hub 자동 재생성
//   - docs/hubs/concepts.md (overview + sub-hub link)
//   - docs/hubs/concepts/<domain>.md × 7 (각 도메인의 모든 concept link)
//
// 모든 concept 가 자기 sub-hub 에서 link 되므로 isolated 해소.

import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..', 'docs');
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

// grade slug → 한국어 label
const GRADE_LABEL = {
  'middle-1': '중1', 'middle-2': '중2', 'middle-3': '중3',
  'high-1': '고1', 'math-1': '수학1', 'math-2': '수학2',
  'calculus': '미적분', 'geometry-elective': '기하', 'prob-stats-elective': '확률과통계',
  '_misc': '미분류 grade',
};
const GRADE_ORDER = ['middle-1', 'middle-2', 'middle-3', 'high-1', 'math-1', 'math-2', 'calculus', 'geometry-elective', 'prob-stats-elective', '_misc'];

function listSubSubdirs(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => e.name);
}

function readConceptMd(absPath, fileNameOnly) {
  const fm = matter(readFileSync(absPath, 'utf8')).data;
  return {
    slug: fileNameOnly.replace(/\.md$/, ''),
    concept_type: fm.concept_type ?? 'definition',
    grade: fm.grade ?? '—',
    mastery: fm.mastery ?? 'unknown',
    unit: fm.unit ?? null,
  };
}

// 도메인 hub (예: hubs/concepts/functions.md) — grade sub-sub-dir 별 link.
function buildSubHub(subdir) {
  const domainDir = path.join(CONCEPTS_DIR, subdir);
  const flatFiles = listMd(domainDir); // direct child (uncategorized 케이스)
  const gradeDirs = listSubSubdirs(domainDir);

  const total = flatFiles.length + gradeDirs.reduce((s, g) => s + listMd(path.join(domainDir, g)).length, 0);
  const label = DOMAIN_LABEL[subdir] ?? subdir;
  const today = new Date().toISOString().slice(0, 10);

  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: concepts-sub
domain: ${subdir}
counts:
  total: ${total}
---

# ${label} (${subdir})

총 ${total}개 concept 노드. 상위: [concepts hub](../concepts.md).

`;

  // grade-level sub-hub 링크
  if (gradeDirs.length > 0) {
    body += `## 학년/과목별\n\n`;
    const ordered = [
      ...GRADE_ORDER.filter((g) => gradeDirs.includes(g)),
      ...gradeDirs.filter((g) => !GRADE_ORDER.includes(g)).sort(),
    ];
    for (const g of ordered) {
      const c = listMd(path.join(domainDir, g)).length;
      body += `- [${GRADE_LABEL[g] ?? g}](../../concepts/${subdir}/${g}/) — ${c}개 (sub-hub: [./${subdir}/${g}.md](./${subdir}/${g}.md))\n`;
    }
    body += '\n';
  }

  // 도메인 dir 직속 (uncategorized 같은 케이스)
  if (flatFiles.length > 0) {
    const items = flatFiles.map((p) => readConceptMd(p, path.basename(p)));
    const buckets = {};
    for (const it of items) (buckets[it.concept_type] ??= []).push(it);
    for (const k of Object.keys(buckets)) buckets[k].sort((a, b) => a.slug.localeCompare(b.slug, 'ko'));
    const orderedTypes = [
      ...TYPE_ORDER.filter((t) => buckets[t]?.length),
      ...Object.keys(buckets).filter((t) => !TYPE_ORDER.includes(t)).sort(),
    ];
    for (const t of orderedTypes) {
      body += `## ${TYPE_LABEL[t] ?? t} (${buckets[t].length})\n\n`;
      for (const it of buckets[t]) {
        const link = it.slug.replace(/_/g, ' ');
        body += `- [${link}](../../concepts/${subdir}/${it.slug}.md) \`${it.mastery}\`\n`;
      }
      body += '\n';
    }
  }

  return body;
}

// grade level hub (예: hubs/concepts/functions/calculus.md) — concept 직접 link.
function buildGradeHub(subdir, gradeDir) {
  const dir = path.join(CONCEPTS_DIR, subdir, gradeDir);
  const files = listMd(dir);
  const items = files.map((p) => readConceptMd(p, path.basename(p)));

  const buckets = {};
  for (const it of items) (buckets[it.concept_type] ??= []).push(it);
  for (const k of Object.keys(buckets)) buckets[k].sort((a, b) => a.slug.localeCompare(b.slug, 'ko'));

  const orderedTypes = [
    ...TYPE_ORDER.filter((t) => buckets[t]?.length),
    ...Object.keys(buckets).filter((t) => !TYPE_ORDER.includes(t)).sort(),
  ];

  const today = new Date().toISOString().slice(0, 10);
  const domLabel = DOMAIN_LABEL[subdir] ?? subdir;
  const gradeLabel = GRADE_LABEL[gradeDir] ?? gradeDir;

  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: concepts-grade
domain: ${subdir}
grade: ${gradeDir}
counts:
  total: ${items.length}
---

# ${domLabel} · ${gradeLabel} (${gradeDir})

총 ${items.length}개 concept 노드. 상위: [${domLabel} hub](../${subdir}.md) · [concepts hub](../../concepts.md).

`;
  for (const t of orderedTypes) {
    body += `## ${TYPE_LABEL[t] ?? t} (${buckets[t].length})\n\n`;
    for (const it of buckets[t]) {
      const link = it.slug.replace(/_/g, ' ');
      body += `- [${link}](../../../concepts/${subdir}/${gradeDir}/${it.slug}.md)${it.unit ? ` · ${it.unit}` : ''} \`${it.mastery}\`\n`;
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

  let gradeHubCount = 0;
  for (const sd of subdirs) {
    writeFileSync(path.join(HUBS_CONCEPTS_DIR, `${sd}.md`), buildSubHub(sd), 'utf8');
    // grade sub-sub-dirs
    const domainDir = path.join(CONCEPTS_DIR, sd);
    const gradeDirs = listSubSubdirs(domainDir);
    if (gradeDirs.length > 0) {
      mkdirSync(path.join(HUBS_CONCEPTS_DIR, sd), { recursive: true });
      for (const g of gradeDirs) {
        writeFileSync(path.join(HUBS_CONCEPTS_DIR, sd, `${g}.md`), buildGradeHub(sd, g), 'utf8');
        gradeHubCount++;
      }
    }
  }

  const rootHub = buildRootHub(subdirs);
  writeFileSync(path.join(HUBS_DIR, 'concepts.md'), rootHub, 'utf8');

  console.log(`✓ ${subdirs.length} domain hubs + ${gradeHubCount} grade hubs + 1 root hub generated`);
}

main();
