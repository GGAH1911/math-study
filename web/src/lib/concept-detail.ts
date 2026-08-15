// 개념 상세 데이터 — `concepts/[...slug]` 가 그리는 **모든 것**을 서버에서 만든다.
//
// ★왜 서버인가: 선수/후속 링크 해석(정규화 leaf 매칭), 연결된 기출·학습노트(빌드 산출물),
//   도형/위젯 스펙(파일), 사용자별 mastery(DB)가 얽혀 있다. 전부 전수 조회나 파일 접근이다.
//
// ★mastery 는 frontmatter(전역)가 아니라 **로그인 사용자의 `concept_mastery`** 에서 읽는다.
//   멀티유저라 frontmatter 값을 쓰면 남의 진도가 보인다.
import { getCollection, getEntry } from 'astro:content';
import { readFileSync } from 'node:fs';
import { getMastery } from './mastery.ts';
import { TYPE_LABEL_KO as TYPE_LABEL, TYPE_ORDER, MASTERY_LABEL_KO } from './concept-meta';
import { REVIEW_STATE_LABEL_KO } from './srs.ts';
import conceptFigures from '../data/concept-figures.json';
import { loadConceptSpec } from './concept-widgets-server';
import { hasWidget } from './concept-widgets';
import problemIndex from '../data/problems-by-concept.json';
import synthesesIndex from '../data/syntheses-by-concept.json';
import { mediaPath } from './media-root.ts';

/** 방출물에서 선렌더 HTML — SSR 의 `<Content />` 와 같은 바이트다. */
function emittedHtml(id: string): string {
  const abs = mediaPath(`/content/concepts/${id}.json`);
  if (!abs) return '';
  try { return (JSON.parse(readFileSync(abs, 'utf8')) as { html?: string }).html ?? ''; }
  catch { return ''; }
}

/**
 * 튜터 채팅 헤더용 단원명만 — 방출물 **한 건**만 읽는다(컬렉션 전수 조회 없음).
 *
 * ★`TutorChat` 은 자체 스크립트가 있어 서버 렌더로 남는다. 그래서 26줄짜리 껍데기
 *   페이지가 이 값 하나는 알아야 한다. `problem-detail.ts` 의 `problemTitle` 과 같은 꼴.
 * ★옛 SSR 페이지의 `fm.unit ?? entry.id` 와 같은 값을 준다.
 * ★flat-leaf(`지수와_로그`)면 방출물이 없어 slug 를 그대로 돌려준다 — 제목이 덜 예쁠 뿐
 *   튜터는 뜬다. 정식 경로 해석은 섬이 클라이언트에서 하고, 그걸 위해 여기서 컬렉션을
 *   전수 조회하면 Phase 3 에서 얻은 것을 도로 잃는다.
 */
export function conceptTitle(slug: string): string {
  const abs = mediaPath(`/content/concepts/${slug}.json`);
  if (!abs) return slug;
  try {
    return (JSON.parse(readFileSync(abs, 'utf8')) as { data?: { unit?: string } }).data?.unit || slug;
  } catch { return slug; }
}

/** flat-leaf → 정식(nested) 경로. 없으면 null. 라우트가 302 로 살린다. */
export async function resolveConceptSlug(slug: string): Promise<string | null> {
  const leafKey = (s: string) => (s.split('/').pop() ?? s).normalize('NFC').replace(/[\s_]/g, '').toLowerCase();
  const leaf = leafKey(slug);
  const all = await getCollection('concepts');
  return all.find((c) => leafKey(c.id) === leaf)?.id ?? null;
}

export async function buildConceptDetail(slug: string, userId: string | null) {
  const entry = await getEntry('concepts', slug);
  if (!entry) return null;
  const fm = { ...entry.data } as Record<string, any>;

  const um = userId ? await getMastery(userId, entry.id) : null;
  fm.mastery = um?.mastery ?? 'unknown';
  if (um?.mastery_updated) {
    const d = new Date(um.mastery_updated);
    if (!isNaN(d.getTime())) fm.mastery_updated = d.toISOString();
  }
  // sub-dir 호환: 'docs/concepts/algebra/근의_공식.md' → 'algebra/근의_공식'
  const fmtPath = (p: string) => p.replace(/^docs\/concepts\//, '').replace(/\.md$/, '');
  // 표시용 라벨은 마지막 segment 만
  const prettySlug = (s: string) => (s.split('/').pop() ?? s).replace(/_/g, ' ');
  
  // 타입별 그루핑 — 노드 맵의 라벨/순서와 동일.
  
  // 모든 concept frontmatter를 한 번에 로드해 link slug → concept_type 매핑.
  const all = await getCollection('concepts');
  const typeBySlug = new Map<string, string>();
  for (const c of all) typeBySlug.set(c.id, c.data.concept_type ?? 'other');
  
  // flat leaf → full 중첩 slug. prerequisites/enables 가 flat slug(`이차함수`)로 저장돼
  // `/concepts/이차함수` 가 404 나는 것을, 실제 c.id(`functions/middle-3/이차함수`)로
  // 해석해 고친다. (readdir NFD 대비 NFC 정규화. 같은 leaf 중복 시 첫 매칭 우선.)
  const leafToFull = new Map<string, string>();
  for (const c of all) {
    const leaf = (c.id.split('/').pop() ?? c.id).normalize('NFC');
    if (!leafToFull.has(leaf)) leafToFull.set(leaf, c.id);
  }
  
  function groupByType(paths: string[]): { type: string; label: string; items: { slug: string; label: string }[] }[] {
    const buckets: Record<string, { slug: string; label: string }[]> = {};
    for (const p of paths) {
      let slug = fmtPath(p);
      // flat slug 면 실제 중첩 slug 로 해석(prerequisites/enables 가 flat 저장 → 404 보정).
      if (!typeBySlug.has(slug)) {
        const full = leafToFull.get((slug.split('/').pop() ?? slug).normalize('NFC'));
        if (full) slug = full;
      }
      const t = typeBySlug.get(slug) ?? 'other';
      buckets[t] = buckets[t] ?? [];
      buckets[t].push({ slug, label: prettySlug(slug) });
    }
    // 알려진 type 순서대로 + 그 외 type을 알파벳 순으로
    const knownOrder = TYPE_ORDER.filter((t) => buckets[t]?.length);
    const otherTypes = Object.keys(buckets).filter((t) => !(TYPE_ORDER as readonly string[]).includes(t)).sort();
    return [...knownOrder, ...otherTypes].map((t) => ({
      type: t,
      label: TYPE_LABEL[t] ?? t,
      items: buckets[t].sort((a, b) => a.label.localeCompare(b.label, 'ko')),
    }));
  }
  
  const prereqGroups = groupByType(fm.prerequisites);
  const enablesGroups = groupByType(fm.enables);
  
  // 개념 도식 — gen_concept_figures.mjs 가 haiku(단계별·sympy 검증)로 생성·캐시한 좌표정확
  // Geometry spec. 축·눈금 숨김으로 본문 위에 교과서 도식처럼 렌더. 없으면(미생성·도식불필요) 생략.
  const _figEntry = (conceptFigures as any).figures?.[entry.id];
  const conceptFigure = _figEntry?.figure ?? null;
  // 3D(입체) 개념은 Geometry3D(R3F) 로 — gen_concept_figures --include-3d 가 figure3d 키로 캐시.
  const conceptFigure3d = _figEntry?.figure3d ?? null;
  const conceptWidgetSpec = loadConceptSpec(entry.id)?.spec ?? null;
  
  // "이 개념의 기출 문제" — predev로 빌드된 problems-by-concept 인덱스에서 로드.
  type ProblemBrief = {
    slug: string; year: number | null; exam_type: string | null; session: string | null;
    grade: string | null; subject: string | null; number: number | null; score: number | null;
    killer_tier: string | null; format: string | null; has_image: boolean;
  };
  const linkedProblemsRaw: ProblemBrief[] = (problemIndex as any).byConcept?.[slug] ?? [];
  
  // 진도(학년 수준) 근접 정렬 — 개념 수준에 가까운 기출이 먼저, 진도 한참 앞선 문제는 뒤로.
  // (기존엔 killer 우선이라 중1 개념에도 수능 킬러가 맨 위에 떠 "너무 앞선 문제" 문제 발생.)
  // 개념 수준은 경로(.../middle-1/.., /calculus/..)에서 산출 → frontmatter grade → 기본 고1.
  function levelFromPath(id: string): number {
    if (/\/middle-1\//.test(id)) return 1;
    if (/\/middle-2\//.test(id)) return 2;
    if (/\/middle-3\//.test(id)) return 3;
    if (/\/high-1\//.test(id)) return 4;
    if (/\/math-[12]\//.test(id)) return 5;
    if (/\/(calculus|geometry-elective|prob-stats-elective)\//.test(id)) return 6;
    const GL: Record<string, number> = { '중1': 1, '중2': 2, '중3': 3, '고1': 4, '수학1': 5, '수학2': 5, '미적분': 6, '기하': 6, '확률과통계': 6 };
    return GL[fm.grade ?? ''] ?? 4;
  }
  const conceptLevel = levelFromPath(entry.id);
  function problemLevel(p: ProblemBrief): number {
    if (p.exam_type === '수능' || p.exam_type === '평가원') return 6; // 고3 수준
    const g = p.grade ?? '';
    if (g.includes('고3')) return 6;
    if (g.includes('고2')) return 5;
    if (g.includes('고1')) return 4;
    if (g.includes('중3')) return 3;
    if (g.includes('중2')) return 2;
    if (g.includes('중1')) return 1;
    return 5;
  }
  const TIER_RANK: Record<string, number> = { early: 0, mid: 1, high: 2, killer: 3 };
  const linkedProblems: ProblemBrief[] = [...linkedProblemsRaw].sort((a, b) => {
    const da = Math.abs(problemLevel(a) - conceptLevel), db = Math.abs(problemLevel(b) - conceptLevel);
    if (da !== db) return da - db;                                  // 1) 학년 근접
    const ta = TIER_RANK[a.killer_tier ?? ''] ?? 1, tb = TIER_RANK[b.killer_tier ?? ''] ?? 1;
    if (ta !== tb) return ta - tb;                                  // 2) 쉬운 것부터
    return (b.year ?? 0) - (a.year ?? 0);                           // 3) 최신순
  });
  
  // 이 페이지에서 promote 된 학습 노트 목록 (build-syntheses-index.mjs 산출물).
  type SynthesisBrief = { slug: string; title: string; created: string | null; review_state: string | null; excerpt: string | null };
  const linkedSyntheses: SynthesisBrief[] = (synthesesIndex as any).byConcept?.[slug] ?? [];
  
  const TIER_LABEL: Record<string, { text: string; cls: string }> = {
    killer: { text: '상', cls: 'bg-rose-500/20 text-rose-300 border-rose-500/40' },
    high:   { text: '상', cls: 'bg-amber-500/20 text-amber-300 border-amber-500/40' },
    mid:    { text: '중',  cls: 'bg-sky-500/20 text-sky-300 border-sky-500/40' },
    early:  { text: '하', cls: 'bg-zinc-600/30 text-zinc-300 border-zinc-600' },
  };
  function tierBadge(t: string | null) {
    return TIER_LABEL[t ?? ''] ?? { text: '기타', cls: 'bg-zinc-700/30 text-zinc-400 border-zinc-700' };
  }
  function problemLabel(p: ProblemBrief): string {
    const yearShort = p.year ? String(p.year).slice(2) : '';
    const subj = p.subject && p.subject !== '단일' && p.subject !== '공통' ? ` ${p.subject}` : '';
    const session = p.session ? ` ${p.session}` : '';
    const exam = p.exam_type ?? '';
    const grade = p.grade && p.exam_type !== '수능' ? ` ${p.grade}` : '';
    return `${yearShort}${grade}${session} ${exam}${subj} ${p.number ?? '?'}번`.trim();
  }
  const PREVIEW_COUNT = 8;

  return {
    id: entry.id, data: fm, html: emittedHtml(entry.id),
    title: prettySlug(entry.id),
    typeLabel: TYPE_LABEL[fm.concept_type] ?? fm.concept_type,
    masteryLabel: MASTERY_LABEL_KO[fm.mastery] ?? fm.mastery,
    reviewLabel: fm.review_state ? (REVIEW_STATE_LABEL_KO[fm.review_state] ?? fm.review_state) : null,
    prereqGroups, enablesGroups,
    conceptFigure, conceptFigure3d, conceptWidgetSpec,
    linkedProblems, linkedSyntheses,
    hasWidgetOf: Object.fromEntries(
      [...(fm.prerequisites ?? []), ...(fm.enables ?? [])]
        .map((r: string) => { const id = leafToFull.get(fmtPath(r)) ?? fmtPath(r); return [r, hasWidget(id)]; }),
    ),
  };
}
