import type { ComponentType } from 'react';
import SineUnitCircle from './SineUnitCircle';

// 개념 노드 → 인터랙티브 위젯 레지스트리. concept-figures(도식)와 평행한 "노드별 위젯 슬롯".
//   매칭은 leaf(파일명) NFC 기준 — 경로/한글 정규화 흔들림 회피([[project_concept_normalization]] 교훈).
//   향후: 개념 id별 위젯 추가(단위원/삼각비, 함수그래퍼, 넓이누적, 접선기울기 …). config는 추후 concept-widgets.json.
const norm = (s: string) => s.normalize('NFC');
const REGISTRY: Array<{ leaf: string; W: ComponentType }> = [
  { leaf: '삼각비의_정의', W: SineUnitCircle },
];

export default function ConceptWidget({ conceptId }: { conceptId: string }) {
  const id = norm(conceptId);
  const hit = REGISTRY.find((r) => id.endsWith(norm(r.leaf)));
  if (!hit) return null;
  const W = hit.W;
  return (
    <div style={{ margin: '24px 0' }}>
      <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 8, fontWeight: 600, letterSpacing: '0.02em' }}>🔭 개념 탐구 · 인터랙티브</div>
      <W />
    </div>
  );
}
