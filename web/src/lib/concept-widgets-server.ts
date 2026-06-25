// 서버 전용(fs): 개념 id → widget_spec_loop가 영속한 InteractiveSpec.
//   astro([...slug])와 chat-context(튜터)가 함께 사용. 클라(ConceptWidget)는 prop으로 spec을 받음.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import type { InteractiveSpec } from '../data/interactive-samples';
import { widgetForConcept } from './concept-widgets';

const DIR = fileURLToPath(new URL('../data/concept-widgets', import.meta.url));
const safe = (id: string) => id.replace(/\//g, '__');

export type ConceptSpec = { spec: InteractiveSpec; title: string; params: string[] };

export function loadConceptSpec(conceptId: string): ConceptSpec | null {
  for (const id of [conceptId, conceptId.normalize('NFC'), conceptId.normalize('NFD')]) {
    const p = `${DIR}/${safe(id)}.json`;
    if (existsSync(p)) {
      try {
        const o = JSON.parse(readFileSync(p, 'utf8'));
        if (o?.spec) return { spec: o.spec, title: o.spec.title ?? '', params: (o.spec.params ?? []).map((x: { label?: string; name: string }) => x.label ?? x.name) };
      } catch { /* skip malformed */ }
    }
  }
  return null;
}

// 튜터(chat-context)가 위젯 존재를 인지하도록 통합 메타 제공: bespoke 우선, 없으면 spec 위젯.
export function tutorWidgetMeta(conceptId: string): { label: string; tutorHint: string } | null {
  const bespoke = widgetForConcept(conceptId);
  if (bespoke) return { label: bespoke.label, tutorHint: bespoke.tutorHint };
  const s = loadConceptSpec(conceptId);
  if (s) return {
    label: `${s.title || '개념 시각화'} 인터랙티브`,
    tutorHint: `본문에 **🔭 인터랙티브로 탐구하기** 버튼이 있고, 누르면 ${s.params.join('·') || '슬라이더'}로 조작하는 모달이 뜹니다. 학생이 시각적 이해가 필요하거나 막힐 때, (이 튜터는 도형을 직접 못 그리니) 큰 모델 권유 대신 "본문의 '인터랙티브로 탐구하기' 버튼을 눌러 ___ 슬라이더를 움직여 ___ 를 확인해보세요" 처럼 그 위젯을 직접 조작하도록 구체적으로 안내하고, 무엇을 보게 될지 짚어 주세요.`,
  };
  return null;
}
