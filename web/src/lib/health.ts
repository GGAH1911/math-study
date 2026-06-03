// Helpers to load wiki health/log info directly from the docs/ filesystem.
// Uses process.cwd() since `npm run dev|build` is always invoked from web/.
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import matter from 'gray-matter';

const WEB_ROOT = process.cwd();
const DOCS = resolve(WEB_ROOT, '..', 'docs');

export type Health = {
  pages: number;
  orphans: number;
  conflicts: number;
  dueToday: number;
  mastery: { unknown: number; learning: number; proficient: number; mastered: number };
  dagIntegrity: string;
  suggestedAction: string;
  lastUpdated: string;
};

export function readHealth(): Health {
  // 정량 필드(개념수·mastery·due·dag)는 *라이브* 소스인 concept-graph.json 에서 실측한다.
  // (그래프 빌드 스크립트 + mastery-promote API 가 노드를 갱신하므로 항상 최신.)
  // docs/index.md frontmatter 의 mastery_*/due_today/pages 는 2026-05-16 박제 스냅샷
  // (개념 490 시절)이라 더 이상 읽지 않는다 — 텍스트(suggested_action/last_updated)만 가져온다.
  const graph = readConceptGraph();
  const mastery = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
  for (const n of graph.nodes) {
    const k = n.mastery as keyof typeof mastery;
    if (k in mastery) mastery[k]++;
  }
  const today = new Date().toISOString().slice(0, 10);
  const dueToday = graph.nodes.reduce(
    (acc, n) => acc + (n.next_review && n.next_review <= today ? 1 : 0),
    0,
  );

  const p = resolve(DOCS, 'index.md');
  const fm = existsSync(p)
    ? (matter(readFileSync(p, 'utf-8')).data as Record<string, unknown>)
    : {};

  return {
    pages: graph.nodes.length,
    orphans: Number(fm.orphans ?? 0),
    conflicts: Number(fm.conflicts ?? 0),
    dueToday,
    mastery,
    dagIntegrity: (graph.stats?.cycles ?? 0) === 0 ? 'ok' : `${graph.stats.cycles} cycles`,
    suggestedAction: String(fm.suggested_action ?? ''),
    lastUpdated: String(fm.last_updated ?? ''),
  };
}

export type LogEntry = { date: string; operation: string; subject: string; raw: string };

export function readLog(limit?: number): LogEntry[] {
  const p = resolve(DOCS, 'log.md');
  if (!existsSync(p)) return [];
  const text = readFileSync(p, 'utf-8');
  const entries: LogEntry[] = [];
  for (const m of text.matchAll(/^## \[(\d{4}-\d{2}-\d{2})\]\s*([^|]+?)\s*\|\s*(.*)$/gm)) {
    entries.push({ date: m[1], operation: m[2].trim(), subject: m[3].trim(), raw: m[0] });
  }
  entries.reverse();
  return limit ? entries.slice(0, limit) : entries;
}

export type ConceptGraph = {
  generatedAt: string;
  nodes: Array<{
    id: string; slug: string; label: string;
    concept_type: string; mastery: string;
    prerequisites: string[]; enables: string[];
    review_state: string | null; next_review: string | null;
    x: number; y: number;
  }>;
  edges: Array<{ id: string; source: string; target: string }>;
  stats: {
    nodes: number; edges: number; cycles: number;
    byMastery: Record<string, number>;
    byType: Record<string, number>;
  };
};

export function readConceptGraph(): ConceptGraph {
  const p = resolve(WEB_ROOT, 'src', 'data', 'concept-graph.json');
  if (!existsSync(p)) {
    return { generatedAt: '', nodes: [], edges: [], stats: { nodes: 0, edges: 0, cycles: 0, byMastery: {}, byType: {} } };
  }
  return JSON.parse(readFileSync(p, 'utf-8'));
}
