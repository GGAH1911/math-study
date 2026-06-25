import type { ComponentType } from 'react';
import { widgetForConcept } from '../lib/concept-widgets';
import type { InteractiveSpec } from '../data/interactive-samples';
import SineUnitCircle from './SineUnitCircle';
import WidgetButton from './WidgetButton';

// 개념 노드 → 인터랙티브 위젯.
//   ① bespoke 손제작 위젯(레지스트리 key→컴포넌트) 우선 — 인라인.
//   ② 없으면 widget_spec_loop가 영속한 InteractiveSpec(prop) → 본문 버튼→모달.
//   메타데이터(매칭·tutorHint)는 lib/concept-widgets.ts(bespoke)·concept-widgets-server.ts(spec) 공유.
const COMPONENTS: Record<string, ComponentType> = {
  'sine-unit-circle': SineUnitCircle,
};

export default function ConceptWidget({ conceptId, spec }: { conceptId: string; spec?: InteractiveSpec | null }) {
  const meta = widgetForConcept(conceptId);
  if (meta && COMPONENTS[meta.key]) {
    const W = COMPONENTS[meta.key];
    return (
      <div style={{ margin: '24px 0' }}>
        <div style={{ fontSize: 12, color: 'var(--color-muted)', marginBottom: 8, fontWeight: 600, letterSpacing: '0.02em' }}>🔭 개념 탐구 · 인터랙티브</div>
        <W />
      </div>
    );
  }
  if (spec) return <WidgetButton spec={spec} />;
  return null;
}
