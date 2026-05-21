#!/usr/bin/env node
/**
 * `docs/problems/*.md` 전수 스캔해서 `concepts:` 가 비어있거나 잘못된 path
 * (존재하지 않는 concept .md 참조)를 식별. fallback chain 으로 채움:
 *   1) unit 필드 valid + concept .md 존재 → 그 unit으로 채움
 *   2) subject 단서로 default unit 매핑 (검정고시→다항식 등)
 *   3) (LLM fallback은 별도 단계; 본 스크립트는 deterministic만)
 *
 * Usage:
 *   node fill-missing-problem-concepts.mjs           # dry-run (default)
 *   node fill-missing-problem-concepts.mjs --apply   # 실제 적용
 *
 * 매핑 못 한 잔여는 docs/missing-concepts-map.json 에 catalog.
 */
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const PROBLEMS_DIR = join(REPO_ROOT, 'docs', 'problems');
const CONCEPTS_DIR = join(REPO_ROOT, 'docs', 'concepts');
const MISSING_LOG = join(REPO_ROOT, 'docs', 'missing-concepts-map.json');

const APPLY = process.argv.includes('--apply');

// 1) 사용 가능한 모든 concept slug 인덱스
const conceptSlugs = new Set(
  readdirSync(CONCEPTS_DIR).filter((f) => f.endsWith('.md')).map((f) => basename(f, '.md')),
);

// 2) subject 단서로 default unit 매핑 — 학평/수능 일반적
//    docs/concepts/ 에 실제로 존재하는 slug만 사용. 미적분/기하/확률/통계 root unit 으로.
const SUBJECT_DEFAULT = {
  '미적분': '미분',         // 미적분 영역은 미분 root로 (적분과 분할되어 있어 미분이 더 흔함)
  '확률과통계': '확률',
  '확률과 통계': '확률',
  '기하': '기하',
  '단일': null,
  '공통': '미분',           // 공통도 미적분 도함수·극값 위주가 대다수
};

// 3) 검정고시 default — 단일과목이고 unit 누락 시 일반 fallback
const GEOMGO_DEFAULT = '다항식';

// 4) unit 필드가 alias라 실제 concept 파일명과 다른 케이스 — 명시적 매핑.
//    누락된 unit 문자열을 가까운 실제 concept slug로 redirect.
//    NOTE: 새로 concept .md 가 생성되면 여기서 제거 (concept이 직접 존재하니 redirect 불필요).
const UNIT_ALIAS = {
  '확률과_통계': '확률',
};

function pathToSlug(p) {
  // "docs/concepts/다항식.md" → "다항식"
  return basename(p, '.md');
}

function conceptExists(slug) {
  return conceptSlugs.has(slug);
}

function listProblemFiles() {
  return readdirSync(PROBLEMS_DIR)
    .filter((f) => f.endsWith('.md'))
    .map((f) => join(PROBLEMS_DIR, f));
}

function fmtPathArray(slugs) {
  const list = slugs.map((s) => `docs/concepts/${s}.md`).join(', ');
  return `[${list}]`;
}

function tryFillFromUnit(fm) {
  const u = fm.unit;
  if (!u || u === 'None' || u === 'null') return null;
  const candidate = String(u).replace(/\s+/g, '_');
  if (conceptExists(candidate)) return candidate;
  if (conceptExists(String(u))) return String(u);
  // alias fallback — unit 문자열이 실제 concept slug 와 약간 다른 케이스
  if (UNIT_ALIAS[candidate]) return UNIT_ALIAS[candidate];
  if (UNIT_ALIAS[String(u)]) return UNIT_ALIAS[String(u)];
  return null;
}

function tryFillFromSubject(fm) {
  const src = fm.source || {};
  const subj = src.subject;
  const examType = src.exam_type;
  if (examType === '검정고시' && conceptExists(GEOMGO_DEFAULT)) return GEOMGO_DEFAULT;
  if (subj && SUBJECT_DEFAULT[subj] && conceptExists(SUBJECT_DEFAULT[subj])) return SUBJECT_DEFAULT[subj];
  return null;
}

const stats = {
  total: 0,
  alreadyMapped: 0,
  fixedByUnit: 0,
  fixedBySubject: 0,
  cleanedInvalidRefs: 0,
  stillEmpty: 0,
};
const fixes = []; // [{ file, before, after, reason }]
const stillEmpty = []; // [{ file, fm }]

for (const file of listProblemFiles()) {
  stats.total++;
  const raw = readFileSync(file, 'utf-8');
  const { data: fm, content } = matter(raw);

  const original = Array.isArray(fm.concepts) ? fm.concepts.slice() : [];
  // invalid path 처리: 우선 alias 로 redirect 시도, 그래도 안 되면 제거.
  const redirected = [];
  const removed = [];
  const seen = new Set();
  for (const p of original) {
    const slug = pathToSlug(String(p));
    let target = null;
    if (conceptExists(slug)) target = slug;
    else if (UNIT_ALIAS[slug] && conceptExists(UNIT_ALIAS[slug])) target = UNIT_ALIAS[slug];
    if (target && !seen.has(target)) {
      redirected.push(`docs/concepts/${target}.md`);
      seen.add(target);
    } else if (!target) {
      removed.push(String(p));
    }
  }
  const valid = redirected;

  if (valid.length === original.length && valid.length > 0) {
    stats.alreadyMapped++;
    continue;
  }

  if (removed.length > 0) stats.cleanedInvalidRefs++;

  // 새 매핑 후보
  let nextConcepts = valid.slice();
  let reason = removed.length > 0 ? `removed invalid: ${removed.join(', ')}` : 'concepts empty';

  if (nextConcepts.length === 0) {
    const fromUnit = tryFillFromUnit(fm);
    if (fromUnit) {
      nextConcepts = [`docs/concepts/${fromUnit}.md`];
      stats.fixedByUnit++;
      reason += ` → unit fallback: ${fromUnit}`;
    } else {
      const fromSubject = tryFillFromSubject(fm);
      if (fromSubject) {
        nextConcepts = [`docs/concepts/${fromSubject}.md`];
        stats.fixedBySubject++;
        reason += ` → subject fallback: ${fromSubject}`;
      }
    }
  }

  if (nextConcepts.length === 0) {
    stats.stillEmpty++;
    stillEmpty.push({ file: file.replace(REPO_ROOT + '/', ''), unit: fm.unit ?? null, subject: fm.source?.subject ?? null });
    continue;
  }

  // apply
  fixes.push({
    file: file.replace(REPO_ROOT + '/', ''),
    before: original,
    after: nextConcepts,
    reason,
  });

  if (APPLY) {
    fm.concepts = nextConcepts;
    // gray-matter stringify 는 array를 multi-line으로 dump. inline `[ ... ]` 유지 위해 직접 패치.
    const newFm = matter.stringify(content, fm);
    // matter.stringify는 array를 inline `[a, b]` 또는 multi-line dump하는데, 우리는 단일 line 선호.
    // 간단 후처리: concepts: 를 inline 으로 강제.
    const inline = nextConcepts.map((p) => p).join(', ');
    const patched = newFm.replace(/^concepts:[\s\S]*?(?=\n[A-Za-z_]|---)/m, `concepts: [${inline}]\n`);
    writeFileSync(file, patched, 'utf-8');
  }
}

console.log(`\n=== fill-missing-problem-concepts (${APPLY ? 'APPLY' : 'DRY-RUN'}) ===`);
console.log(`총 problem: ${stats.total}`);
console.log(`이미 정상 매핑: ${stats.alreadyMapped}`);
console.log(`unit fallback 정정: ${stats.fixedByUnit}`);
console.log(`subject fallback 정정: ${stats.fixedBySubject}`);
console.log(`invalid 참조 제거된 파일: ${stats.cleanedInvalidRefs}`);
console.log(`여전히 매핑 못함: ${stats.stillEmpty}`);

if (fixes.length > 0) {
  console.log(`\n--- 변경 예시 (최대 20개) ---`);
  for (const f of fixes.slice(0, 20)) {
    console.log(`  ${f.file}`);
    console.log(`    before: ${JSON.stringify(f.before)}`);
    console.log(`    after:  ${JSON.stringify(f.after)}`);
    console.log(`    reason: ${f.reason}`);
  }
  if (fixes.length > 20) console.log(`  ... (+${fixes.length - 20}개)`);
}

if (stillEmpty.length > 0) {
  if (APPLY) {
    writeFileSync(MISSING_LOG, JSON.stringify({ generatedAt: new Date().toISOString(), entries: stillEmpty }, null, 2), 'utf-8');
    console.log(`\n매핑 실패 ${stillEmpty.length}건 → ${MISSING_LOG}`);
  } else {
    console.log(`\n매핑 실패 ${stillEmpty.length}건 (apply 시 ${MISSING_LOG.replace(REPO_ROOT + '/', '')} 로 catalog):`);
    for (const e of stillEmpty.slice(0, 10)) {
      console.log(`  ${e.file}  unit=${e.unit}  subject=${e.subject}`);
    }
  }
}
