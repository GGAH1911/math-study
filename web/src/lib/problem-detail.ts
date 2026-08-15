// 기출 상세 데이터 — `problems/[...slug]` 가 그리는 **모든 것**을 서버에서 만든다.
//
// ★왜 서버인가: 이 화면은 본문 하나가 아니다 — 재구성 뷰(로제타 디코드 + Gemini 교정),
//   도형 배치, 회차 내 이전/다음 네비게이션, 개념 ref 해석(정규화 leaf 매칭)이 얽혀 있다.
//   전부 **파일·컬렉션 전수 조회**에 기대므로 브라우저로 옮길 수 없다.
//
// ★재구성은 **어드민 전용**이다. 도형 라벨이 이미지 밖으로 새는 엣지케이스가 있어 사용자에겐
//   부적합 — 사용자는 원본 이미지만 본다. 이 판정도 서버에서 한다(클라이언트가 정하면 우회된다).
import { getEntry, getCollection } from 'astro:content';
import { readFileSync } from 'node:fs';
import { renderReconstruct } from './reconstruct';
import { yearLabel } from './problem-meta';
import reconData from '../data/problem-reconstructions.json';
import { mediaPath } from './media-root.ts';

/** 방출물에서 선렌더 HTML 을 읽는다. SSR 의 `<Content />` 와 같은 바이트다. */
function emittedHtml(id: string): string {
  const abs = mediaPath(`/content/problems/${id}.json`);
  if (!abs) return '';
  try { return (JSON.parse(readFileSync(abs, 'utf8')) as { html?: string }).html ?? ''; }
  catch { return ''; }
}

// ★엔트리 타입을 좁게 쓰면 컬렉션 스키마와 안 맞는다(`number` 가 string|number 다).
//   읽는 필드만 최소로 받되 값 타입은 넓게 둔다.
type NavLike = { id: string; data: { source?: { subject?: string; number?: string | number } } };
const navOf = (e: NavLike) => ({
  id: e.id, subject: String(e.data.source?.subject ?? ''), number: Number(e.data.source?.number ?? 0),
});

export async function buildProblemDetail(slug: string, isAdmin: boolean) {
  const entry = await getEntry('problems', slug);
  if (!entry) return null;
  const fm = entry.data;
  const figFull =
    !fm.figure_image && !(fm.figures && fm.figures.length) && fm.has_figure && fm.image_paths && fm.image_paths[0]
      ? `/problem-images/${String(fm.image_paths[0]).split('/').pop()}`
      : null;
  const figSrc = fm.figure_image || figFull;
  const figDivOf = (src: string, full = false) =>
    `<div class="recon-fig-wrap"><img src="${src}" alt="도형" class="recon-fig${full ? ' recon-fig-full' : ''}" loading="lazy" />${full ? '<span class="recon-fig-note">원본 전체 이미지 (도형만 추출 불가)</span>' : ''}</div>`;
  // 다중 그림(figures: [{image, after_line}]) 우선 → 각자 위치에 삽입. 없으면 단일 figure_image/전체이미지 폴백.
  const figureList = Array.isArray(fm.figures) && fm.figures.length
    ? (fm.figures as any[]).map((f) => ({ html: figDivOf(String(f.image)), afterLine: f.after_line }))
    : (figSrc ? [{ html: figDivOf(figSrc, !!figFull), afterLine: fm.figure_after_line }] : []);
  // 인라인 도형: 본문 줄 중간 {{INLn}} 자리에 인라인 <img>(임베드 객체 src). 블록 figures 와 별개.
  const inlineFigList = Array.isArray(fm.inline_figures)
    ? (fm.inline_figures as any[]).map((f) => String(f.image))
    : [];
  // 표·연립 등 복잡한 2D 구조는 텍스트 재구성이 근본적으로 깨진다(표준정규분포표→분수, 연립 2식
  // 뒤섞임) → 재구성 대신 원본 전체이미지로 표시(해당 문제들은 전부 image_paths 보유).
  const _sText = fm.searchable_text ?? '';
  const _wholeStem =
    fm.image_paths && fm.image_paths[0] ? String(fm.image_paths[0]).split('/').pop() : null;
  // 표: 표준정규분포표(셀이 분수로 깨짐)·P(0≤Z 헤더·소수격자 분수. 연립: '연립방정식'이되 정상
  // \begin{cases}로 디코드된 건 제외(텍스트 재구성 양호). 해당 문제는 전부 image_paths 보유.
  const reconUnsupported =
    !(fm.tables && fm.tables.length) &&  // 표가 table JSON으로 추출됐으면 HTML <table> 재구성 지원(폴백 해제)
    !!_wholeStem &&
    (/표준정규분포표|P\(\s*0\s*[≤<]\s*Z|\\frac\{[\d.]+\s+[\d.]+/.test(_sText) ||
      (/연립방정식/.test(_sText) && !/\\begin\{cases\}/.test(_sText)));
  const reconFull = reconUnsupported
    ? `<div class="recon-fig-wrap"><img src="/problem-images/${_wholeStem}" alt="문제" class="recon-fig recon-fig-full" loading="lazy" /><span class="recon-fig-note">표·연립 등 복잡한 구조 — 원본 이미지로 표시 (텍스트 재구성 미지원)</span></div>`
    : renderReconstruct(_sText, { figures: figureList, tables: fm.tables, inlineFigures: inlineFigList });
  // 재구성은 어드민 전용: 도형 라벨이 이미지 밖으로 새는 등 엣지케이스가 있어 사용자에겐 부적합 →
  // 사용자는 원본 이미지(<Content/>)만, 재구성 토글·뷰는 admin 만. (디코더의 가치는 인제스트용 searchable_text.)
  const reconHTML = isAdmin ? reconFull : ''; // 빈 문자열=토글/재구성 숨김 → 비어드민은 <Content/> 원본만
  // Gemini 비전 교정 재구성(있으면): 결정론적 reconFull 대신 교정 전사(KaTeX) + bareAxes 도식으로
  // 원본과 동일하게. fixes(교정내역)는 백엔드 보관용 — 프론트 미노출. 선행 번호("13.")는 recon-head 와
  // 중복되므로 제거.
  const gRecon = (reconData as Record<string, any>)[entry.id] ?? null;
  // Gemini 교정본 정리: 선행 번호("13.")·본문 끝 점수([3점], recon-head 에 이미 있음) 제거,
  // $...$ 구분자 제거(renderReconstruct=katex SSOT 는 구분자 없는 형식 기대 — 안 그러면 raw 노출).
  const gClean = gRecon
    ? String(gRecon.corrected || '')
        .replace(/^\s*\d{1,2}\.\s*/, '')
        .replace(/\[\s*\d+\s*점\s*\]/g, '')
        .replace(/\$/g, '')
        .trim()
    : '';
  // 그림 위치를 원본과 동일하게: 수능 객관식은 [문제]→[그림]→[선택지]. 선택지(①~⑤) 경계에서
  // 분리해 그림을 그 사이에 둔다(선택지 없으면 그림이 본문 끝 — 그대로 맞음).
  const _ci = gClean.search(/[①②③④⑤⑥⑦⑧⑨⑩]/);
  const gStmtHtml = (isAdmin && gRecon) ? renderReconstruct(_ci > 0 ? gClean.slice(0, _ci) : gClean, {}) : '';
  const gChoiceHtml = (isAdmin && gRecon && _ci > 0) ? renderReconstruct(gClean.slice(_ci), {}) : '';
  // 'docs/concepts/algebra/근의_공식.md' → 'algebra/근의_공식'
  const fmtPath = (p: string) => p.replace(/^docs\/concepts\//, '').replace(/\.md$/, '');
  const labelOf = (slug: string) => (slug.split('/').pop() ?? slug);
  // 개념 ref 해석: exact id → 그대로, 아니면 정규화 leaf(공백·_ 제거)로 정식 노드 찾기.
  // 해석되면 정식 경로로 링크, 안 되면 평문(깨진 링크 방지). 노드 다이어트로 flat→nested 이동·병합 다수.
  const allConceptsForLink = await getCollection('concepts');
  const conceptIdSet = new Set(allConceptsForLink.map((c) => c.id.normalize('NFC')));
  const conceptLeafKey = (s: string) => (s.split('/').pop() ?? s).normalize('NFC').replace(/[\s_]/g, '').toLowerCase();
  const conceptLeafToId = new Map<string, string>();
  for (const c of allConceptsForLink) { const k = conceptLeafKey(c.id); if (!conceptLeafToId.has(k)) conceptLeafToId.set(k, c.id); }
  const resolveConcept = (ref: string): string | null => {
    const id = fmtPath(ref).normalize('NFC');
    if (conceptIdSet.has(id)) return id;
    return conceptLeafToId.get(conceptLeafKey(id)) ?? null;
  };
  // '단일'(고1·고2·통합형)은 과목 표기 생략 — "2025년 모의고사 9번"처럼.
  const subjLabel = fm.source?.subject && fm.source.subject !== '단일' ? `${fm.source.subject} ` : '';
  const unitTitle = fm.source?.subject
    ? `${yearLabel(fm.source.year, fm.source.exam_type)} ${fm.source.exam_type} ${subjLabel}${fm.source.number}번`
    : entry.id;
  
  // 회차 내 이전/다음 네비게이션. 같은 회차(연도·시험·세션·학년·기관) 전체를 모아
  // 공통(1-22)↔선택(23-30) 경계에서 분기: 공통 마지막 → 선택과목 선택, 선택 첫 → 공통 복귀.
  // 가/나형·단일(검정고시·고1·2)은 공통이 없어 같은 과목 내 선형 이동.
  // 이 문제에 **미리 검증된 3D 도형**이 있는지 — 있으면 학생에게 알린다.
  // 있는 줄 모르면 아무도 안 물어본다(2026-08-14 사장님 지적).
  const { readFigure3D } = await import('./figures-3d');
  const has3D = !!readFigure3D(entry.id);
  const src = fm.source;
  type ProbEntry = Awaited<ReturnType<typeof getCollection<'problems'>>>[number];
  const byNum = (a: ProbEntry, b: ProbEntry) => Number(a.data.source?.number ?? 0) - Number(b.data.source?.number ?? 0);
  const roundAll: ProbEntry[] = src
    ? (await getCollection('problems', (e) => {
        const s = e.data.source;
        return !!s && s.year === src.year && s.exam_type === src.exam_type
          && (s.session ?? '') === (src.session ?? '')
          && (s.grade ?? '') === (src.grade ?? '')
          && (s.agency ?? '') === (src.agency ?? '');
      })).sort(byNum)
    : [];
  const ELECTIVE_ORDER = ['확률과통계', '미적분', '기하'];
  const gongtong = roundAll.filter((e) => e.data.source?.subject === '공통');
  const electiveSubjects = [...new Set(roundAll
    .map((e) => e.data.source?.subject).filter((s): s is string => !!s && s !== '공통'))]
    .sort((a, b) => ((ELECTIVE_ORDER.indexOf(a) + 1) || 99) - ((ELECTIVE_ORDER.indexOf(b) + 1) || 99));
  const hasGongtong = gongtong.length > 0;
  
  let prevEntry: ProbEntry | null = null;
  let nextEntries: ProbEntry[] = [];
  if (src) {
    const isGongtong = src.subject === '공통';
    const subjList = roundAll.filter((e) => e.data.source?.subject === src.subject);
    const i = subjList.findIndex((e) => e.id === entry.id);
    // 이전: 과목 내 앞 문제. 선택 첫 문제(23)면 공통 마지막(22)으로 복귀.
    if (i > 0) prevEntry = subjList[i - 1];
    else if (hasGongtong && !isGongtong && i === 0) prevEntry = gongtong[gongtong.length - 1] ?? null;
    // 다음: 공통 마지막이면 선택과목 분기(각 과목 첫 문제), 아니면 과목 내 다음.
    if (hasGongtong && isGongtong && i === subjList.length - 1) {
      nextEntries = electiveSubjects
        .map((s) => roundAll.filter((e) => e.data.source?.subject === s).sort(byNum)[0])
        .filter((e): e is ProbEntry => !!e);
    } else if (i >= 0 && i < subjList.length - 1) {
      nextEntries = [subjList[i + 1]];
    }
  }

  return {
    id: entry.id,
    data: fm,
    html: emittedHtml(entry.id),
    unitTitle, subjLabel, has3D, isAdmin,
    wholeStem: _wholeStem,
    recon: { html: reconHTML, gStmtHtml, gChoiceHtml, hasGeo: !!(isAdmin && gRecon), geo: isAdmin ? gRecon?.figure ?? null : null, full: reconFull },
    roundNav: {
      prev: prevEntry ? navOf(prevEntry) : null,
      nexts: nextEntries.map(navOf),
      curSubject: src?.subject ?? '',
      currentLabel: `${subjLabel}${src?.number ?? ''}번`,
    },
    concepts: (fm.concepts ?? []).map((p: string) => {
      const resolved = resolveConcept(p);
      return { ref: p, label: labelOf(fmtPath(p)), resolved };
    }),
  };
}

/**
 * 튜터 채팅 헤더용 제목만 — 방출물 **한 건**만 읽는다(컬렉션 전수 조회 없음).
 * `TutorChat` 은 서버 렌더로 남기므로 페이지가 이 값을 알아야 한다.
 */
export function problemTitle(slug: string): string {
  const abs = mediaPath(`/content/problems/${slug}.json`);
  if (!abs) return slug;
  try {
    const s = (JSON.parse(readFileSync(abs, 'utf8')) as { data?: { source?: any } }).data?.source;
    if (!s?.subject) return slug;
    const subj = s.subject !== '단일' ? `${s.subject} ` : '';
    return `${yearLabel(s.year, s.exam_type)} ${s.exam_type} ${subj}${s.number}번`;
  } catch { return slug; }
}
