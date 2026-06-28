// ConceptDAG dagre 레이아웃(순수) — 컴포넌트에서 분리.
import dagre from 'dagre';
import type { GraphNode, GraphEdge } from './dag-types';

export function dagreLayout(
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
