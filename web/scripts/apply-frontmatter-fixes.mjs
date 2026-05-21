#!/usr/bin/env node
/**
 * Apply frontmatter fixes from /tmp/fix_results_*.json to docs/problems/*.md.
 *
 * Each fix entry: { file, new_searchable_text, new_exam_intent }
 * Patches two fields safely (line-based YAML edit, no gray-matter stringify
 * to avoid reordering other fields):
 *   - `exam_intent: "..."` (one-line, double-quoted, backslash-escaped)
 *   - `searchable_text: |` (multi-line block, 2-space indent)
 *
 * Usage:
 *   node apply-frontmatter-fixes.mjs           # dry-run
 *   node apply-frontmatter-fixes.mjs --apply   # actually patch
 *
 * Outputs summary + per-file action log. Failed patches → docs/audits/fix-failures.json
 */
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);
const FIX_GLOB_DIR = '/tmp';
const FAILURE_LOG = resolve(REPO_ROOT, 'docs', 'audits', 'fix-failures.json');

const APPLY = process.argv.includes('--apply');

// 1) 8 wave JSON 통합 + dedup
const allFixes = [];
const seenFiles = new Set();
let skippedAtSource = 0;
for (const f of readdirSync(FIX_GLOB_DIR)) {
  if (!/^fix_results_\d+\.json$/.test(f)) continue;
  let arr;
  try { arr = JSON.parse(readFileSync(join(FIX_GLOB_DIR, f), 'utf-8')); }
  catch (e) { console.warn(`skip ${f}: ${e.message}`); continue; }
  if (!Array.isArray(arr)) continue;
  for (const e of arr) {
    if (e.skip) { skippedAtSource++; continue; }
    if (!e.file || !e.new_searchable_text) continue;
    if (seenFiles.has(e.file)) continue; // dedup (한 파일이 두 wave 에 중복 나오는 경우 첫 번째만)
    seenFiles.add(e.file);
    allFixes.push(e);
  }
}

console.log(`\n=== apply-frontmatter-fixes (${APPLY ? 'APPLY' : 'DRY-RUN'}) ===`);
console.log(`총 fix entries: ${allFixes.length} (subagent skipped: ${skippedAtSource})`);

// 2) frontmatter 영역 안전 patch — line-based.
//    `searchable_text: |` 블록: 다음 줄부터 indented (2+ space) 라인을 그 블록의 child로 간주.
//    indent 없는 다음 `^[a-z_]:` 필드 또는 `---` 만나면 stop.
function patch(text, newSearchable, newIntent) {
  const lines = text.split('\n');
  if (lines[0] !== '---') throw new Error('no frontmatter open');
  let fmEnd = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i] === '---') { fmEnd = i; break; }
  }
  if (fmEnd < 0) throw new Error('no frontmatter close');

  // exam_intent — YAML double-quote: `\` 와 `"` escape. 줄바꿈은 \n 으로.
  if (newIntent != null) {
    const intentEscaped = String(newIntent)
      .replace(/\\/g, '\\\\')
      .replace(/"/g, '\\"')
      .replace(/\n/g, '\\n');
    let replaced = false;
    for (let i = 1; i < fmEnd; i++) {
      if (/^exam_intent:\s*/.test(lines[i])) {
        lines[i] = `exam_intent: "${intentEscaped}"`;
        replaced = true;
        break;
      }
    }
    if (!replaced) {
      // 키가 없으면 append (frontmatter end 직전)
      lines.splice(fmEnd, 0, `exam_intent: "${intentEscaped}"`);
      fmEnd++;
    }
  }

  // searchable_text — multi-line block scalar `|`. 기존 블록 제거 + 새 블록 삽입.
  let stIdx = -1;
  for (let i = 1; i < fmEnd; i++) {
    if (/^searchable_text:\s*\|?\s*$/.test(lines[i])) { stIdx = i; break; }
  }
  // 새 블록 구성 — `|` (literal) 사용, 2-space indent, 줄바꿈 보존.
  const stLines = [
    'searchable_text: |',
    ...String(newSearchable).split('\n').map((l) => '  ' + l),
  ];

  if (stIdx >= 0) {
    // 기존 블록 길이 — `^  ` (2-space indent) 또는 `^   `… 인 줄들이 child.
    // 단순 규칙: stIdx 다음 줄부터 `^[a-zA-Z_]` 또는 `---` 만날 때까지 child로 간주.
    let j = stIdx + 1;
    while (j < fmEnd && !/^[A-Za-z_]/.test(lines[j]) && lines[j] !== '---') {
      j++;
    }
    const removed = j - stIdx;
    lines.splice(stIdx, removed, ...stLines);
    fmEnd += stLines.length - removed;
  } else {
    // 키 없으면 frontmatter 끝에 append
    lines.splice(fmEnd, 0, ...stLines);
  }

  return lines.join('\n');
}

// 3) 각 fix 적용
const failures = [];
let applied = 0;
let dryShown = 0;
for (const fix of allFixes) {
  const path = resolve(REPO_ROOT, fix.file);
  if (!existsSync(path)) { failures.push({ file: fix.file, error: 'file missing' }); continue; }
  const orig = readFileSync(path, 'utf-8');
  let patched;
  try { patched = patch(orig, fix.new_searchable_text, fix.new_exam_intent); }
  catch (e) { failures.push({ file: fix.file, error: e.message }); continue; }
  if (patched === orig) continue; // no-op (이미 같은 값)
  if (APPLY) {
    writeFileSync(path, patched, 'utf-8');
    applied++;
  } else if (dryShown < 3) {
    console.log(`\n--- DRY-RUN preview ${fix.file} ---`);
    console.log(patched.split('\n').slice(0, 35).join('\n'));
    dryShown++;
  }
}

console.log();
console.log(`적용: ${APPLY ? applied : 'DRY-RUN (' + (allFixes.length - failures.length) + ' 예정)'}`);
console.log(`실패: ${failures.length}`);

if (failures.length > 0) {
  if (APPLY) {
    writeFileSync(FAILURE_LOG, JSON.stringify({ ts: new Date().toISOString(), failures }, null, 2), 'utf-8');
    console.log(`실패 catalog: ${FAILURE_LOG}`);
  } else {
    console.log('실패 예시:');
    for (const f of failures.slice(0, 5)) console.log(`  ${f.file}: ${f.error}`);
  }
}
