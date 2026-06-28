// ConceptDAG 노드 렌더 컴포넌트 — 분리(JSX 그대로). ReactFlow 의 conceptNode 타입.
import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { GraphNode, ColorMode } from '../lib/dag-types';
import { hasWidget } from '../lib/concept-widgets';
import { MASTERY_COLOR, TYPE_LABEL_KO, TYPE_ICON, GRADE_COLOR, DOMAIN_COLOR } from '../lib/concept-meta';

function ConceptNodeImpl({ data }: { data: GraphNode & {
  highlighted?: boolean;
  filterDimmed?: boolean;   // excluded by mastery/grade/domain filter → aggressive dim
  focusDimmed?: boolean;    // not related to current selection → soft dim, stays readable
  colorMode?: ColorMode;
  childCount?: number; expanded?: boolean;
  onToggleExpand?: (id: string) => void;
} }) {
  const isUnit = data.concept_type === 'unit';
  const masteryColor = MASTERY_COLOR[data.mastery] ?? '#a1a1aa';
  const domainColor = data.domain ? (DOMAIN_COLOR[data.domain] ?? '#71717a') : '#71717a';
  const gradeColor = data.grade ? (GRADE_COLOR[data.grade] ?? '#71717a') : '#71717a';
  const mode: ColorMode = data.colorMode ?? 'domain';
  const primary =
    mode === 'mastery' ? masteryColor :
    mode === 'grade'   ? gradeColor :
                         domainColor;
  // Filter-dim wins over focus-dim (excluded nodes stay clearly excluded).
  const opacity = data.filterDimmed ? 0.10 : (data.focusDimmed ? 0.35 : 1);
  return (
    <div
      className="relative"
      style={{ opacity, transition: 'opacity 200ms ease' }}
    >
      <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} />
      <div
        className="rounded-xl"
        style={{
          minWidth: isUnit ? 168 : 140,
          padding: isUnit ? '10px 14px' : '8px 12px',
          border: `${isUnit ? (data.highlighted ? 4 : 2.5) : (data.highlighted ? 3 : 2)}px solid ${primary}`,
          // 노드 배경·라벨은 짝이 맞는 테마 토큰으로(라이트=종이/잉크·다크=흑연/초크).
          // 옛 '#18181b' 검정 하드코딩은 라이트 카드(홈 mini)·라이트 테마에서 라벨(zinc-50,
          // .react-flow 흑판 스코프가 초크로 강제)과 명도 충돌해 라벨이 사라졌다.
          background: data.highlighted ? `${primary}22` : 'var(--color-surface)',
        }}
      >
        <div className="flex items-center justify-between gap-2">
          <span className="text-base leading-none" style={{ color: primary }}
                title={TYPE_LABEL_KO[data.concept_type] ?? '기타'}>
            {TYPE_ICON[data.concept_type] ?? '·'}
          </span>
          <div className="flex items-center gap-1.5">
            {isUnit && typeof data.childCount === 'number' && data.childCount > 0 && (
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); data.onToggleExpand?.(data.id); }}
                onDoubleClick={(e) => e.stopPropagation()}
                className="text-[11px] font-mono px-2 py-0.5 rounded-full hover:scale-105 transition cursor-pointer leading-none"
                style={{
                  background: data.expanded ? `${primary}40` : 'var(--color-surface-2)',
                  color: data.expanded ? primary : 'var(--color-muted)',
                  border: `1px solid ${data.expanded ? primary : 'var(--color-border)'}`,
                }}
                title={data.expanded ? `접기 (${data.childCount}개 spoke)` : `펼치기 (${data.childCount}개 spoke)`}
              >
                {data.expanded ? '−' : '+'} {data.childCount}
              </button>
            )}
            {data.note_count != null && data.note_count > 0 && (
              // 학습 노트(syntheses) 카운트 — 클릭하면 컨셉 페이지로 점프해
              // 우측 사이드바의 "저장된 노트" 섹션에서 목록 확인 가능.
              <a
                href={`/concepts/${data.id}`}
                onClick={(e) => e.stopPropagation()}
                onDoubleClick={(e) => e.stopPropagation()}
                title={`${data.note_count}개 저장된 노트 → 컨셉 페이지로`}
                className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 hover:bg-amber-500/30 transition leading-none cursor-pointer"
              >🗒{data.note_count}</a>
            )}
            {hasWidget(data.id) && (
              <span
                className="text-[10px] px-1.5 py-0.5 rounded-full leading-none"
                style={{ background: 'color-mix(in oklab, var(--color-accent) 18%, transparent)', color: 'var(--color-accent)', border: '1px solid color-mix(in srgb, var(--color-accent) 40%, var(--color-border))' }}
                title="인터랙티브 위젯 있음"
              >🔭</span>
            )}
            <span
              className="inline-block size-2 rounded-full"
              style={{ background: masteryColor }}
              title={`mastery: ${data.mastery}`}
            />
          </div>
        </div>
        <div className={`mt-1 font-semibold text-[color:var(--color-text)] ${isUnit ? 'text-sm' : 'text-xs'}`}>
          {data.label.replace(/_/g, ' ')}
        </div>
        <div className="mt-1.5 flex gap-1 flex-wrap">
          {data.domain && (
            <span
              className="text-[9px] font-medium px-1.5 py-0.5 rounded"
              style={{ background: `${domainColor}25`, color: domainColor }}
            >
              {data.domain}
            </span>
          )}
          {data.grade && (
            <span
              className="text-[9px] font-medium px-1.5 py-0.5 rounded opacity-70"
              style={{ background: `${gradeColor}20`, color: gradeColor }}
            >
              {data.grade}
            </span>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} />
    </div>
  );
}

const ConceptNode = memo(ConceptNodeImpl);
export const nodeTypes = { conceptNode: ConceptNode };
