// 개념 노드 → 인터랙티브 위젯 레지스트리 (서버/클라 공유 데이터, React 의존 없음).
//   - ConceptWidget.tsx(클라): key로 컴포넌트 렌더.
//   - chat-context.ts(서버): tutorHint를 튜터 시스템프롬프트에 주입 → 튜터가 위젯 존재를 인지하고 안내.
//   매칭은 leaf(파일명) NFC ([[project_concept_normalization]] 흔들림 회피).
import widgetIndex from '../data/concept-widgets-index.json';

export type ConceptWidgetMeta = {
  leaf: string;       // 개념 id 끝 매칭(파일명)
  key: string;        // ConceptWidget 컴포넌트 맵 키
  label: string;      // 학생/튜터에게 보일 이름
  tutorHint: string;  // 튜터가 위젯을 활용해 안내하도록 주입되는 설명
};

export const CONCEPT_WIDGETS: ConceptWidgetMeta[] = [
  {
    leaf: '삼각비의_정의',
    key: 'sine-unit-circle',
    label: '단위원·삼각비(활시위) 인터랙티브',
    tutorHint:
      '단위원과 직각삼각형에서 학생이 각도 θ를 드래그하면 실시간으로 변합니다. 위젯의 색: 사인(=활시위의 절반=반현)=초록 세로선, 코사인=파란 가로선, 탄젠트=빨간 선, 활(호)=주황 호. 사인이 왜 "활시위(현)의 절반"인지, θ가 커질수록 각 값이 어떻게 변하는지 눈으로 확인할 수 있습니다. (색을 학생에게 정확히 알려주세요.)',
  },
];

const norm = (s: string) => s.normalize('NFC');

export function widgetForConcept(slug: string): ConceptWidgetMeta | null {
  const id = norm(slug);
  return CONCEPT_WIDGETS.find((w) => id.endsWith(norm(w.leaf))) ?? null;
}

// ── SSOT 매니페스트: 인터랙티브 위젯 있는 개념 id 집합(자동생성, 워커풀 --commit이 매일 갱신) ──
const SPEC_WIDGET_IDS = new Set((widgetIndex as string[]).map((s) => s.normalize('NFC')));

/** spec(자동) 또는 bespoke 위젯이 있는 개념인가 — 모든 표면의 🔭 뱃지·필터 공용 판정. */
export function hasWidget(slug: string): boolean {
  const id = norm(slug);
  return SPEC_WIDGET_IDS.has(id) || CONCEPT_WIDGETS.some((w) => id.endsWith(norm(w.leaf)));
}

/** 전체 위젯 개념 id 집합(필터·카운트용). */
export const WIDGET_CONCEPT_IDS = SPEC_WIDGET_IDS;
