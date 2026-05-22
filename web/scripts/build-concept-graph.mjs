#!/usr/bin/env node
/**
 * Parse all concept frontmatter under ../docs/concepts and emit
 * src/data/concept-graph.json with nodes (mastery, type, dagre coords)
 * and edges (prerequisite arrows).
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';
import matter from 'gray-matter';
import dagre from 'dagre';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const DOCS_DIR = join(WEB_ROOT, '..', 'docs', 'concepts');
const OUT_DIR = join(WEB_ROOT, 'src', 'data');
const OUT_FILE = join(OUT_DIR, 'concept-graph.json');

// sub-dir 호환: 'algebra/근의_공식' (DOCS_DIR 기준 relative path, .md 제거)
function slugFromFile(absPath) {
  return relative(DOCS_DIR, absPath).replace(/\.md$/, '').split(/[\\/]/).join('/');
}
// frontmatter cross-ref ('docs/concepts/algebra/근의_공식.md' 또는 슬러그 only) → slug
function slugFromRef(p) {
  return p.replace(/^docs\/concepts\//, '').replace(/\.md$/, '');
}

function walkMd(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...walkMd(p));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function readConcepts() {
  return walkMd(DOCS_DIR).map((filePath) => {
    const fm = matter(readFileSync(filePath, 'utf-8')).data;
    const id = slugFromFile(filePath);
    return {
      id,
      slug: id,
      label: (id.split('/').pop() ?? id).replace(/_/g, ' '),
      concept_type: fm.concept_type ?? 'definition',
      grade: fm.grade ?? null,
      domain: fm.domain ?? null,
      unit: fm.unit ?? null,
      subunit: fm.subunit ?? null,
      mastery: fm.mastery ?? 'unknown',
      prerequisites: (fm.prerequisites ?? []).map(slugFromRef),
      enables: (fm.enables ?? []).map(slugFromRef),
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
  g.setGraph({ rankdir: 'LR', nodesep: 30, ranksep: 120, marginx: 30, marginy: 30 });
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
  const byDomain = {};
  for (const c of concepts) if (c.domain) byDomain[c.domain] = (byDomain[c.domain] ?? 0) + 1;

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
      byDomain,
    },
  };

  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(out, null, 2), 'utf-8');
  console.log(`[concept-graph] ${concepts.length} nodes, ${edges.length} edges, ${cycles} cycles → ${OUT_FILE}`);
}

main();
