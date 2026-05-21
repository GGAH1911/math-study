#!/usr/bin/env node
/**
 * docs/problems/*.md 전체를 스캔해서 frontmatter `concepts:` 를 invert.
 * 출력: src/data/problems-by-concept.json
 *   {
 *     generatedAt, totalProblems, conceptsWithProblems,
 *     byConcept: {
 *       "다항식": [{ slug, year, exam_type, session, grade, subject, number, score,
 *                    killer_tier, format, has_image }, ...]
 *     }
 *   }
 *
 * concept 페이지가 SSR 시 import해 "이 개념의 기출 문제" 섹션 표시.
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const PROBLEMS_DIR = join(REPO_ROOT, 'docs', 'problems');
const CONCEPTS_DIR = join(REPO_ROOT, 'docs', 'concepts');
const OUT_DIR = join(WEB_ROOT, 'src', 'data');
const OUT_FILE = join(OUT_DIR, 'problems-by-concept.json');

const conceptSlugs = new Set(
  readdirSync(CONCEPTS_DIR).filter((f) => f.endsWith('.md')).map((f) => basename(f, '.md')),
);

// Spoke (definition/theorem/lemma/example) → parent unit 매핑.
// concept-graph.json 의 unit 노드 `enables:` 를 역방향으로 walk.
// Propagation 에 사용 — problem이 spoke 만 참조해도 그 spoke의 parent unit에
// 자동으로 매핑 추가됨.
const GRAPH_FILE = join(WEB_ROOT, 'src', 'data', 'concept-graph.json');
const parentOf = {};
if (existsSync(GRAPH_FILE)) {
  const graph = JSON.parse(readFileSync(GRAPH_FILE, 'utf-8'));
  for (const n of graph.nodes ?? []) {
    if (n.concept_type === 'unit') {
      for (const child of (n.enables ?? [])) {
        parentOf[child] = n.id;
      }
    }
  }
}

function pathToSlug(p) { return basename(String(p), '.md'); }

const byConcept = {}; // slug → [problem brief, ...]
const missing = new Set(); // concept slug 가 concept-graph 에 없는 경우
let totalProblems = 0;
let totalMappings = 0;
let propagatedMappings = 0;

// dedup용 — (concept slug, problem slug) 페어 추적
const seenPair = new Set();
function addMapping(conceptSlug, brief, via) {
  if (!conceptSlugs.has(conceptSlug)) { missing.add(conceptSlug); return false; }
  const k = `${conceptSlug}::${brief.slug}`;
  if (seenPair.has(k)) return false;
  seenPair.add(k);
  (byConcept[conceptSlug] = byConcept[conceptSlug] || []).push({ ...brief, via });
  return true;
}

const problemFiles = readdirSync(PROBLEMS_DIR).filter((f) => f.endsWith('.md'));
for (const fname of problemFiles) {
  totalProblems++;
  const file = join(PROBLEMS_DIR, fname);
  const raw = readFileSync(file, 'utf-8');
  const { data: fm } = matter(raw);
  const src = fm.source || {};
  const brief = {
    slug: basename(fname, '.md'),
    year: src.year ?? null,
    exam_type: src.exam_type ?? null,
    session: src.session ?? null,
    grade: src.grade ?? null,
    subject: src.subject ?? null,
    number: src.number ?? null,
    score: src.score ?? null,
    killer_tier: fm.killer_tier || null,
    format: fm.format || null,
    has_image: !!fm.has_image,
  };
  // 1) direct 매핑
  const directSlugs = new Set();
  for (const cp of (fm.concepts ?? [])) {
    const slug = pathToSlug(cp);
    if (addMapping(slug, brief, 'direct')) {
      totalMappings++;
      directSlugs.add(slug);
    }
  }
  // 2) propagation: 각 direct slug 의 parent unit 에도 자동 추가
  //    (spoke → parent unit). direct가 이미 unit이면 parentOf에 없으니 무시.
  for (const s of directSlugs) {
    const parent = parentOf[s];
    if (parent && !directSlugs.has(parent)) {
      if (addMapping(parent, brief, 'propagated')) {
        propagatedMappings++;
      }
    }
  }
}

// 각 concept 의 문제 목록 정렬: killer_tier > year desc > number desc
const TIER_RANK = { killer: 0, high: 1, mid: 2, early: 3 };
function tierKey(t) { return TIER_RANK[t] ?? 4; }
for (const slug of Object.keys(byConcept)) {
  byConcept[slug].sort((a, b) => {
    const t = tierKey(a.killer_tier) - tierKey(b.killer_tier);
    if (t !== 0) return t;
    const y = (b.year ?? 0) - (a.year ?? 0);
    if (y !== 0) return y;
    return (b.number ?? 0) - (a.number ?? 0);
  });
}

mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(OUT_FILE, JSON.stringify({
  generatedAt: new Date().toISOString(),
  totalProblems,
  conceptsWithProblems: Object.keys(byConcept).length,
  totalMappings,
  propagatedMappings,
  byConcept,
}, null, 2), 'utf-8');

console.log(`[problem-index] ${totalProblems} problems, ${Object.keys(byConcept).length} concepts mapped, ${totalMappings} direct + ${propagatedMappings} propagated edges → ${OUT_FILE.replace(REPO_ROOT + '/', '')}`);
if (missing.size > 0) {
  console.log(`  ⚠ ${missing.size} concept slug 누락 (problem 참조했지만 concept 파일 없음). 일부:`);
  let i = 0;
  for (const s of missing) { if (i++ < 10) console.log(`    ${s}`); }
}
