// ConceptDAG 그래프 데이터 타입 — 컴포넌트에서 분리.
export type GraphNode = {
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

export type GraphEdge = { id: string; source: string; target: string };

export type GraphData = {
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
export type ColorMode = 'domain' | 'mastery' | 'grade';
