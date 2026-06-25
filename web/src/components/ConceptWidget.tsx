import type { ComponentType } from 'react';
import { widgetForConcept } from '../lib/concept-widgets';
import SineUnitCircle from './SineUnitCircle';

// 개념 노드 → 인터랙티브 위젯. 메타데이터(매칭·tutorHint)는 lib/concept-widgets.ts 공유 레지스트리(서버=튜터도 사용).
//   여기선 key → React 컴포넌트 매핑만. concept-figures(도식)와 평행한 "노드별 위젯 슬롯".
const COMPONENTS: Record<string, ComponentType> = {
  'sine-unit-circle': SineUnitCircle,
};

export default function ConceptWidget({ conceptId }: { conceptId: string }) {
  const meta = widgetForConcept(conceptId);
  if (!meta) return null;
  const W = COMPONENTS[meta.key];
  if (!W) return null;
  return (
    <div style={{ margin: '24px 0' }}>
      <div style={{ fontSize: 12, color: 'var(--color-muted)', marginBottom: 8, fontWeight: 600, letterSpacing: '0.02em' }}>🔭 개념 탐구 · 인터랙티브</div>
      <W />
    </div>
  );
}
