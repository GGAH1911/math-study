import { useMemo, useState, useCallback, useEffect } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  type NodeMouseHandler,
  Handle,
  Position,
  MarkerType,
  ReactFlowProvider,
  useReactFlow,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

type GraphNode = {
  id: string;
  slug: string;
  label: string;
  concept_type: 'unit' | 'definition' | 'theorem' | 'lemma' | 'example' | string;
  grade: string | null;
  domain: string | null;
  unit: string | null;
  subunit: string | null;
  mastery: 'unknown' | 'learning' | 'proficient' | 'mastered' | string;
  prerequisites: string[];
  enables: string[];
  review_state: string | null;
  next_review: string | null;
  x: number;
  y: number;
};

type GraphEdge = { id: string; source: string; target: string };

type GraphData = {
  generatedAt: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    nodes: number; edges: number; cycles: number;
    byMastery?: Record<string, number>;
    byType?: Record<string, number>;
    byGrade?: Record<string, number>;
  };
};

type Props = {
  data: GraphData;
  variant?: 'mini' | 'full';
  highlight?: string;
};

const MASTERY_COLOR: Record<string, string> = {
  unknown: '#f43f5e',
  learning: '#f59e0b',
  proficient: '#10b981',
  mastered: '#0ea5e9',
};

const TYPE_ICON: Record<string, string> = {
  unit: '◆',
  definition: '○',
  theorem: '◇',
  lemma: '△',
  example: '□',
};

const GRADE_ORDER = ['중1', '중2', '중3', '고1', '수학1', '수학2', '미적분', '기하', '확률과통계'];
const GRADE_COLOR: Record<string, string> = {
  '중1': '#94a3b8',
  '중2': '#64748b',
  '중3': '#475569',
  '고1': '#a78bfa',
  '수학1': '#8b5cf6',
  '수학2': '#7c3aed',
  '미적분': '#6d28d9',
  '기하': '#22d3ee',
  '확률과통계': '#ec4899',
};

const DOMAIN_ORDER = ['수와식', '방정식', '함수', '도형', '확률통계', '논리'];
const DOMAIN_COLOR: Record<string, string> = {
  '수와식':   '#f59e0b',  // amber
  '방정식':   '#ef4444',  // red
  '함수':     '#3b82f6',  // blue (가장 큰 도메인, 메인)
  '도형':     '#22d3ee',  // cyan
  '확률통계': '#ec4899',  // pink
  '논리':     '#a78bfa',  // violet
};

function ConceptNode({ data }: { data: GraphNode & { highlighted?: boolean; dimmed?: boolean; colorMode?: 'domain' | 'mastery' } }) {
  const isUnit = data.concept_type === 'unit';
  const masteryColor = MASTERY_COLOR[data.mastery] ?? '#a1a1aa';
  const domainColor = data.domain ? (DOMAIN_COLOR[data.domain] ?? '#71717a') : '#71717a';
  const gradeColor = data.grade ? (GRADE_COLOR[data.grade] ?? '#71717a') : '#71717a';
  // Primary outline color = domain (학습 본질). Mastery shown as small dot.
  const mode = data.colorMode ?? 'domain';
  const primary = mode === 'domain' ? domainColor : masteryColor;
  return (
    <div
      className="relative"
      style={{
        opacity: data.dimmed ? 0.18 : 1,
        transform: data.highlighted ? 'scale(1.06)' : undefined,
        transition: 'opacity 200ms ease, transform 200ms ease',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ visibility: 'hidden' }} />
      <div
        className="rounded-xl backdrop-blur"
        style={{
          minWidth: isUnit ? 168 : 140,
          padding: isUnit ? '10px 14px' : '8px 12px',
          border: `${isUnit ? 2.5 : 2}px solid ${primary}`,
          background: data.highlighted ? `${primary}30` : '#18181b',
          boxShadow: data.highlighted
            ? `0 0 0 4px ${primary}40, 0 0 24px ${primary}30`
            : isUnit
              ? `0 4px 16px ${primary}25`
              : `0 2px 12px ${primary}20`,
        }}
      >
        <div className="flex items-center justify-between gap-2">
          <span className="text-base leading-none" style={{ color: primary }} title={data.concept_type}>
            {TYPE_ICON[data.concept_type] ?? '·'}
          </span>
          <span
            className="inline-block size-2 rounded-full"
            style={{ background: masteryColor }}
            title={`mastery: ${data.mastery}`}
          />
        </div>
        <div className={`mt-1 font-semibold text-zinc-50 ${isUnit ? 'text-sm' : 'text-xs'}`}>
          {data.label}
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
      <Handle type="source" position={Position.Bottom} style={{ visibility: 'hidden' }} />
    </div>
  );
}

const nodeTypes = { conceptNode: ConceptNode };

function Inner({ data, variant = 'full', highlight }: Props) {
  const [selected, setSelected] = useState<string | null>(highlight ?? null);
  const [masteryFilter, setMasteryFilter] = useState<Set<string>>(
    new Set(['unknown', 'learning', 'proficient', 'mastered']),
  );
  const gradesInData = useMemo(
    () => GRADE_ORDER.filter((g) => data.nodes.some((n) => n.grade === g)),
    [data.nodes],
  );
  const domainsInData = useMemo(
    () => DOMAIN_ORDER.filter((d) => data.nodes.some((n) => n.domain === d)),
    [data.nodes],
  );
  const [gradeFilter, setGradeFilter] = useState<Set<string>>(new Set(gradesInData));
  const [domainFilter, setDomainFilter] = useState<Set<string>>(new Set(domainsInData));
  const [searchTerm, setSearchTerm] = useState('');
  const rf = useReactFlow();

  const filteredIds = useMemo(() => {
    return new Set(
      data.nodes
        .filter((n) => masteryFilter.has(n.mastery))
        .filter((n) => !n.grade || gradeFilter.has(n.grade))
        .filter((n) => !n.domain || domainFilter.has(n.domain))
        .filter((n) => !searchTerm || n.label.includes(searchTerm))
        .map((n) => n.id),
    );
  }, [data.nodes, masteryFilter, gradeFilter, domainFilter, searchTerm]);

  const nodes: Node[] = useMemo(
    () =>
      data.nodes.map((n) => ({
        id: n.id,
        type: 'conceptNode',
        position: { x: n.x, y: n.y },
        data: {
          ...n,
          highlighted: n.id === selected,
          dimmed: !filteredIds.has(n.id),
        },
      })),
    [data.nodes, selected, filteredIds],
  );

  const edges: Edge[] = useMemo(
    () =>
      data.edges.map((e) => {
        const visible = filteredIds.has(e.source) && filteredIds.has(e.target);
        return {
          id: e.id,
          source: e.source,
          target: e.target,
          animated: e.source === selected || e.target === selected,
          style: {
            stroke: visible ? '#52525b' : '#27272a',
            strokeWidth: e.source === selected || e.target === selected ? 2 : 1.5,
            opacity: visible ? 1 : 0.3,
          },
          markerEnd: { type: MarkerType.ArrowClosed, color: '#52525b' },
        };
      }),
    [data.edges, filteredIds, selected],
  );

  // Center-and-zoom helper: smooth pan to a node + comfortable zoom
  const flyTo = useCallback((nodeId: string) => {
    const n = data.nodes.find((x) => x.id === nodeId);
    if (!n) return;
    rf.setCenter(n.x, n.y, { zoom: 1.25, duration: 500 });
  }, [rf, data.nodes]);

  const goto = useCallback((nodeId: string) => {
    setSelected(nodeId);
    flyTo(nodeId);
  }, [flyTo]);

  const onNodeClick: NodeMouseHandler = useCallback((_, node) => {
    goto(node.id);
  }, [goto]);

  useEffect(() => {
    const t = setTimeout(() => {
      if (highlight) {
        goto(highlight);
      } else {
        rf.fitView({ padding: 0.2, duration: 400 });
      }
    }, 50);
    return () => clearTimeout(t);
  }, [rf, highlight, goto]);

  // 검색어가 정확히 한 노드만 매치하면 그리로 이동
  useEffect(() => {
    if (!searchTerm) return;
    const matches = data.nodes.filter((n) => n.label.includes(searchTerm));
    if (matches.length === 1) {
      const id = matches[0].id;
      setSelected(id);
      flyTo(id);
    } else if (matches.length > 1 && matches.length <= 12) {
      // 다수 매치: 매치된 노드들이 다 보이도록 fit
      rf.fitView({ nodes: matches.map((m) => ({ id: m.id })), padding: 0.3, duration: 400 });
    }
  }, [searchTerm, data.nodes, rf, flyTo]);

  // 키보드 단축키 (입력란에 포커스 없을 때만)
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA') {
        if (e.key === 'Escape') (e.target as HTMLElement).blur();
        return;
      }
      if (e.key === 'f') { rf.fitView({ padding: 0.2, duration: 400 }); e.preventDefault(); }
      else if (e.key === 'Escape') { setSelected(null); }
      else if (e.key === '/') {
        const inp = document.querySelector<HTMLInputElement>('.dag-search-input');
        if (inp) { inp.focus(); e.preventDefault(); }
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [rf]);

  const selectedNode = data.nodes.find((n) => n.id === selected);

  // Single-select-with-reset:
  //   default = all selected (전체)
  //   click pill X (when all active or other subset active) → narrow to {X}
  //   click pill X (when only X is active) → back to all
  const ALL_MASTERY = ['unknown', 'learning', 'proficient', 'mastered'] as const;
  const toggleMastery = (m: string) => {
    setMasteryFilter((prev) => {
      if (prev.size === 1 && prev.has(m)) return new Set(ALL_MASTERY);
      return new Set([m]);
    });
  };
  const resetMastery = () => setMasteryFilter(new Set(ALL_MASTERY));

  const toggleGrade = (g: string) => {
    setGradeFilter((prev) => {
      if (prev.size === 1 && prev.has(g)) return new Set(gradesInData);
      return new Set([g]);
    });
  };
  const resetGrade = () => setGradeFilter(new Set(gradesInData));

  const toggleDomain = (d: string) => {
    setDomainFilter((prev) => {
      if (prev.size === 1 && prev.has(d)) return new Set(domainsInData);
      return new Set([d]);
    });
  };
  const resetDomain = () => setDomainFilter(new Set(domainsInData));

  const masteryAllActive = masteryFilter.size === ALL_MASTERY.length;
  const gradeAllActive = gradeFilter.size === gradesInData.length;
  const domainAllActive = domainFilter.size === domainsInData.length;

  return (
    <div className={`relative w-full ${variant === 'mini' ? 'h-[320px]' : 'h-full'}`}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={onNodeClick}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={variant === 'full'}
        nodesConnectable={false}
        elementsSelectable
        fitView
        fitViewOptions={{ padding: 0.2 }}
        defaultEdgeOptions={{ type: 'smoothstep' }}
        minZoom={0.15}
        maxZoom={2.5}
        zoomOnScroll={true}
        panOnScroll={false}
        panOnDrag={true}
        selectionOnDrag={false}
        zoomActivationKeyCode={null}
      >
        <Background gap={20} size={1} color="#27272a" />
        {variant === 'full' && (
          <>
            <Controls position="top-right" showInteractive={false} className="!bg-zinc-900 !border !border-zinc-800" />
            <MiniMap
              position="bottom-right"
              maskColor="rgba(9,9,11,0.7)"
              nodeColor={(n) => MASTERY_COLOR[(n.data as any).mastery] ?? '#a1a1aa'}
              style={{ background: '#18181b', border: '1px solid #27272a' }}
            />
          </>
        )}
      </ReactFlow>

      {variant === 'full' && (
        <>
          {/* Left filter panel */}
          <div className="absolute top-4 left-4 z-10 w-72 card p-3 space-y-3 max-h-[calc(100%-2rem)] overflow-auto">
            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-1">검색 <span className="text-zinc-600 normal-case tracking-normal">(/ 키)</span></label>
              <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="개념 이름…"
                className="dag-search-input w-full px-2 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm focus:outline-none focus:border-indigo-400"
              />
              <p className="mt-1 text-[10px] text-zinc-600">
                f = fit · esc = 닫기 · 노드/링크 클릭 = 자동 이동
              </p>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500">Mastery</label>
                <button
                  onClick={resetMastery}
                  disabled={masteryAllActive}
                  className={`text-[10px] uppercase tracking-wider transition ${
                    masteryAllActive
                      ? 'text-emerald-400 cursor-default'
                      : 'text-zinc-500 hover:text-zinc-100 cursor-pointer'
                  }`}
                >
                  {masteryAllActive ? '● 전체' : '○ 전체로'}
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {(['unknown', 'learning', 'proficient', 'mastered'] as const).map((m) => {
                  const isActive = masteryFilter.has(m);
                  const isSole = masteryFilter.size === 1 && isActive;
                  const color = MASTERY_COLOR[m];
                  return (
                    <button
                      key={m}
                      onClick={() => toggleMastery(m)}
                      className="px-2 py-1 rounded-md text-xs font-medium transition border flex items-center gap-1.5"
                      style={{
                        background: isSole ? `${color}30` : (isActive ? `${color}10` : 'transparent'),
                        borderColor: isSole ? color : (isActive ? `${color}55` : '#27272a'),
                        color: isActive ? color : '#52525b',
                        opacity: !masteryAllActive && !isActive ? 0.4 : 1,
                      }}
                      title={isSole ? '클릭하면 전체로 복귀' : '이것만 보기'}
                    >
                      <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                      <span>{m}</span>
                      <span className="text-zinc-500 font-normal">
                        {data.nodes.filter((n) => n.mastery === m).length}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {domainsInData.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500">도메인 (학습 본질)</label>
                  <button
                    onClick={resetDomain}
                    disabled={domainAllActive}
                    className={`text-[10px] uppercase tracking-wider transition ${
                      domainAllActive
                        ? 'text-emerald-400 cursor-default'
                        : 'text-zinc-500 hover:text-zinc-100 cursor-pointer'
                    }`}
                  >
                    {domainAllActive ? '● 전체' : '○ 전체로'}
                  </button>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {domainsInData.map((d) => {
                    const isActive = domainFilter.has(d);
                    const isSole = domainFilter.size === 1 && isActive;
                    const color = DOMAIN_COLOR[d] ?? '#71717a';
                    return (
                      <button
                        key={d}
                        onClick={() => toggleDomain(d)}
                        className="px-2 py-1 rounded-md text-xs font-medium transition border flex items-center gap-1.5"
                        style={{
                          background: isSole ? `${color}30` : (isActive ? `${color}10` : 'transparent'),
                          borderColor: isSole ? color : (isActive ? `${color}55` : '#27272a'),
                          color: isActive ? color : '#52525b',
                          opacity: !domainAllActive && !isActive ? 0.4 : 1,
                        }}
                        title={isSole ? '클릭하면 전체로 복귀' : '이 도메인만 보기'}
                      >
                        <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                        <span>{d}</span>
                        <span className="text-zinc-500 font-normal">
                          {data.nodes.filter((n) => n.domain === d).length}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {gradesInData.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500">학년 (보조)</label>
                  <button
                    onClick={resetGrade}
                    disabled={gradeAllActive}
                    className={`text-[10px] uppercase tracking-wider transition ${
                      gradeAllActive
                        ? 'text-emerald-400 cursor-default'
                        : 'text-zinc-500 hover:text-zinc-100 cursor-pointer'
                    }`}
                  >
                    {gradeAllActive ? '● 전체' : '○ 전체로'}
                  </button>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {gradesInData.map((g) => {
                    const isActive = gradeFilter.has(g);
                    const isSole = gradeFilter.size === 1 && isActive;
                    const color = GRADE_COLOR[g] ?? '#71717a';
                    return (
                      <button
                        key={g}
                        onClick={() => toggleGrade(g)}
                        className="px-2 py-1 rounded-md text-xs font-medium transition border flex items-center gap-1.5"
                        style={{
                          background: isSole ? `${color}30` : (isActive ? `${color}10` : 'transparent'),
                          borderColor: isSole ? color : (isActive ? `${color}55` : '#27272a'),
                          color: isActive ? color : '#52525b',
                          opacity: !gradeAllActive && !isActive ? 0.4 : 1,
                        }}
                        title={isSole ? '클릭하면 전체로 복귀' : '이 학년만 보기'}
                      >
                        <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                        <span>{g}</span>
                        <span className="text-zinc-500 font-normal">
                          {data.nodes.filter((n) => n.grade === g).length}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
            <div className="text-[11px] text-zinc-500 pt-2 border-t border-zinc-800">
              <div className="flex justify-between">
                <span>nodes</span><span className="font-mono">{data.stats.nodes}</span>
              </div>
              <div className="flex justify-between">
                <span>edges</span><span className="font-mono">{data.stats.edges}</span>
              </div>
              <div className="flex justify-between">
                <span>cycles</span>
                <span className={`font-mono ${data.stats.cycles > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {data.stats.cycles}
                </span>
              </div>
            </div>
          </div>

          {/* Right detail panel */}
          {selectedNode && (
            <div className="absolute top-4 right-4 z-10 w-72 card p-4 space-y-3">
              <header className="flex items-center justify-between">
                <h3 className="text-sm font-semibold">{selectedNode.label}</h3>
                <button onClick={() => setSelected(null)} className="text-zinc-500 hover:text-zinc-100 text-lg leading-none">×</button>
              </header>
              <div className="flex gap-1.5 flex-wrap">
                <span className={`chip chip-mastery-${selectedNode.mastery}`}>{selectedNode.mastery}</span>
                <span className="chip">{selectedNode.concept_type}</span>
                {selectedNode.domain && (
                  <span
                    className="chip"
                    style={{
                      color: DOMAIN_COLOR[selectedNode.domain] ?? '#a1a1aa',
                      borderColor: `${DOMAIN_COLOR[selectedNode.domain] ?? '#a1a1aa'}55`,
                    }}
                  >
                    {selectedNode.domain}
                  </span>
                )}
                {selectedNode.grade && (
                  <span
                    className="chip"
                    style={{
                      color: GRADE_COLOR[selectedNode.grade] ?? '#a1a1aa',
                      borderColor: `${GRADE_COLOR[selectedNode.grade] ?? '#a1a1aa'}55`,
                    }}
                  >
                    {selectedNode.grade}
                  </span>
                )}
                {selectedNode.review_state && <span className="chip">review: {selectedNode.review_state}</span>}
              </div>
              {selectedNode.prerequisites.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1">선수 (prerequisites)</div>
                  <ul className="text-sm space-y-0.5">
                    {selectedNode.prerequisites.map((p) => (
                      <li key={p}>
                        <button
                          onClick={() => goto(p)}
                          className="text-indigo-400 hover:underline text-left"
                        >{p}</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {selectedNode.enables.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1">enables</div>
                  <ul className="text-sm space-y-0.5">
                    {selectedNode.enables.map((p) => (
                      <li key={p}>
                        <button
                          onClick={() => goto(p)}
                          className="text-indigo-400 hover:underline text-left"
                        >{p}</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <a
                href={`/concepts/${encodeURIComponent(selectedNode.slug)}`}
                className="block text-center mt-2 px-3 py-2 rounded-md bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-sm font-medium transition"
              >
                상세 페이지 →
              </a>
            </div>
          )}

          {/* Legend bottom-left */}
          <div className="absolute bottom-4 left-4 z-10 card px-3 py-2 text-xs">
            <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1.5">노드 모양</div>
            <div className="flex gap-3 text-zinc-300">
              {(['definition', 'theorem', 'lemma', 'example'] as const).map((t) => (
                <span key={t} className="flex items-center gap-1">
                  <span className="text-base">{TYPE_ICON[t]}</span>
                  <span>{t}</span>
                </span>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default function ConceptDAG(props: Props) {
  return (
    <ReactFlowProvider>
      <Inner {...props} />
    </ReactFlowProvider>
  );
}
