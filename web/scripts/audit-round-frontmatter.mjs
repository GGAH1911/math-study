#!/usr/bin/env node
/**
 * 단일 회차의 problem .md 들에 대해 frontmatter searchable_text 와 이미지를
 * cross-check. heuristic만 — LLM 호출 없음. 의심 케이스를 catalog.
 *
 * 사용 예:
 *   node audit-round-frontmatter.mjs --round 2025_수능
 *   node audit-round-frontmatter.mjs --round 2025_수능 --html /tmp/audit.html
 *
 * 본격 LLM-기반 audit/fix는 별도 subagent 흐름 (skill 안내 참조).
 * 이 스크립트는 신규 인제스트 직후 "어느 problem이 의심스러운지" 빠르게 보여
 * 사용자가 subagent 호출 우선순위를 정하도록.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename, resolve } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);

function arg(name, def) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : def;
}

const round = arg('round');
const htmlOut = arg('html');
if (!round) { console.error('--round <slug> required'); process.exit(1); }

const problemsDir = join(REPO_ROOT, 'docs', 'problems');
const files = readdirSync(problemsDir).filter((f) => f.startsWith(`${round}_`) && f.endsWith('.md'));
if (files.length === 0) { console.error(`no problems for round ${round}`); process.exit(1); }

const findings = []; // { file, suspect, reasons[] }
for (const fname of files) {
  const file = join(problemsDir, fname);
  const { data: fm } = matter(readFileSync(file, 'utf-8'));
  const st = (fm.searchable_text ?? '').trim();
  const reasons = [];
  // 휴리스틱 단서
  if (!st) reasons.push('searchable_text 비어있음');
  if (/⋄|글리프|placeholder|표현 불가능한/.test(st)) reasons.push('OCR placeholder/글리프 깨짐');
  if (st.length < 40) reasons.push(`너무 짧음 (${st.length}자)`);
  if (st.length > 1500) reasons.push(`너무 김 (${st.length}자) — 인접 문제 cross-contamination 의심`);
  if (/\.\.\.$/.test(st) || /\sa\.\.\.$/.test(st)) reasons.push('truncated (...)');
  if (fm.has_figure && !/그림|좌표|점|선분|원|각|삼각|사각|반지름|호|접선|기울기/.test(st)) {
    reasons.push('has_figure=true 인데 도형 묘사 키워드 없음');
  }
  if (!fm.answer) reasons.push('answer 누락');
  if (!fm.exam_intent) reasons.push('exam_intent 누락');
  if (fm.unit === 'None' || fm.unit === null) reasons.push('unit 분류 실패');
  if (reasons.length > 0) findings.push({ file: fname, reasons, image: fm.image_paths?.[0] });
}

console.log(`[audit] round=${round}: ${files.length} problems, ${findings.length} suspect`);
for (const f of findings.slice(0, 20)) {
  console.log(`  ${f.file}`);
  for (const r of f.reasons) console.log(`    - ${r}`);
}
if (findings.length > 20) console.log(`  ... +${findings.length - 20} more`);

if (htmlOut) {
  const html = `<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><title>Audit ${round}</title>
<style>
body { font: 14px/1.5 system-ui, sans-serif; max-width: 1100px; margin: 2em auto; padding: 0 1em; color: #222; }
h1 { font-size: 1.4em; margin-bottom: 0.2em; }
.summary { background: #f4f4f4; padding: 0.8em 1em; border-radius: 6px; margin: 1em 0; }
.suspect { border: 1px solid #ddd; border-left: 4px solid #f59e0b; padding: 0.6em 1em; margin: 0.6em 0; border-radius: 4px; }
.suspect h3 { margin: 0 0 0.4em; font-size: 1em; }
.suspect ul { margin: 0; padding-left: 1.4em; color: #b45309; }
.suspect img { max-width: 400px; max-height: 200px; border: 1px solid #ddd; margin-top: 0.6em; }
.empty { color: #6b7280; }
</style></head><body>
<h1>Frontmatter audit — ${round}</h1>
<div class="summary"><b>${files.length}</b> problem 중 <b>${findings.length}</b> 의심 (heuristic 기반)</div>
${findings.length === 0 ? '<p class="empty">의심 항목 없음 ✓</p>' :
  findings.map((f) => `<div class="suspect">
    <h3>${f.file}</h3>
    <ul>${f.reasons.map((r) => `<li>${r}</li>`).join('')}</ul>
    ${f.image ? `<img src="/${f.image}" alt="">` : ''}
  </div>`).join('\n')}
</body></html>`;
  writeFileSync(htmlOut, html, 'utf-8');
  console.log(`\nHTML report: ${htmlOut}`);
}
