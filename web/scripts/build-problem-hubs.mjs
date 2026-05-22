#!/usr/bin/env node
// Phase B hub: problems/ sub-dir 기반 hub 자동 재생성
//   - docs/hubs/problems.md (year 별 link)
//   - docs/hubs/problems/<year>.md (round 별 link)
//   - docs/hubs/problems/<year>/<round>.md (problem 별 link, subject 그루핑)

import { readdirSync, readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..', 'docs');
const PROBLEMS_DIR = path.join(ROOT, 'problems');
const HUBS_DIR = path.join(ROOT, 'hubs');
const HUBS_PROBLEMS_DIR = path.join(HUBS_DIR, 'problems');

function subdirs(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => e.name);
}

function listMd(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith('.md')).map((f) => path.join(dir, f));
}

const SUBJECT_ORDER = ['공통', '미적분', '확률과통계', '기하', '단일'];

function buildRoundHub(year, round) {
  const dir = path.join(PROBLEMS_DIR, year, round);
  const files = listMd(dir);
  const bySubject = {};
  for (const p of files) {
    const fm = matter(readFileSync(p, 'utf8')).data;
    const subj = fm.source?.subject ?? '?';
    const num = fm.source?.number ?? 0;
    (bySubject[subj] ??= []).push({
      slug: path.basename(p, '.md'),
      num: typeof num === 'number' ? num : parseInt(String(num), 10) || 0,
      tier: fm.killer_tier ?? null,
      answer: fm.answer ?? null,
    });
  }
  for (const k of Object.keys(bySubject)) bySubject[k].sort((a, b) => a.num - b.num);

  const orderedSubs = [
    ...SUBJECT_ORDER.filter((s) => bySubject[s]?.length),
    ...Object.keys(bySubject).filter((s) => !SUBJECT_ORDER.includes(s)).sort(),
  ];

  const today = new Date().toISOString().slice(0, 10);
  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: problems-round
year: ${year}
round: ${round}
counts:
  total: ${files.length}
---

# ${year} ${round}

총 ${files.length}개 문항. 상위: [${year} hub](../${year}.md) · [problems hub](../../problems.md).

`;
  for (const s of orderedSubs) {
    body += `## ${s} (${bySubject[s].length})\n\n`;
    for (const it of bySubject[s]) {
      const tier = it.tier ? ` \`${it.tier}\`` : '';
      const ans = it.answer ? ` 정답:${it.answer}` : '';
      body += `- [${it.num}번](../../../problems/${year}/${round}/${it.slug}.md)${tier}${ans}\n`;
    }
    body += '\n';
  }
  return body;
}

function buildYearHub(year) {
  const dir = path.join(PROBLEMS_DIR, year);
  const rounds = subdirs(dir);
  const today = new Date().toISOString().slice(0, 10);
  const roundCounts = rounds.map((r) => ({ r, c: listMd(path.join(dir, r)).length }));
  roundCounts.sort((a, b) => a.r.localeCompare(b.r, 'ko'));
  const total = roundCounts.reduce((s, x) => s + x.c, 0);

  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: problems-year
year: ${year}
counts:
  total: ${total}
  rounds: ${rounds.length}
---

# ${year}학년도 문항

총 ${total}개 문항, ${rounds.length}개 회차. 상위: [problems hub](../problems.md).

`;
  for (const { r, c } of roundCounts) {
    body += `- [${r}](./${year}/${r}.md) — ${c}개\n`;
  }
  return body;
}

function buildRootHub(years) {
  const today = new Date().toISOString().slice(0, 10);
  const yearCounts = years.map((y) => {
    const rounds = subdirs(path.join(PROBLEMS_DIR, y));
    const total = rounds.reduce((s, r) => s + listMd(path.join(PROBLEMS_DIR, y, r)).length, 0);
    return { y, rounds: rounds.length, total };
  });
  yearCounts.sort((a, b) => b.y.localeCompare(a.y));
  const grandTotal = yearCounts.reduce((s, x) => s + x.total, 0);

  let body = `---
sources: []
created: ${today}
updated: ${today}
hub_type: problems
counts:
  total: ${grandTotal}
  years: ${years.length}
---

# Problems hub

총 ${grandTotal}개 문항, ${years.length}개 학년도.

`;
  for (const { y, rounds, total } of yearCounts) {
    body += `- [${y}학년도](./problems/${y}.md) — ${rounds}개 회차, ${total}개 문항\n`;
  }
  return body;
}

function main() {
  const years = subdirs(PROBLEMS_DIR);
  if (!years.length) { console.error('no problem years'); process.exit(1); }

  for (const y of years) {
    const yDir = path.join(HUBS_PROBLEMS_DIR, y);
    mkdirSync(yDir, { recursive: true });
    for (const r of subdirs(path.join(PROBLEMS_DIR, y))) {
      writeFileSync(path.join(yDir, `${r}.md`), buildRoundHub(y, r), 'utf8');
    }
    writeFileSync(path.join(HUBS_PROBLEMS_DIR, `${y}.md`), buildYearHub(y), 'utf8');
  }
  writeFileSync(path.join(HUBS_DIR, 'problems.md'), buildRootHub(years), 'utf8');

  const roundCount = years.reduce((s, y) => s + subdirs(path.join(PROBLEMS_DIR, y)).length, 0);
  console.log(`✓ ${years.length} year hubs + ${roundCount} round hubs + 1 root hub generated`);
}

main();
