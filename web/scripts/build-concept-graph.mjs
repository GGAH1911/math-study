#!/usr/bin/env node
/**
 * Parse all concept frontmatter under ../docs/concepts and emit
 * src/data/concept-graph.json with nodes (mastery, type, dagre coords)
 * and edges (prerequisite arrows).
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename } from 'node:path';
import matter from 'gray-matter';
import dagre from 'dagre';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const DOCS_DIR = join(WEB_ROOT, '..', 'docs', 'concepts');
const OUT_DIR = join(WEB_ROOT, 'src', 'data');
const OUT_FILE = join(OUT_DIR, 'concept-graph.json');

function slugFromPath(p) {
  return basename(p, '.md');
}

function readConcepts() {
  if (!existsSync(DOCS_DIR)) return [];
  return readdirSync(DOCS_DIR)
    .filter((f) => f.endsWith('.md'))
    .map((f) => {
      const filePath = join(DOCS_DIR, f);
      const fm = matter(readFileSync(filePath, 'utf-8')).data;
      return {
        id: slugFromPath(f),
        slug: slugFromPath(f),
        label: slugFromPath(f).replace(/_/g, ' '),
        concept_type: fm.concept_type ?? 'definition',
        grade: fm.grade ?? null,
        unit: fm.unit ?? null,
        subunit: fm.subunit ?? null,
        mastery: fm.mastery ?? 'unknown',
        prerequisites: (fm.prerequisites ?? []).map(slugFromPath),
        enables: (fm.enables ?? []).map(slugFromPath),
        review_state: fm.review_state ?? null,
        next_review: fm.next_review ?? null,
      };
    });
}

function buildEdges(concepts) {
  const ids = new Set(concepts.map((c) => c.id));
  const edges = [];
  for (const c of concepts) {
    for (const pre of c.prerequisites) {
      if (ids.has(pre)) {
        edges.push({ id: `e-${pre}-${c.id}`, source: pre, target: c.id });
      }
    }
  }
  return edges;
}

function layout(concepts, edges) {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: 'TB', nodesep: 50, ranksep: 70, marginx: 30, marginy: 30 });
  g.setDefaultEdgeLabel(() => ({}));
  for (const c of concepts) {
    g.setNode(c.id, { width: 180, height: 70 });
  }
  for (const e of edges) {
    g.setEdge(e.source, e.target);
  }
  dagre.layout(g);
  const positioned = concepts.map((c) => {
    const n = g.node(c.id);
    return { ...c, x: n.x, y: n.y };
  });
  return positioned;
}

function detectCycles(concepts) {
  const adj = new Map(concepts.map((c) => [c.id, c.enables.filter((e) => concepts.find((cc) => cc.id === e))]));
  const indeg = new Map(concepts.map((c) => [c.id, 0]));
  for (const [_, outs] of adj) for (const t of outs) indeg.set(t, (indeg.get(t) ?? 0) + 1);
  const queue = [];
  for (const [id, d] of indeg) if (d === 0) queue.push(id);
  let visited = 0;
  while (queue.length) {
    const n = queue.shift();
    visited++;
    for (const t of adj.get(n) ?? []) {
      indeg.set(t, indeg.get(t) - 1);
      if (indeg.get(t) === 0) queue.push(t);
    }
  }
  return concepts.length - visited;
}

function main() {
  const concepts = readConcepts();
  const edges = buildEdges(concepts);
  const positioned = layout(concepts, edges);
  const cycles = detectCycles(concepts);

  const byMastery = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
  for (const c of concepts) byMastery[c.mastery] = (byMastery[c.mastery] ?? 0) + 1;
  const byType = { unit: 0, definition: 0, theorem: 0, lemma: 0, example: 0 };
  for (const c of concepts) byType[c.concept_type] = (byType[c.concept_type] ?? 0) + 1;
  const byGrade = {};
  for (const c of concepts) if (c.grade) byGrade[c.grade] = (byGrade[c.grade] ?? 0) + 1;

  const out = {
    generatedAt: new Date().toISOString(),
    nodes: positioned,
    edges,
    stats: {
      nodes: concepts.length,
      edges: edges.length,
      cycles,
      byMastery,
      byType,
      byGrade,
    },
  };

  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(out, null, 2), 'utf-8');
  console.log(`[concept-graph] ${concepts.length} nodes, ${edges.length} edges, ${cycles} cycles → ${OUT_FILE}`);
}

main();
