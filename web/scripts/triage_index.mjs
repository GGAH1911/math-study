#!/usr/bin/env node
// figure-triage.json 인덱스 빌드/갱신.
// 모든 docs/problems/**/*.md 의 figures/inline_figures 를 스캔해 트리아지 큐에 넣는다.
// 기존 결정(status/triaged_*)은 보존하고, 신규 figure 만 untriaged 로 추가. 사라진 figure 는 제거.
// 사용: node web/scripts/triage_index.mjs   (옵션 --prune-missing 없으면 사라진 것도 유지)
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = join(__dirname, '..', '..');               // .../math-study
const PROB_DIR = join(REPO, 'docs', 'problems');
const OUT = join(REPO, 'web', 'src', 'data', 'figure-triage.json');

function walk(dir, acc = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, acc);
    else if (e.name.endsWith('.md')) acc.push(p);
  }
  return acc;
}

// 기존 인덱스 로드(결정 보존)
let prev = { schemaVersion: 1, figures: {} };
if (existsSync(OUT)) { try { prev = JSON.parse(readFileSync(OUT, 'utf-8')); } catch { /* 깨졌으면 새로 */ } }
const prevFigs = prev.figures || {};

const figures = {};
let nFiles = 0, nFig = 0, nNew = 0;
for (const file of walk(PROB_DIR)) {
  nFiles++;
  let fm;
  try { fm = matter(readFileSync(file, 'utf-8')).data; } catch { continue; }
  const slug = basename(file, '.md');
  const round = file.replace(PROB_DIR + '/', '').split('/').slice(0, 2).join('/'); // 연도/회차
  const subject = (fm.subject || slug.match(/_(가형|나형|단일|미적분|확률과통계|기하|공통)_/)?.[1]) || '';
  const items = [];
  if (Array.isArray(fm.figures)) fm.figures.forEach((f, i) => f?.image && items.push([f.image, 'figure', i]));
  if (Array.isArray(fm.inline_figures)) fm.inline_figures.forEach((f, i) => f?.image && items.push([f.image, 'inline', i]));
  for (const [image, kind, idx] of items) {
    nFig++;
    const existing = prevFigs[image];
    if (existing) { figures[image] = { ...existing, problem_slug: slug, round, subject, kind, figure_index: idx }; }
    else {
      nNew++;
      figures[image] = {
        problem_slug: slug, round, subject, kind, figure_index: idx,
        status: 'untriaged', suggested: null, suggest_reason: null,
        triaged_by: null, triaged_at: null, notes: null, render3d: null,
      };
    }
  }
}

if (!existsSync(dirname(OUT))) mkdirSync(dirname(OUT), { recursive: true });
const out = { schemaVersion: 1, generatedAt: process.argv.includes('--stamp') ? new Date().toISOString() : (prev.generatedAt ?? null), figures };
writeFileSync(OUT, JSON.stringify(out, null, 2));

// 상태 카운트
const counts = {};
for (const v of Object.values(figures)) counts[v.status] = (counts[v.status] || 0) + 1;
console.log(`스캔 ${nFiles} md · figure ${nFig}개 (신규 ${nNew}) → ${OUT}`);
console.log('상태:', JSON.stringify(counts));
