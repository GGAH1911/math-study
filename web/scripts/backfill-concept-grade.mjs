#!/usr/bin/env node
/**
 * Backfill `grade:` frontmatter for concepts that don't have one yet.
 * Mirror of backfill-concept-domain.mjs:
 *   1. Inherit from home_unit.grade (115 of 118 uncategorized files).
 *   2. Fall back to a hand-curated map for the 3 orphans whose stale
 *      flat-path prereqs prevented home-unit resolution.
 *
 * Default is dry-run. Pass `--write` to edit .md files.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const DOCS_DIR = join(REPO_ROOT, 'docs', 'concepts');
const GRAPH_FILE = join(WEB_ROOT, 'src', 'data', 'concept-graph.json');

// Orphans (home_unit=null because of stale flat prereqs). Verified by
// reading their `prerequisites` field and pointing the chain at the right
// subdir.
const ORPHAN_GRADE = {
  'uncategorized/0_꼴_극한': '미적분',     // prereq: 여러가지함수의_극한 (functions/calculus)
  'uncategorized/0_부정형': '수학2',       // prereq: 함수의_극한과_연속 (functions/math-2)
  'uncategorized/sin_cos_관계식': '수학1',  // prereq: 삼각함수 (functions/math-1)
};

// Insert `grade:` right after `domain:` (if present) or after `concept_type:`.
// Replaces existing value if already set.
function setGradeInFrontmatter(text, grade) {
  if (/^grade:\s*.*$/m.test(text)) {
    return text.replace(/^grade:\s*.*$/m, `grade: ${grade}`);
  }
  if (/^domain:.*$/m.test(text)) {
    return text.replace(/^(domain:.*)$/m, `$1\ngrade: ${grade}`);
  }
  if (/^concept_type:.*$/m.test(text)) {
    return text.replace(/^(concept_type:.*)$/m, `$1\ngrade: ${grade}`);
  }
  return text.replace(/^---\n/, `---\ngrade: ${grade}\n`);
}

function main() {
  const write = process.argv.includes('--write');
  const graph = JSON.parse(readFileSync(GRAPH_FILE, 'utf-8'));
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));

  let viaHome = 0, viaOrphan = 0, alreadyHasGrade = 0, unresolved = 0, missingFile = 0;
  const planned = [];
  const unresolvedList = [];

  for (const node of graph.nodes) {
    if (node.grade) { alreadyHasGrade++; continue; }

    let grade = null;
    let via = '';
    if (node.home_unit) {
      const home = byId.get(node.home_unit);
      if (home?.grade) { grade = home.grade; via = 'home'; }
    }
    if (!grade && ORPHAN_GRADE[node.id]) {
      grade = ORPHAN_GRADE[node.id];
      via = 'orphan';
    }
    if (!grade) { unresolved++; unresolvedList.push(node.id); continue; }

    const mdPath = join(DOCS_DIR, `${node.id}.md`);
    if (!existsSync(mdPath)) { missingFile++; continue; }
    planned.push({ id: node.id, grade, via, mdPath });
    if (via === 'home') viaHome++; else viaOrphan++;
  }

  console.log(`══ backfill-concept-grade ══`);
  console.log(`  already has grade:   ${alreadyHasGrade}`);
  console.log(`  via home_unit:       ${viaHome}`);
  console.log(`  via orphan map:      ${viaOrphan}`);
  console.log(`  unresolved:          ${unresolved}`);
  console.log(`  missing .md file:    ${missingFile}`);
  if (unresolvedList.length) {
    console.log(`\nUnresolved:`);
    for (const id of unresolvedList) console.log(`    ${id}`);
  }

  console.log(`\nSample plan (first 10):`);
  for (const p of planned.slice(0, 10)) {
    console.log(`  ${p.grade.padEnd(8)} (${p.via.padEnd(6)}) ← ${p.id}`);
  }
  if (planned.length > 10) console.log(`  ... and ${planned.length - 10} more.`);

  if (!write) {
    console.log(`\n(dry-run; pass --write to apply ${planned.length} changes)`);
    return;
  }

  console.log(`\nWriting ${planned.length} files...`);
  for (const p of planned) {
    const text = readFileSync(p.mdPath, 'utf-8');
    const updated = setGradeInFrontmatter(text, p.grade);
    if (updated !== text) writeFileSync(p.mdPath, updated, 'utf-8');
  }
  console.log(`Done.`);
}

main();
