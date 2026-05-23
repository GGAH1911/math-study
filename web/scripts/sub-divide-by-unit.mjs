#!/usr/bin/env node
/**
 * Sub-divide every concept grade dir by unit. Each spoke moves to live
 * UNDER its home_unit:
 *
 *   docs/concepts/<dom>/<grade>/<spoke>.md
 *     → docs/concepts/<dom>/<grade>/<unit-stem>/<spoke>.md
 *
 * Unit files themselves stay at their current path; the new sibling
 * directory just holds their spokes. After this the audit's flat-warn
 * for grade dirs disappears (each grade dir now contains only unit
 * files + unit subfolders), and the filesystem mirrors the prereq
 * graph's unit grouping.
 *
 * Orphan spokes (no home_unit — 3 in the current data) stay put.
 *
 * Default is dry-run. Pass `--write` to git mv + rewrite refs.
 *
 * Cross-references in problem files, tool files, and other concept
 * files are rewritten in the same pass (full-path swap of
 * `docs/concepts/<old-id>` to `docs/concepts/<new-id>`, with and
 * without `.md` suffix).
 */
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, basename } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const DOCS_DIR = join(REPO_ROOT, 'docs');
const CONCEPTS_DIR = join(DOCS_DIR, 'concepts');
const GRAPH_FILE = join(WEB_ROOT, 'src', 'data', 'concept-graph.json');

function walkMd(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) walkMd(p, out);
    else if (entry.endsWith('.md')) out.push(p);
  }
  return out;
}

function quote(s) {
  return "'" + s.replace(/'/g, `'\\''`) + "'";
}

function main() {
  const write = process.argv.includes('--write');
  const graph = JSON.parse(readFileSync(GRAPH_FILE, 'utf-8'));

  // Build the move plan.
  const moves = [];
  const collisions = [];
  let alreadyNested = 0;
  let orphan = 0;
  let unitFile = 0;

  for (const node of graph.nodes) {
    if (node.concept_type === 'unit') { unitFile++; continue; }
    if (!node.home_unit) { orphan++; continue; }

    // Current id = path relative to docs/concepts, without .md.
    // We want target id = <home_unit>/<spoke-basename>.
    const spokeName = basename(node.id);
    const homeUnitId = node.home_unit;            // e.g. functions/calculus/도함수의_활용_심화
    const newId = `${homeUnitId}/${spokeName}`;

    if (node.id === newId) { alreadyNested++; continue; }
    // Skip if the spoke's current path is already inside its home_unit.
    if (dirname(node.id) === homeUnitId) { alreadyNested++; continue; }

    const srcAbs = join(CONCEPTS_DIR, `${node.id}.md`);
    const dstAbs = join(CONCEPTS_DIR, `${newId}.md`);
    if (!existsSync(srcAbs)) {
      console.log(`  ! missing source: ${node.id}`);
      continue;
    }
    if (existsSync(dstAbs)) { collisions.push({ id: node.id, dst: newId }); continue; }
    moves.push({
      oldId: node.id, newId,
      srcAbs, dstAbs,
      srcRel: relative(REPO_ROOT, srcAbs),
      dstRel: relative(REPO_ROOT, dstAbs),
    });
  }

  console.log(`══ sub-divide-by-unit ══`);
  console.log(`  unit files (stay put):    ${unitFile}`);
  console.log(`  orphan spokes (skip):     ${orphan}`);
  console.log(`  already nested (skip):    ${alreadyNested}`);
  console.log(`  planned moves:            ${moves.length}`);
  console.log(`  collisions:               ${collisions.length}`);
  if (collisions.length) {
    console.log(`\nCollisions (target path already taken):`);
    for (const c of collisions.slice(0, 10)) {
      console.log(`    ${c.id}  →  ${c.dst}`);
    }
    if (collisions.length > 10) console.log(`    ... +${collisions.length - 10} more`);
  }

  // Distribution of unit folder sizes after the move.
  const sizes = {};
  for (const m of moves) {
    const u = dirname(m.newId);
    sizes[u] = (sizes[u] ?? 0) + 1;
  }
  const sizeArr = Object.entries(sizes).sort((a,b)=>b[1]-a[1]);
  console.log(`\nResulting unit folder sizes (top 10):`);
  for (const [u, n] of sizeArr.slice(0, 10)) console.log(`    ${n.toString().padStart(4)}  ${u}`);
  console.log(`  units with > 100 spokes: ${sizeArr.filter(([,n]) => n > 100).length}`);
  console.log(`  units with 50-100:       ${sizeArr.filter(([,n]) => n >= 50 && n <= 100).length}`);
  console.log(`  units with < 50:         ${sizeArr.filter(([,n]) => n < 50).length}`);

  // Reference replacement table: only the full `.md` form. Substring
  // replacement on bare ids (no .md) is unsafe — an oldId can be a
  // prefix of another path (e.g. moving `algebra/foo` would also rewrite
  // references to `algebra/foo_extension.md`). All canonical references
  // in this repo use the .md suffix, so the .md-anchored swap is enough.
  const replacements = moves.map((m) => [
    `docs/concepts/${m.oldId}.md`,
    `docs/concepts/${m.newId}.md`,
  ]);

  // Scan all .md under docs/ for swap candidates.
  const allMd = walkMd(DOCS_DIR);
  let totalHits = 0;
  const affected = [];
  for (const p of allMd) {
    const text = readFileSync(p, 'utf-8');
    let hits = 0;
    for (const [from] of replacements) {
      if (text.includes(from)) hits += (text.split(from).length - 1);
    }
    if (hits > 0) { affected.push(p); totalHits += hits; }
  }
  console.log(`\nFiles needing reference updates: ${affected.length}`);
  console.log(`Total reference swaps: ${totalHits}`);

  if (!write) {
    console.log(`\n(dry-run; pass --write to perform ${moves.length} moves + ${totalHits} ref swaps)`);
    if (collisions.length) console.log(`NOTE: ${collisions.length} collision(s) must be resolved first.`);
    return;
  }
  if (collisions.length) {
    console.error(`\nAborting: ${collisions.length} collision(s). Resolve and re-run.`);
    process.exit(1);
  }

  // Execute. To avoid intermediate-collision issues (rename A→A/sub then
  // rename A/sub → A/sub/x), do all `mkdir -p` first, then all `git mv`,
  // then all in-place edits.
  console.log(`\nCreating ${moves.length} parent directories...`);
  for (const m of moves) {
    const dstDir = dirname(m.dstAbs);
    if (!existsSync(dstDir)) mkdirSync(dstDir, { recursive: true });
  }

  console.log(`Running ${moves.length} git mv operations...`);
  // Batch in chunks of 100 to keep the command line manageable.
  for (let i = 0; i < moves.length; i++) {
    const m = moves[i];
    execSync(`git mv ${quote(m.srcRel)} ${quote(m.dstRel)}`, { cwd: REPO_ROOT });
    if ((i + 1) % 200 === 0) console.log(`  ... ${i + 1}/${moves.length}`);
  }

  console.log(`Rewriting refs in ${affected.length} files (${totalHits} swaps)...`);
  for (const p of walkMd(DOCS_DIR)) {
    let text = readFileSync(p, 'utf-8');
    let changed = false;
    for (const [from, to] of replacements) {
      if (text.includes(from)) { text = text.split(from).join(to); changed = true; }
    }
    if (changed) writeFileSync(p, text, 'utf-8');
  }
  console.log(`Done.`);
}

main();
