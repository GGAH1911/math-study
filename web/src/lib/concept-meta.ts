// Shared metadata for concepts — labels, colors, ordering.
// Used by /concepts (index + detail) and the graph component to keep
// the visual language consistent.

export const MASTERY_ORDER = ['unknown', 'learning', 'proficient', 'mastered'] as const;
export type Mastery = (typeof MASTERY_ORDER)[number];

export const MASTERY_COLOR: Record<string, string> = {
  unknown: '#f43f5e',     // rose-500
  learning: '#f59e0b',    // amber-500
  proficient: '#10b981',  // emerald-500
  mastered: '#0ea5e9',    // sky-500
};

export const MASTERY_LABEL_KO: Record<string, string> = {
  unknown: '미습득',
  learning: '학습중',
  proficient: '능숙',
  mastered: '숙달',
};

export const TYPE_ORDER = ['unit', 'definition', 'theorem', 'lemma', 'example'] as const;
export type ConceptType = (typeof TYPE_ORDER)[number];

export const TYPE_LABEL_KO: Record<string, string> = {
  unit: '단원',
  definition: '정의',
  theorem: '정리',
  lemma: '보조정리',
  example: '예제',
};

export const TYPE_ICON: Record<string, string> = {
  unit: '◆',
  definition: '○',
  theorem: '◇',
  lemma: '△',
  example: '□',
};

export const GRADE_ORDER = ['중1', '중2', '중3', '고1', '수학1', '수학2', '미적분', '기하', '확률과통계'] as const;
export type Grade = (typeof GRADE_ORDER)[number];

export const GRADE_COLOR: Record<string, string> = {
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

export const DOMAIN_ORDER = ['수와식', '방정식', '함수', '도형', '확률통계', '논리'] as const;
export type Domain = (typeof DOMAIN_ORDER)[number];

export const DOMAIN_COLOR: Record<string, string> = {
  '수와식':   '#f59e0b',  // amber
  '방정식':   '#ef4444',  // red
  '함수':     '#3b82f6',  // blue (가장 큰 도메인)
  '도형':     '#22d3ee',  // cyan
  '확률통계': '#ec4899',  // pink
  '논리':     '#a78bfa',  // violet
};
