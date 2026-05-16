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
  const p = resolve(DOCS, 'index.md');
  const fm = existsSync(p)
    ? (matter(readFileSync(p, 'utf-8')).data as Record<string, unknown>)
    : {};
  const num = (k: string) => Number(fm[k] ?? 0);
  const str = (k: string) => String(fm[k] ?? '');
  return {
    pages: num('pages'),
    orphans: num('orphans'),
    conflicts: num('conflicts'),
    dueToday: num('due_today'),
    mastery: {
      unknown: num('mastery_unknown'),
      learning: num('mastery_learning'),
      proficient: num('mastery_proficient'),
      mastered: num('mastery_mastered'),
    },
    dagIntegrity: str('dag_integrity') || 'ok',
    suggestedAction: str('suggested_action'),
    lastUpdated: str('last_updated'),
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
