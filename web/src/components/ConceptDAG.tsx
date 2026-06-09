import { useMemo, useState, useCallback, useEffect, useRef, memo } from 'react';
import dagre from 'dagre';
import {
  ReactFlow,
  Background,
  Controls,
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
import {
  MASTERY_COLOR,
  TYPE_LABEL_KO,
  TYPE_ICON,
  GRADE_ORDER,
  GRADE_COLOR,
  DOMAIN_ORDER,
  DOMAIN_COLOR,
} from '../lib/concept-meta';

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
  // graph.astro 에서 syntheses-by-concept 인덱스로 주입. 0이면 배지 미노출.
  note_count?: number;
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

// 검색 매칭용 정규화: 한글 NFC(맥/아이패드는 NFD 입력 가능) + 소문자(ASCII 라벨).
// 라벨과 질의 양쪽에 동일 적용해 NFD 질의·대소문자 불일치로 인한 0건 매칭을 방지.
const searchNorm = (s: string): string => s.normalize('NFC').toLowerCase();

// Edge color is keyed off the *other* node's concept_type — i.e. when
// the user selects a unit, every line leading to a 정의 is blue, to a
// 정리 is purple, to a 예제 is pink, etc. Makes it visible at a glance
// what kind of spoke is downstream. Graph-only, so it lives here.
const TYPE_EDGE_COLOR: Record<string, string> = {
  definition: '#60a5fa', // blue-400
  theorem:    '#c084fc', // purple-400
  lemma:      '#fbbf24', // amber-400
  example:    '#fb7185', // rose-400
  unit:       '#2dd4bf', // teal-400
};
// Column order when laying out a unit's expanded spokes: definitions
// first (학습 흐름의 시작), then theorems, lemmas, examples last.
const TYPE_COL_ORDER: string[] = ['definition', 'theorem', 'lemma', 'example'];

type ColorMode = 'domain' | 'mastery' | 'grade';

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
          background: data.highlighted ? `${primary}30` : '#18181b',
        }}
      >
        <div className="flex items-center justify-between gap-2">
          <span className="text-base leading-none" style={{ color: primary }}
                title={`${TYPE_LABEL_KO[data.concept_type] ?? '기타'} (${data.concept_type})`}>
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
                  background: data.expanded ? `${primary}40` : '#27272a',
                  color: data.expanded ? primary : '#d4d4d8',
                  border: `1px solid ${data.expanded ? primary : '#3f3f46'}`,
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
            <span
              className="inline-block size-2 rounded-full"
              style={{ background: masteryColor }}
              title={`mastery: ${data.mastery}`}
            />
          </div>
        </div>
        <div className={`mt-1 font-semibold text-zinc-50 ${isUnit ? 'text-sm' : 'text-xs'}`}>
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
const nodeTypes = { conceptNode: ConceptNode };
const FIT_VIEW_OPTIONS = { padding: 0.2 };
// React Flow's `default` edge type IS bezier — it curves around nodes
// more gracefully than `smoothstep`, which liked to right-angle straight
// through unrelated nodes and made it look like A was connected to B
// when it wasn't.
const DEFAULT_EDGE_OPTIONS = { type: 'default' as const };

// Re-layout the visible subset of the graph with dagre so collapsed-only
// (unit-only) view doesn't leave nodes scattered at their original (full-
// graph) coordinates.
function dagreLayout(
  visibleNodes: GraphNode[],
  visibleEdges: GraphEdge[],
): Map<string, { x: number; y: number }> {
  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: 'LR',
    nodesep: 120,
    ranksep: 240,
    edgesep: 40,
    marginx: 60,
    marginy: 60,
  });
  g.setDefaultEdgeLabel(() => ({}));
  for (const n of visibleNodes) {
    const isUnit = n.concept_type === 'unit';
    // Allow per-node width/height override (used to reserve grid space
    // for an expanded unit's spoke cluster).
    const w = (n as unknown as { _width?: number })._width
      ?? (isUnit ? 200 : 160);
    const h = (n as unknown as { _height?: number })._height
      ?? (isUnit ? 80 : 64);
    g.setNode(n.id, { width: w, height: h });
  }
  for (const e of visibleEdges) {
    if (g.hasNode(e.source) && g.hasNode(e.target)) g.setEdge(e.source, e.target);
  }
  dagre.layout(g);
  const out = new Map<string, { x: number; y: number }>();
  for (const n of visibleNodes) {
    const node = g.node(n.id);
    if (node) out.set(n.id, { x: node.x, y: node.y });
  }
  return out;
}

function Inner({ data, variant = 'full', highlight }: Props) {
  // graph.astro uses prerender=true, which means Astro.url.searchParams
  // isn't read per-request — so the `highlight` prop from the server is
  // always undefined. Fall back to reading the URL on the client.
  const effectiveHighlight = useMemo(() => {
    if (highlight) return highlight;
    if (typeof window === 'undefined') return undefined;
    const p = new URLSearchParams(window.location.search);
    return p.get('highlight') ?? p.get('node') ?? undefined;
  }, [highlight]);
  const [selected, setSelected] = useState<string | null>(effectiveHighlight ?? null);
  // opt-in: 빈 Set = 전체(필터 없음). 클릭으로 좁힌다.
  const [masteryFilter, setMasteryFilter] = useState<Set<string>>(new Set());
  const gradesInData = useMemo(
    () => GRADE_ORDER.filter((g) => data.nodes.some((n) => n.grade === g)),
    [data.nodes],
  );
  const domainsInData = useMemo(
    () => DOMAIN_ORDER.filter((d) => data.nodes.some((n) => n.domain === d)),
    [data.nodes],
  );
  const [gradeFilter, setGradeFilter] = useState<Set<string>>(new Set());
  const [domainFilter, setDomainFilter] = useState<Set<string>>(new Set());
  // "노트 있음" 토글 — true면 note_count>0 인 노드만 visible로 인정.
  const [notesOnly, setNotesOnly] = useState<boolean>(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedTerm, setDebouncedTerm] = useState('');
  const [colorBy, setColorBy] = useState<ColorMode>('domain');
  // Collapsed-by-default: only unit nodes show until the user expands one.
  // Set of unit ids whose direct-prereq spokes are visible.
  const [expandedUnits, setExpandedUnits] = useState<Set<string>>(() => new Set());
  const [collapseMode, setCollapseMode] = useState<boolean>(true);
  const rf = useReactFlow();

  // Map each spoke to its "home unit": the first unit reached by walking
  // its prerequisites chain. Computed once per data load.
  const homeUnitOf = useMemo(() => {
    const byId = new Map(data.nodes.map((n) => [n.id, n]));
    const cache = new Map<string, string | null>();
    const resolve = (id: string, seen: Set<string> = new Set()): string | null => {
      if (cache.has(id)) return cache.get(id)!;
      if (seen.has(id)) return null;
      seen.add(id);
      const n = byId.get(id);
      if (!n) return null;
      if (n.concept_type === 'unit') { cache.set(id, id); return id; }
      for (const ref of n.prerequisites ?? []) {
        const r = resolve(ref, seen);
        if (r) { cache.set(id, r); return r; }
      }
      cache.set(id, null);
      return null;
    };
    const out = new Map<string, string | null>();
    for (const n of data.nodes) out.set(n.id, resolve(n.id));
    return out;
  }, [data.nodes]);

  // Reusable toggle — bound to the inline +/− button on each unit and
  // also fired by double-clicking the whole unit node. Defined here
  // (before nodes useMemo) so the memo callback can reference it.
  const toggleExpand = useCallback((unitId: string) => {
    setExpandedUnits((prev) => {
      const next = new Set(prev);
      if (next.has(unitId)) next.delete(unitId);
      else next.add(unitId);
      return next;
    });
  }, []);

  // Pre-compute spoke count per unit (for the "+N" badge).
  const spokeCountByUnit = useMemo(() => {
    const c = new Map<string, number>();
    for (const n of data.nodes) {
      if (n.concept_type === 'unit') continue;
      const u = homeUnitOf.get(n.id);
      if (u) c.set(u, (c.get(u) ?? 0) + 1);
    }
    return c;
  }, [data.nodes, homeUnitOf]);

  // Group spokes by their home unit once. Position calc and per-unit
  // queries can read from this Map instead of re-filtering data.nodes
  // every time a filter changes.
  const spokesByUnit = useMemo(() => {
    const m = new Map<string, GraphNode[]>();
    for (const n of data.nodes) {
      if (n.concept_type === 'unit') continue;
      const u = homeUnitOf.get(n.id);
      if (!u) continue;
      let arr = m.get(u);
      if (!arr) { arr = []; m.set(u, arr); }
      arr.push(n);
    }
    return m;
  }, [data.nodes, homeUnitOf]);

  // id → node lookup. Used by edges/positions/goto; avoids repeated
  // O(n) data.nodes.find() calls.
  const nodeById = useMemo(
    () => new Map(data.nodes.map((n) => [n.id, n])),
    [data.nodes],
  );

  const allUnitIds = useMemo(() =>
    data.nodes.filter((n) => n.concept_type === 'unit').map((n) => n.id),
    [data.nodes]);

  useEffect(() => {
    const t = setTimeout(() => setDebouncedTerm(searchTerm), 200);
    return () => clearTimeout(t);
  }, [searchTerm]);

  // Search auto-expands the matching spoke's home unit so it's actually
  // visible. Computed separately from the user-toggled expansion set.
  const searchAutoExpanded = useMemo(() => {
    if (!debouncedTerm) return new Set<string>();
    const term = searchNorm(debouncedTerm);
    const out = new Set<string>();
    for (const n of data.nodes) {
      if (searchNorm(n.label).includes(term)) {
        const u = homeUnitOf.get(n.id);
        if (u) out.add(u);
      }
    }
    return out;
  }, [debouncedTerm, data.nodes, homeUnitOf]);

  const filteredIds = useMemo(() => {
    const effectiveExpanded = new Set([...expandedUnits, ...searchAutoExpanded]);
    const term = debouncedTerm ? searchNorm(debouncedTerm) : '';
    return new Set(
      data.nodes
        .filter((n) => masteryFilter.size === 0 || masteryFilter.has(n.mastery))
        .filter((n) => gradeFilter.size === 0 || !n.grade || gradeFilter.has(n.grade))
        .filter((n) => domainFilter.size === 0 || !n.domain || domainFilter.has(n.domain))
        .filter((n) => !term || searchNorm(n.label).includes(term))
        // "노트 있음" 토글: 노트 카운트가 있는 노드만 통과. 단원도 동일
        // 기준으로 dim — 노트 없는 단원도 어차피 흥미 없으니 일관 처리.
        .filter((n) => !notesOnly || (n.note_count ?? 0) > 0)
        .filter((n) => {
          if (!collapseMode) return true;
          if (n.concept_type === 'unit') return true;
          const u = homeUnitOf.get(n.id);
          // home unit 없는 orphan spoke(301개): 무검색 접기뷰에선 숨김(기존 동작)이되,
          // 검색 중이면 노출 — 그래야 정확히 검색해도 영영 안 보이는 문제 해소.
          // (검색 매칭은 위 373줄 search 필터에서 이미 통과한 노드만 여기 옴)
          if (!u) return !!term;
          return effectiveExpanded.has(u);
        })
        .map((n) => n.id),
    );
  }, [data.nodes, masteryFilter, gradeFilter, domainFilter, debouncedTerm,
      collapseMode, expandedUnits, searchAutoExpanded, homeUnitOf, notesOnly]);

  // When a node is selected, compute the set of nodes that are *related*
  // (the selected node + every direct prereq / enables target). Other
  // nodes get heavily dimmed so the user can read the relationship
  // without the whole canvas competing for attention.
  const relatedToSelected = useMemo(() => {
    if (!selected) return null;            // null = "no focus mode"
    const out = new Set<string>([selected]);
    for (const e of data.edges) {
      if (e.source === selected) out.add(e.target);
      else if (e.target === selected) out.add(e.source);
    }
    return out;
  }, [selected, data.edges]);

  // When collapse mode is on:
  //   1. Run dagre on the visible *units only* — laying out spoke nodes
  //      with dagre alongside is fine for tens of spokes but breaks down
  //      at 100+ (the column for the unit gets monstrously tall).
  //   2. For each expanded unit, place its spoke nodes in a typed grid
  //      to the right of the unit. Columns = {정의, 정리, 보조정리, 예제},
  //      each column wraps after MAX_ROWS rows into another sub-column.
  //      Layout is deterministic and dense, so even units with 165 spokes
  //      fit in roughly 4 cols × 40 rows of compact tiles.
  // Grid metrics shared between unit box sizing and spoke placement.
  const COL_W = 240;
  const ROW_H = 130;
  const MAX_ROWS = 9;
  const UNIT_W = 200;
  const UNIT_MARGIN = 100;

  // Unit-level dagre layout. Independent of filters — only re-runs when
  // the graph data, the set of expanded units, or search-driven expansion
  // changes. Filter toggles (mastery/grade/domain) leave this cache alone.
  const unitLayout = useMemo(() => {
    const unitNodes = data.nodes.filter((n) => n.concept_type === 'unit');
    const uSet = new Set(unitNodes.map((n) => n.id));
    const expandedSet = new Set([...expandedUnits, ...searchAutoExpanded]);

    const sizedUnits = unitNodes.map((u) => {
      if (!expandedSet.has(u.id)) return u;
      const spokes = spokesByUnit.get(u.id) ?? [];
      const byType: Record<string, number> = {};
      for (const s of spokes) byType[s.concept_type] = (byType[s.concept_type] ?? 0) + 1;
      let totalCols = 0;
      for (const t of TYPE_COL_ORDER) {
        const n = byType[t] ?? 0;
        totalCols += Math.max(0, Math.ceil(n / MAX_ROWS));
      }
      const cols = Math.max(1, totalCols);
      const tallestCol = Math.min(MAX_ROWS, Math.max(1, ...Object.values(byType)));
      const w = UNIT_W + UNIT_MARGIN + cols * COL_W + 40;
      const h = Math.max(80, tallestCol * ROW_H + 60);
      return { ...u, _width: w, _height: h, _cols: cols } as GraphNode & {
        _width?: number; _height?: number; _cols?: number;
      };
    });

    const unitEdges = data.edges.filter((e) => uSet.has(e.source) && uSet.has(e.target));
    const dagrePositions = dagreLayout(
      sizedUnits as unknown as GraphNode[],
      unitEdges,
    );
    const sizedById = new Map(sizedUnits.map((u) => [u.id, u]));

    return { unitNodes, expandedSet, dagrePositions, sizedById };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data.nodes, data.edges, expandedUnits, searchAutoExpanded, spokesByUnit]);

  const positions = useMemo(() => {
    if (!collapseMode) {
      const m = new Map<string, { x: number; y: number }>();
      for (const n of data.nodes) m.set(n.id, { x: n.x, y: n.y });
      return m;
    }

    const { unitNodes, expandedSet, dagrePositions, sizedById } = unitLayout;
    const out = new Map<string, { x: number; y: number }>();

    for (const u of unitNodes) {
      const dagreCenter = dagrePositions.get(u.id);
      if (!dagreCenter) continue;
      const meta = sizedById.get(u.id) as GraphNode & { _width?: number; _cols?: number };
      const w = meta._width ?? UNIT_W;
      const boxLeft = dagreCenter.x - w / 2;
      const unitX = boxLeft + UNIT_W / 2;
      out.set(u.id, { x: unitX, y: dagreCenter.y });
    }

    // Place spokes in typed grids inside each expanded unit's box.
    // Position every spoke (not just filtered ones) so filter toggles
    // don't re-trigger dagre; React Flow hides filtered-out nodes via
    // their `hidden` prop.
    for (const unit of unitNodes) {
      if (!expandedSet.has(unit.id)) continue;
      const dagreCenter = dagrePositions.get(unit.id);
      if (!dagreCenter) continue;
      const meta = sizedById.get(unit.id) as GraphNode & { _width?: number; _cols?: number };
      const w = meta._width ?? UNIT_W;
      const boxLeft = dagreCenter.x - w / 2;

      const spokes = spokesByUnit.get(unit.id) ?? [];
      const groups: Record<string, GraphNode[]> = {};
      for (const s of spokes) (groups[s.concept_type] ??= []).push(s);
      const orderedTypes = [
        ...TYPE_COL_ORDER.filter((t) => groups[t]?.length),
        ...Object.keys(groups).filter((t) => !TYPE_COL_ORDER.includes(t)),
      ];

      let xCursor = boxLeft + UNIT_W + UNIT_MARGIN;
      for (const t of orderedTypes) {
        const list = groups[t];
        const subCols = Math.max(1, Math.ceil(list.length / MAX_ROWS));
        for (let i = 0; i < list.length; i++) {
          const subCol = Math.floor(i / MAX_ROWS);
          const row = i % MAX_ROWS;
          const colHeight = Math.min(MAX_ROWS, list.length - subCol * MAX_ROWS);
          const x = xCursor + subCol * COL_W + COL_W / 2;
          const y = dagreCenter.y + (row - (colHeight - 1) / 2) * ROW_H;
          out.set(list[i].id, { x, y });
        }
        xCursor += subCols * COL_W;
      }
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [collapseMode, data.nodes, unitLayout, spokesByUnit]);

  const nodes: Node[] = useMemo(
    () =>
      data.nodes.map((n) => {
        const pos = positions.get(n.id) ?? { x: n.x, y: n.y };
        // Two dim modes — filter-dim wins (user explicitly excluded the
        // node) and is aggressive (~0.10). Focus-dim (not related to a
        // selection) is softer (~0.35) so the rest of the map stays
        // readable instead of going pitch black.
        const filterDimmed = !filteredIds.has(n.id);
        const focusDimmed = !filterDimmed && relatedToSelected !== null && !relatedToSelected.has(n.id);
        return {
          id: n.id,
          type: 'conceptNode',
          position: pos,
          // Nodes sit above ordinary edges. Only edges from the focused
          // node get elevated above this (we set their zIndex to 1000).
          zIndex: 10,
          hidden: collapseMode && n.concept_type !== 'unit' && !filteredIds.has(n.id),
          data: {
            ...n,
            highlighted: n.id === selected,
            filterDimmed,
            focusDimmed,
            colorMode: colorBy,
            childCount: n.concept_type === 'unit' ? (spokeCountByUnit.get(n.id) ?? 0) : undefined,
            expanded: expandedUnits.has(n.id) || searchAutoExpanded.has(n.id),
            onToggleExpand: toggleExpand,
          },
        };
      }),
    [data.nodes, positions, selected, filteredIds, colorBy, collapseMode, spokeCountByUnit, expandedUnits, searchAutoExpanded, toggleExpand, relatedToSelected],
  );

  const edges: Edge[] = useMemo(
    () =>
      data.edges.map((e) => {
        const visible = filteredIds.has(e.source) && filteredIds.has(e.target);
        const touchesSel = selected != null && (e.source === selected || e.target === selected);
        // Pick the "other end" node so we can color by its type.
        const otherId = e.source === selected ? e.target : e.source;
        const otherType = touchesSel
          ? nodeById.get(otherId)?.concept_type
          : null;
        const hiColor: string | null = touchesSel
          ? (otherType ? (TYPE_EDGE_COLOR[otherType] ?? '#a1a1aa') : '#a1a1aa')
          : null;
        return {
          id: e.id,
          source: e.source,
          target: e.target,
          hidden: collapseMode && (!filteredIds.has(e.source) || !filteredIds.has(e.target)),
          animated: touchesSel,
          // All edges sit *below* the nodes (nodes have zIndex 10).
          // Unrelated nodes are dimmed enough that the focused edge
          // still reads through them; related nodes light up.
          zIndex: 0,
          style: {
            stroke: hiColor ?? (visible ? '#3f3f46' : '#1f1f23'),
            strokeWidth: touchesSel ? 2.5 : 1,
            ...(touchesSel ? { strokeDasharray: '8 4' } : {}),
            // When a node is selected, edges that don't touch it used to
            // drop to 0.05 — that made the whole map go nearly black.
            // 0.22 keeps the secondary graph structure readable so users
            // can still trace context around the focused subtree.
            opacity: touchesSel ? 1 : (selected ? 0.22 : (visible ? 0.55 : 0.2)),
          },
          markerEnd: { type: MarkerType.ArrowClosed, color: hiColor ?? '#3f3f46' },
        };
      }),
    [data.edges, filteredIds, selected, collapseMode, nodeById],
  );

  // Keep latest positions accessible from callbacks without invalidating
  // their identity each layout pass.
  const positionsRef = useRef(positions);
  useEffect(() => { positionsRef.current = positions; }, [positions]);

  // Center-and-zoom helper: smooth pan to a node using the *current* dagre
  // position (not the raw n.x/n.y from the data file, which is wrong in
  // collapse mode).
  const flyTo = useCallback((nodeId: string) => {
    const pos = positionsRef.current.get(nodeId);
    if (pos) {
      rf.setCenter(pos.x, pos.y, { zoom: 1.25, duration: 500 });
      return;
    }
    const n = data.nodes.find((x) => x.id === nodeId);
    if (n) rf.setCenter(n.x, n.y, { zoom: 1.25, duration: 500 });
  }, [rf, data.nodes]);

  const goto = useCallback((nodeId: string) => {
    const target = nodeById.get(nodeId);
    // dangling 참조(그래프에 없는 prereq/enables slug)면 selectedNode 가 null 이 되어
    // 패널이 조용히 닫히는 죽은 버튼이 된다 → 선택 자체를 막아 현재 패널 유지.
    if (!target) return;
    setSelected(nodeId);
    // If clicking a spoke from a list and its home unit is collapsed,
    // expand it first so the spoke becomes visible — otherwise we'd fly
    // the camera to an empty (hidden) area.
    if (target && target.concept_type !== 'unit') {
      const home = homeUnitOf.get(nodeId);
      if (home && !expandedUnits.has(home) && !searchAutoExpanded.has(home)) {
        setExpandedUnits((p) => new Set([...p, home]));
      }
    }
    // Defer the camera move so dagre has a frame to re-layout when we
    // just expanded a unit. positionsRef will then hold the new coords.
    window.setTimeout(() => flyTo(nodeId), 80);
  }, [flyTo, nodeById, homeUnitOf, expandedUnits, searchAutoExpanded]);

  const onNodeClick: NodeMouseHandler = useCallback((_, node) => {
    // Select only — don't fly/zoom. Auto-zoom was disorienting; the user
    // could easily lose context (panned to an off-screen blank area).
    setSelected(node.id);
  }, []);

  const onNodeDoubleClick: NodeMouseHandler = useCallback((_, node) => {
    const d = node.data as GraphNode;
    if (d.concept_type !== 'unit') return;
    toggleExpand(node.id);
  }, [toggleExpand]);

  const expandAll = useCallback(() => setExpandedUnits(new Set(allUnitIds)), [allUnitIds]);
  const collapseAll = useCallback(() => setExpandedUnits(new Set()), []);

  useEffect(() => {
    const t = setTimeout(() => {
      if (effectiveHighlight) {
        // Only the explicit ?highlight=... param flies the camera.
        goto(effectiveHighlight);
      } else {
        rf.fitView({ padding: 0.2, duration: 400 });
      }
    }, 50);
    return () => clearTimeout(t);
    // goto intentionally excluded — we don't want this to re-fire on
    // every render of goto's closure deps.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rf, effectiveHighlight]);

  // (No automatic camera fit on expand/collapse — the user explicitly
  // doesn't want the view to fly around. Press `f` to manually fit.)

  // 검색어 매치 노드를 selected로만 잡아둠 (자동 zoom/pan 안 함).
  // 다수 매치는 fitView로 한 화면에 모아주는 것까지만 (그건 길 잃지 않음).
  useEffect(() => {
    if (!debouncedTerm) return;
    const term = searchNorm(debouncedTerm);
    const matches = data.nodes.filter((n) => searchNorm(n.label).includes(term));
    if (matches.length === 1) {
      setSelected(matches[0].id);
    } else if (matches.length > 1 && matches.length <= 12) {
      rf.fitView({ nodes: matches.map((m) => ({ id: m.id })), padding: 0.3, duration: 400 });
    }
  }, [debouncedTerm, data.nodes, rf]);

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

  const selectedNode = selected ? nodeById.get(selected) ?? null : null;

  // Display label: replace underscores with spaces (slugs use _ as separator).
  const prettyLabel = (ref: string) => {
    const n = nodeById.get(ref);
    return (n?.label ?? ref).replace(/_/g, ' ');
  };

  // Group an id list (prereqs or enables) by concept_type, preserving the
  // canonical type order (unit → definition → theorem → lemma → example → 기타).
  const groupRefsByType = (refs: string[]) => {
    const groups = new Map<string, string[]>();
    for (const ref of refs) {
      const t = nodeById.get(ref)?.concept_type ?? 'other';
      const arr = groups.get(t) ?? [];
      arr.push(ref);
      groups.set(t, arr);
    }
    const ordered: Array<[string, string[]]> = [];
    for (const t of ['unit', ...TYPE_COL_ORDER]) {
      const arr = groups.get(t);
      if (arr?.length) ordered.push([t, arr]);
    }
    for (const [t, arr] of groups) {
      if (t !== 'unit' && !TYPE_COL_ORDER.includes(t)) ordered.push([t, arr]);
    }
    return ordered;
  };

  // Memoized pill counts — avoid O(N) re-filter on every render
  const masteryCounts = useMemo(() => {
    const c: Record<string, number> = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
    for (const n of data.nodes) c[n.mastery] = (c[n.mastery] ?? 0) + 1;
    return c;
  }, [data.nodes]);
  const domainCounts = useMemo(() => {
    const c: Record<string, number> = {};
    for (const n of data.nodes) if (n.domain) c[n.domain] = (c[n.domain] ?? 0) + 1;
    return c;
  }, [data.nodes]);
  const gradeCounts = useMemo(() => {
    const c: Record<string, number> = {};
    for (const n of data.nodes) if (n.grade) c[n.grade] = (c[n.grade] ?? 0) + 1;
    return c;
  }, [data.nodes]);

  // Multi-select toggle:
  //   default = all selected (전체)
  //   click pill X → toggle X in/out of the active set
  //   if user deselects last one → snap back to all (avoid showing nothing)
  //   "전체로" 버튼 = explicit reset to all
  const ALL_MASTERY = ['unknown', 'learning', 'proficient', 'mastered'] as const;
  const toggleInSet = <T extends string>(prev: Set<string>, item: T, _all: readonly T[]): Set<string> => {
    const next = new Set(prev);
    if (next.has(item)) next.delete(item);
    else next.add(item);
    return next; // opt-in: 빈 Set = 전체이므로 "마지막 끄면 전체 복귀" 로직 불필요
  };
  const toggleMastery = (m: string) => setMasteryFilter((p) => toggleInSet(p, m, ALL_MASTERY));
  const resetMastery = () => setMasteryFilter(new Set());

  const toggleGrade = (g: string) => setGradeFilter((p) => toggleInSet(p, g, gradesInData));
  const resetGrade = () => setGradeFilter(new Set());

  const toggleDomain = (d: string) => setDomainFilter((p) => toggleInSet(p, d, domainsInData));
  const resetDomain = () => setDomainFilter(new Set());

  const masteryAllActive = masteryFilter.size === 0;
  const gradeAllActive = gradeFilter.size === 0;
  const domainAllActive = domainFilter.size === 0;

  return (
    <div className={`relative w-full ${variant === 'mini' ? 'h-[320px]' : 'h-full'}`}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={onNodeClick}
        onNodeDoubleClick={onNodeDoubleClick}
        onPaneClick={() => setSelected(null)}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={variant === 'full'}
        nodesConnectable={false}
        elementsSelectable
        fitView
        fitViewOptions={FIT_VIEW_OPTIONS}
        defaultEdgeOptions={DEFAULT_EDGE_OPTIONS}
        onlyRenderVisibleElements
        minZoom={0.15}
        maxZoom={2.5}
        zoomOnScroll={true}
        panOnScroll={false}
        panOnDrag={true}
        selectionOnDrag={false}
        zoomActivationKeyCode={null}
      >
        {variant === 'full' && (
          <Controls position="bottom-right" showInteractive={false} className="dag-controls" />
        )}
      </ReactFlow>

      {variant === 'full' && (
        <>
          {/* Left filter panel */}
          <div className="absolute top-4 bottom-24 left-4 z-10 w-72 card p-3 space-y-3 overflow-auto">
            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-1">검색 <span className="text-zinc-600 normal-case tracking-normal">(/ 키)</span></label>
              <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="개념 이름…"
                className="dag-search-input w-full px-2 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm focus:outline-none focus:border-indigo-400"
              />
              <p className="mt-1 text-[10px] text-zinc-600">
                f = fit · esc = 닫기 · 클릭 = 이동 · <strong>더블클릭(unit) = 펼치기/접기</strong>
              </p>
            </div>

            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-1">접기/펼치기</label>
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setCollapseMode((v) => !v)}
                  className={`flex-1 text-xs px-2 py-1 rounded border transition ${
                    collapseMode
                      ? 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300'
                      : 'border-zinc-700 text-zinc-400 hover:text-zinc-100'
                  }`}
                  title="끄면 모든 spoke 강제 표시"
                >
                  접기 모드 {collapseMode ? 'ON' : 'OFF'}
                </button>
                <button onClick={expandAll}
                        className="text-[10px] px-2 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                  모두 펼침
                </button>
                <button onClick={collapseAll}
                        className="text-[10px] px-2 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                  모두 접기
                </button>
              </div>
              <p className="mt-1 text-[10px] text-zinc-600">
                펼쳐진 unit: <span className="text-zinc-300">{expandedUnits.size}/{allUnitIds.length}</span>
                {searchAutoExpanded.size > 0 && (
                  <span className="text-emerald-400"> · 검색 매치 unit {searchAutoExpanded.size}개 자동 펼침</span>
                )}
              </p>
            </div>
            <div>
              <label className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 block mb-1">노드 색상 기준</label>
              <div className="inline-flex rounded-md border border-zinc-800 overflow-hidden text-xs">
                {(['domain', 'mastery', 'grade'] as const).map((c) => (
                  <button
                    key={c}
                    onClick={() => setColorBy(c)}
                    className={`px-2.5 py-1 transition ${
                      colorBy === c ? 'bg-indigo-500/20 text-indigo-300' : 'text-zinc-500 hover:text-zinc-200'
                    }`}
                  >
                    {c === 'domain' ? '도메인' : c === 'mastery' ? '마스터리' : '학년'}
                  </button>
                ))}
              </div>
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
                      title="클릭하여 토글"
                    >
                      <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                      <span>{m}</span>
                      <span className="text-zinc-500 font-normal">
                        {masteryCounts[m] ?? 0}
                      </span>
                    </button>
                  );
                })}
                {/* 학습 노트(syntheses) 토글 — graph.astro에서 주입한 note_count 사용. */}
                <button
                  onClick={() => setNotesOnly((v) => !v)}
                  className="px-2 py-1 rounded-md text-xs font-medium transition border flex items-center gap-1.5"
                  style={{
                    background: notesOnly ? 'rgba(245, 158, 11, 0.30)' : 'transparent',
                    borderColor: notesOnly ? '#f59e0b' : '#27272a',
                    color: notesOnly ? '#fbbf24' : '#52525b',
                  }}
                  title={notesOnly ? '필터 해제' : '저장된 노트가 있는 컨셉만 표시'}
                >
                  <span aria-hidden>🗒</span>
                  <span>노트 있음</span>
                </button>
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
                        title="클릭하여 토글"
                      >
                        <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                        <span>{d}</span>
                        <span className="text-zinc-500 font-normal">
                          {domainCounts[d] ?? 0}
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
                        title="클릭하여 토글"
                      >
                        <span className="inline-block size-1.5 rounded-full" style={{ background: color }} />
                        <span>{g}</span>
                        <span className="text-zinc-500 font-normal">
                          {gradeCounts[g] ?? 0}
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
                <h3 className="text-sm font-semibold">{selectedNode.label.replace(/_/g, ' ')}</h3>
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
                  <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1.5">선수 (prerequisites)</div>
                  <div className="space-y-2">
                    {groupRefsByType(selectedNode.prerequisites).map(([t, refs]) => (
                      <div key={t}>
                        <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 mb-0.5">
                          <span style={{ color: TYPE_EDGE_COLOR[t] ?? '#71717a' }}>{TYPE_ICON[t] ?? '·'}</span>
                          <span>{TYPE_LABEL_KO[t] ?? t}</span>
                          <span className="text-zinc-600 font-mono">{refs.length}</span>
                        </div>
                        <ul className="text-sm space-y-0.5 pl-4">
                          {refs.map((p) => (
                            <li key={p}>
                              {nodeById.has(p) ? (
                                <button
                                  onClick={() => goto(p)}
                                  className="text-indigo-400 hover:underline text-left"
                                >{prettyLabel(p)}</button>
                              ) : (
                                // dangling 참조 — 그래프에 노드가 없으므로 클릭 비활성.
                                <span
                                  className="text-zinc-500 text-left cursor-default"
                                  title="이 개념은 그래프에 없습니다"
                                >{prettyLabel(p)}</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {selectedNode.enables.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1.5">enables</div>
                  <div className="space-y-2">
                    {groupRefsByType(selectedNode.enables).map(([t, refs]) => (
                      <div key={t}>
                        <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 mb-0.5">
                          <span style={{ color: TYPE_EDGE_COLOR[t] ?? '#71717a' }}>{TYPE_ICON[t] ?? '·'}</span>
                          <span>{TYPE_LABEL_KO[t] ?? t}</span>
                          <span className="text-zinc-600 font-mono">{refs.length}</span>
                        </div>
                        <ul className="text-sm space-y-0.5 pl-4">
                          {refs.map((p) => (
                            <li key={p}>
                              {nodeById.has(p) ? (
                                <button
                                  onClick={() => goto(p)}
                                  className="text-indigo-400 hover:underline text-left"
                                >{prettyLabel(p)}</button>
                              ) : (
                                // dangling 참조 — 그래프에 노드가 없으므로 클릭 비활성.
                                <span
                                  className="text-zinc-500 text-left cursor-default"
                                  title="이 개념은 그래프에 없습니다"
                                >{prettyLabel(p)}</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              <a
                href={`/concepts/${selectedNode.slug}`}
                className="block text-center mt-2 px-3 py-2 rounded-md bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-sm font-medium transition"
              >
                상세 페이지 →
              </a>
            </div>
          )}

          {/* Legend bottom-left */}
          <div className="absolute bottom-4 left-4 z-10 card px-3 py-2 text-xs">
            <div className="text-[10px] uppercase tracking-[0.15em] text-zinc-500 mb-1.5">노드 모양</div>
            <div className="flex gap-4 text-zinc-300">
              {(['definition', 'theorem', 'lemma', 'example'] as const).map((t) => (
                <span key={t} className="flex items-center gap-1.5">
                  <span className="text-base" style={{ color: TYPE_EDGE_COLOR[t] }}>{TYPE_ICON[t]}</span>
                  <span className="flex items-baseline gap-1">
                    <span>{TYPE_LABEL_KO[t]}</span>
                    <span className="text-[9px] text-zinc-600 lowercase">{t}</span>
                  </span>
                  <span
                    className="inline-block rounded-sm"
                    style={{ background: TYPE_EDGE_COLOR[t], width: 14, height: 2 }}
                    title="연결선 색"
                  />
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
