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
  concept_type: 'definition' | 'theorem' | 'lemma' | 'example' | string;
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
  stats: { nodes: number; edges: number; cycles: number };
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
  definition: '○',
  theorem: '◇',
  lemma: '△',
  example: '□',
};

function ConceptNode({ data }: { data: GraphNode & { highlighted?: boolean; dimmed?: boolean } }) {
  const color = MASTERY_COLOR[data.mastery] ?? '#a1a1aa';
  return (
    <div
      className="relative"
      style={{
        opacity: data.dimmed ? 0.25 : 1,
        transform: data.highlighted ? 'scale(1.05)' : undefined,
        transition: 'opacity 200ms ease, transform 200ms ease',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ visibility: 'hidden' }} />
      <div
        className="rounded-lg px-3 py-2 min-w-[140px] border-2 backdrop-blur"
        style={{
          borderColor: color,
          background: data.highlighted ? `${color}30` : '#18181b',
          boxShadow: data.highlighted ? `0 0 0 4px ${color}40` : `0 2px 12px ${color}20`,
        }}
      >
        <div className="flex items-center justify-between gap-2">
          <span
            className="text-base"
            style={{ color }}
            title={`${data.concept_type}`}
          >
            {TYPE_ICON[data.concept_type] ?? '·'}
          </span>
          <span
            className="text-[10px] uppercase tracking-wider font-medium"
            style={{ color }}
          >
            {data.mastery}
          </span>
        </div>
        <div className="mt-1 text-sm font-semibold text-zinc-50">{data.label}</div>
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
  const [searchTerm, setSearchTerm] = useState('');
  const rf = useReactFlow();

  const filteredIds = useMemo(() => {
    return new Set(
      data.nodes
        .filter((n) => masteryFilter.has(n.mastery))
        .filter((n) => !searchTerm || n.label.includes(searchTerm))
        .map((n) => n.id),
    );
  }, [data.nodes, masteryFilter, searchTerm]);

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

  const onNodeClick: NodeMouseHandler = useCallback((_, node) => {
    setSelected(node.id);
  }, []);

  useEffect(() => {
    const t = setTimeout(() => {
      rf.fitView({ padding: 0.2, duration: 400 });
    }, 50);
    return () => clearTimeout(t);
  }, [rf]);

  const selectedNode = data.nodes.find((n) => n.id === selected);

  const toggleMastery = (m: string) => {
    setMasteryFilter((prev) => {
      const next = new Set(prev);
      if (next.has(m)) next.delete(m); else next.add(m);
      return next;
    });
  };

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
        minZoom={0.3}
        maxZoom={2.5}
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
          <div className="absolute top-4 left-4 z-10 w-60 card p-3 space-y-3 max-h-[calc(100%-2rem)] overflow-auto">
            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-1">검색</label>
              <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="개념 이름…"
                className="w-full px-2 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-2">Mastery 필터</label>
              <div className="space-y-1">
                {(['unknown', 'learning', 'proficient', 'mastered'] as const).map((m) => (
                  <label key={m} className="flex items-center gap-2 text-sm cursor-pointer hover:text-zinc-100 transition">
                    <input
                      type="checkbox"
                      checked={masteryFilter.has(m)}
                      onChange={() => toggleMastery(m)}
                      className="accent-indigo-400"
                    />
                    <span
                      className="inline-block size-2 rounded-full"
                      style={{ background: MASTERY_COLOR[m] }}
                    />
                    <span className="text-zinc-300">{m}</span>
                    <span className="ml-auto text-xs text-zinc-500">
                      {data.nodes.filter((n) => n.mastery === m).length}
                    </span>
                  </label>
                ))}
              </div>
            </div>
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
                {selectedNode.review_state && <span className="chip">review: {selectedNode.review_state}</span>}
              </div>
              {selectedNode.prerequisites.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1">선수 (prerequisites)</div>
                  <ul className="text-sm space-y-0.5">
                    {selectedNode.prerequisites.map((p) => (
                      <li key={p}>
                        <button
                          onClick={() => setSelected(p)}
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
                          onClick={() => setSelected(p)}
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
