#!/usr/bin/env node
/**
 * Backfill `domain:` frontmatter for concepts that don't have one yet.
 *
 * Strategy (in order):
 *   1. Read `home_unit` from concept-graph.json — if the home unit has a
 *      domain, inherit it. Covers ~115/118 of the residual `uncategorized/`
 *      stubs because the build script already walked their prerequisite
 *      chains.
 *   2. For the remainder (stale prereqs that don't resolve to any unit),
 *      apply the keyword rules from scripts/propagate_domain.py.
 *
 * Default is dry-run. Pass `--write` to actually edit the .md files.
 *
 * Usage:
 *   node web/scripts/backfill-concept-domain.mjs              # preview
 *   node web/scripts/backfill-concept-domain.mjs --write      # apply
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve as resolvePath } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const DOCS_DIR = join(REPO_ROOT, 'docs', 'concepts');
const GRAPH_FILE = join(WEB_ROOT, 'src', 'data', 'concept-graph.json');

// Mirrors scripts/propagate_domain.py:12-24. The order matters — more
// specific domains come first so e.g. "삼각함수" hits 함수 not 도형.
const DOMAIN_RULES = [
  [/확률|통계|분산|표준편차|기댓값|이항분포|정규분포|이항|순열|조합|중복순열|중복조합|평균|중앙값|빈도|독립시행|조건부확률/, '확률통계'],
  [/벡터|공간|구면|구체|이차곡선|타원|쌍곡선|포물선|준선|좌표공간|법선|기하학|닮음|피타고라스|삼각비|원|호도|원주|중심각|원주각|접선의?_길이|접점|삼각형|사각형|다각형|입체|회전체|구|원기둥|원뿔|기둥/, '도형'],
  [/미분|도함수|접선의?_방정식|극값|극대|극소|극솟?값|극댓?값|변곡점|적분|역도함수|넓이의?_변화율|곡선의_미분|곡선의_접촉|미분가능성|리만|샌드위치|속도|가속도|평균변화율|함수|그래프|수열|극한|연속|지수|로그|삼각함수|호도법|삼각방정식|삼각부등식|사인|코사인|탄젠트|sin|cos|tan|log|exp|부정형/, '함수'],
  [/방정식|부등식|판별식|근의?_공식|연립|일대일대응|역함수의?_방정식|항등식/, '방정식'],
  [/다항식|인수분해|복소수|나머지정리|인수정리|식의?_계산|제곱근|루트|소인수|약수|배수|소수|수의?_체계|정수|유리수|무리수|실수|허수|절댓값|문자와_식/, '수와식'],
  [/명제|논리|역|이|대우|충분조건|필요조건|집합|원소|부분집합|벤다이어그램|진리값|배중률/, '논리'],
];

function classifyByKeyword(id) {
  for (const [pattern, domain] of DOMAIN_RULES) {
    if (pattern.test(id)) return domain;
  }
  return null;
}

// Insert/replace `domain: <value>` in the frontmatter. Places it right
// after `concept_type:` so the field order matches the rest of the
// concepts; if not present, prepends inside the `---` block.
function setDomainInFrontmatter(text, domain) {
  const existing = text.match(/^domain:\s*.*$/m);
  if (existing) {
    return text.replace(/^domain:\s*.*$/m, `domain: ${domain}`);
  }
  const ctMatch = text.match(/^concept_type:.*$/m);
  if (ctMatch) {
    return text.replace(/^(concept_type:.*)$/m, `$1\ndomain: ${domain}`);
  }
  return text.replace(/^---\n/, `---\ndomain: ${domain}\n`);
}

function main() {
  const write = process.argv.includes('--write');
  const graph = JSON.parse(readFileSync(GRAPH_FILE, 'utf-8'));
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));

  let viaHome = 0, viaKeyword = 0, alreadyHasDomain = 0, unresolved = 0, missingFile = 0;
  const planned = []; // { id, domain, via, mdPath }
  const unresolvedList = [];

  for (const node of graph.nodes) {
    if (node.domain) { alreadyHasDomain++; continue; }

    let domain = null;
    let via = '';
    if (node.home_unit) {
      const home = byId.get(node.home_unit);
      if (home?.domain) { domain = home.domain; via = 'home'; }
    }
    if (!domain) {
      const kw = classifyByKeyword(node.id);
      if (kw) { domain = kw; via = 'keyword'; }
    }
    if (!domain) { unresolved++; unresolvedList.push(node.id); continue; }

    const mdPath = join(DOCS_DIR, `${node.id}.md`);
    if (!existsSync(mdPath)) { missingFile++; continue; }
    planned.push({ id: node.id, domain, via, mdPath });
    if (via === 'home') viaHome++; else viaKeyword++;
  }

  console.log(`══ backfill-concept-domain ══`);
  console.log(`  already has domain:  ${alreadyHasDomain}`);
  console.log(`  via home_unit:       ${viaHome}`);
  console.log(`  via keyword:         ${viaKeyword}`);
  console.log(`  unresolved:          ${unresolved}`);
  console.log(`  missing .md file:    ${missingFile}`);
  if (unresolvedList.length) {
    console.log(`\nUnresolved:`);
    for (const id of unresolvedList) console.log(`    ${id}`);
  }

  // Sample to eyeball
  console.log(`\nSample plan (first 10):`);
  for (const p of planned.slice(0, 10)) {
    console.log(`  ${p.domain.padEnd(8)} (${p.via.padEnd(7)}) ← ${p.id}`);
  }
  if (planned.length > 10) console.log(`  ... and ${planned.length - 10} more.`);

  if (!write) {
    console.log(`\n(dry-run; pass --write to apply ${planned.length} changes)`);
    return;
  }

  console.log(`\nWriting ${planned.length} files...`);
  for (const p of planned) {
    const text = readFileSync(p.mdPath, 'utf-8');
    const updated = setDomainInFrontmatter(text, p.domain);
    if (updated !== text) writeFileSync(p.mdPath, updated, 'utf-8');
  }
  console.log(`Done.`);
}

main();
