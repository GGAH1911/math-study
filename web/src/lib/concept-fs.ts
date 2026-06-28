// 개념/문제 마크다운 FS·검색 헬퍼 — chat-context 에서 분리. 서버 전용(node:fs).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import matter from 'gray-matter';

export const WEB_ROOT = process.cwd();
export const CONCEPTS_DIR = resolve(WEB_ROOT, '..', 'docs', 'concepts');
export const PROBLEMS_DIR = resolve(WEB_ROOT, '..', 'docs', 'problems');

export type ConceptFM = {
  slug: string;
  concept_type: string;
  grade?: string;
  unit?: string;
  prerequisites: string[];
  enables: string[];
  mastery: string;
  body: string;
};

// 수식 출력 규칙: Haiku 같은 작은 모델이 부등식/절댓값/집합기호를 raw
// 텍스트로 흘리는 빈도가 높아 별도 섹션으로 강조. 이걸 안 따르면 `<`가
// HTML-escape되어 `&lt;`로 그대로 화면에 노출됨.

// 도구(그래픽 fence) 카탈로그 + 정적/동적 선택 규칙. 모든 튜터 프롬프트
// (concept/problem)가 이 동일한 가이드를 공유하도록 추출. 도구만 추가하고
// prompt를 안 건드리면 LLM이 새 도구를 거의 안 쓰기 때문에 — system prompt가
// 핵심 산출물.

// concept slug 는 sub-dir 포함 ('algebra/근의_공식'). problems 도 sub-dir 진입 예정.
// 'docs/concepts/algebra/근의_공식.md' 또는 'algebra/근의_공식.md' 등 다양한 형식 수용.
export function slugOf(p: string) {
  return String(p)
    .replace(/^docs\/(concepts|problems)\//, '')
    .replace(/\.md$/, '');
}

// Slug whitelist — Korean letters, ASCII letters/digits, underscore, dash, slash (sub-dir).
// `..` 같은 path-traversal 은 safeJoin 의 prefix check 가 차단.
const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/;

export function safeJoin(baseDir: string, slug: string): string | null {
  const nfc = String(slug).normalize('NFC');                 // 한글 슬러그는 NFC로 화이트리스트 검사
  if (!SLUG_RE.test(nfc) || nfc.includes('..')) return null;
  // ★파일시스템 정규화 불일치(Astro entry.id=NFC vs readdir=NFD) 대비 — 존재하는 형태를 찾는다.
  for (const s of [slug, nfc, String(slug).normalize('NFD')]) {
    const target = resolve(baseDir, `${s}.md`);
    if (target.startsWith(resolve(baseDir) + '/') && existsSync(target)) return target;
  }
  return null;
}

export function readConcept(slug: string): ConceptFM | null {
  const p = safeJoin(CONCEPTS_DIR, slug);
  if (!p || !existsSync(p)) return null;
  const raw = readFileSync(p, 'utf-8');
  const parsed = matter(raw);
  const fm = parsed.data;
  return {
    slug,
    concept_type: fm.concept_type ?? 'definition',
    grade: fm.grade,
    unit: fm.unit,
    prerequisites: (fm.prerequisites ?? []).map((p: string) => slugOf(p)),
    enables: (fm.enables ?? []).map((p: string) => slugOf(p)),
    mastery: fm.mastery ?? 'unknown',
    body: parsed.content,
  };
}

function walkMdSync(dir: string): string[] {
  if (!existsSync(dir)) return [];
  const out: string[] = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = resolve(dir, e.name);
    if (e.isDirectory()) out.push(...walkMdSync(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

export function listAllConcepts(): ConceptFM[] {
  return walkMdSync(CONCEPTS_DIR)
    .map((abs) => {
      const rel = abs.slice(resolve(CONCEPTS_DIR).length + 1).replace(/\.md$/, '').split(/[\\/]/).join('/');
      return readConcept(rel);
    })
    .filter((c): c is ConceptFM => c !== null);
}

// 질문 텍스트와 개념 인덱스를 bigram(2글자) 오버랩으로 매칭 → 실존 개념 후보.
// 한국어는 토큰 경계가 모호해 char-bigram 이 견고. score = 개념명 bigram 중 질문에
// 들어있는 비율 → 개념명이 질문에 얼마나 등장하나. 튜터에 "실존 후보"를 주입해
// 경로 추측(hallucination)을 막는 retrieval grounding 용.
function _bigrams(s: string): Set<string> {
  const t = s.replace(/[\s_]/g, '').toLowerCase();
  const out = new Set<string>();
  if (t.length === 1) { out.add(t); return out; }
  for (let i = 0; i < t.length - 1; i++) out.add(t.slice(i, i + 2));
  return out;
}

export function searchConcepts(query: string, limit = 6, minScore = 0.5): ConceptFM[] {
  const qb = _bigrams(query);
  if (qb.size === 0) return [];
  // 단일 글자 개념명(예: '원')은 multi-char 질의의 bigram 집합과 절대 교집합이
  // 안 생겨 누락된다 — 1글자 이름은 질의 본문 substring 포함 여부로 별도 판정.
  const qNorm = query.replace(/[\s_]/g, '').toLowerCase();
  const scored: { c: ConceptFM; score: number }[] = [];
  for (const c of listAllConcepts()) {
    const name = c.slug.split('/').pop() ?? c.slug;        // 마지막 세그먼트 = 개념명
    const nb = _bigrams(name);
    if (nb.size === 0) continue;
    const nNorm = name.replace(/[\s_]/g, '').toLowerCase();
    if (nNorm.length === 1) {
      if (qNorm.includes(nNorm)) scored.push({ c, score: 1 });
      continue;
    }
    let inter = 0;
    for (const g of nb) if (qb.has(g)) inter++;
    const score = inter / nb.size;
    if (score >= minScore) scored.push({ c, score });
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, limit).map((s) => s.c);
}

export function readProblem(slug: string): { slug: string; fm: Record<string, any>; body: string } | null {
  const p = safeJoin(PROBLEMS_DIR, slug);
  if (!p || !existsSync(p)) return null;
  const parsed = matter(readFileSync(p, 'utf-8'));
  return { slug, fm: parsed.data, body: parsed.content };
}
