#!/usr/bin/env node
// redraw 재현 벌크 채점 — 그리기=gemma4, 채점=Opus.
//   verify_batch 패턴: 1콜에 N도형 묶음(CHUNK 5) + clean cwd/DISABLE_GIT 프롬프트캐싱(cache_read ~76%↓ 분산) + 라인파싱(parsefail 차단).
//   각 도형: [원본 이미지]+[재현 이미지(figrender-plot screenshot)]+[본문] → docs/report/REDRAW_RUBRIC.md 8항목 채점.
//   결과(verdict/total/①/issue)를 /tmp/redraw_specs/<id>.json 에 기록(갤러리 뱃지).
// 사용: node web/scripts/redraw_score_batch.mjs [--list id1,id2] [--chunk 5] [--model opus] [--norender]
import { spawn, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, existsSync, readdirSync, mkdirSync } from 'node:fs';

const REPO = '/home/insung/Projects/math-study';
const SPECS = '/tmp/redraw_specs';
const RENDERS = '/tmp/redraw_renders';
const LOGDIR = '/tmp/ingest_logs';
const PORT = process.env.MATH_STUDY_PORT || '4325';
const A = process.argv.slice(2);
const getOpt = (k, d = null) => { const i = A.indexOf(k); return i >= 0 && A[i + 1] ? A[i + 1] : d; };
const CHUNK = parseInt(getOpt('--chunk', '5'), 10);
const MODEL = getOpt('--model', 'opus');
const NORENDER = A.includes('--norender');
for (const d of [RENDERS, LOGDIR]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const CLEAN_DIR = '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });
const TS = String(Math.floor(Date.now() / 1000));
const LOG = `${LOGDIR}/redraw_score_${TS}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };
const RUBRIC = readFileSync(`${REPO}/docs/report/REDRAW_RUBRIC.md`, 'utf8');

function ids() {
  const list = getOpt('--list');
  if (list) return list.split(',').map((s) => s.trim()).filter(Boolean);
  return readdirSync(SPECS).filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, '')).sort();
}
function bonmun(id) {  // id=<round>_<subj>_<num> → md searchable_text
  const m = id.match(/^(.+)_([^_]+)_(\d+)$/); if (!m) return '';
  const [, round, subj, num] = m;
  const base = `${REPO}/docs/problems/${round.split('_')[0]}`;
  if (!existsSync(base)) return '';
  for (const sub of readdirSync(base)) for (const nm of [`${id}.md`, `${round}_${subj}_${String(num).padStart(2, '0')}.md`]) {
    const p = `${base}/${sub}/${nm}`;
    if (existsSync(p)) { const t = readFileSync(p, 'utf8'); const mm = t.match(/\nsearchable_text: \|\n((?:  .*\n?)*)/); if (mm) return mm[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join(' ').replace(/\{\{[^}]+\}\}/g, '').replace(/\s+/g, ' ').trim().slice(0, 500); }
  }
  return '';
}
function renderOne(id) {  // figrender-plot?id= → /tmp/redraw_renders/<id>.png
  const out = `${RENDERS}/${id}.png`;
  spawnSync('google-chrome-stable', ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--window-size=560,470', '--virtual-time-budget=11000', `--screenshot=${out}`, `http://127.0.0.1:${PORT}/dev/figrender-plot?id=${encodeURIComponent(id)}&w=520`], { timeout: 30000 });
  return existsSync(out) ? out : null;
}
function claudeCall(prompt, dirs) {
  return new Promise((res) => {
    const args = ['-p', prompt, '--model', MODEL, '--output-format', 'json'];
    for (const d of dirs) { args.push('--add-dir', d); }
    const c = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    let out = ''; c.stdout.on('data', (d) => (out += d));
    c.on('close', () => { try { const j = JSON.parse(out); const u = j.usage || {}; appendFileSync(`${LOGDIR}/redraw_score_usage.log`, `${MODEL}\tcr=${u.cache_read_input_tokens ?? '?'}\tcc=${u.cache_creation_input_tokens ?? '?'}\tin=${u.input_tokens ?? '?'}\tout=${u.output_tokens ?? '?'}\n`); res(j.result || ''); } catch { res(''); } });
  });
}
function saveScore(id, r) {
  const f = `${SPECS}/${id}.json`; const o = JSON.parse(readFileSync(f, 'utf8'));
  o.verdict = r.verdict; o.score = r.total; o.bonmunFit = r.bonmun; o.issue = r.issue; o.scoredBy = MODEL; o.scoredAt = new Date().toISOString();
  writeFileSync(f, JSON.stringify(o));
}
async function scoreChunk(items) {
  let prompt = `다음 ${items.length}개 기출 함수그래프 재현(redraw)을 채점한다. 각 도형마다 [원본 이미지]·[재현 이미지]·[본문]을 비교해 아래 채점기준으로 0~40점 채점하라. ★문제를 풀지 마라(채점만). 이미지 둘 다 Read 로 본다.

${RUBRIC}

★출력은 각 도형당 **정확히 한 줄**, 아래 형식만(JSON·설명·코드펜스 금지):
N|verdict|total|bonmun|issue
- N = 아래 [도형 N]의 N(1,2,…). verdict = pass 또는 fix. total = 8항목 합계(0~40). bonmun = ①본문정합성 점수(0~5). issue = 가장 큰 결함 1개(50자 이내, 없으면 -).
- ★①본문정합성 3 미만이면 verdict=fix. 점좌표·k·곡선식을 본문 조건으로 유도해 재현값과 수치 대조(눈대중 금지).
총 ${items.length}줄만.`;
  items.forEach((it, i) => { prompt += `\n\n[도형 ${i + 1}] 원본: ${it.orig} · 재현: ${it.render} · 본문: ${it.bonmun || '(본문 없음 — 이미지만 대조)'}`; });
  const t0 = Date.now();
  const out = await claudeCall(prompt, [`${REPO}/web/private/problem-images`, RENDERS]);
  const sec = ((Date.now() - t0) / 1000).toFixed(0);
  const vmap = new Map();
  for (const line of out.split('\n')) {
    const m = line.trim().match(/^(\d+)\s*\|\s*(pass|fix)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*)$/i);
    if (m) vmap.set(parseInt(m[1], 10), { verdict: m[2].toLowerCase(), total: +m[3], bonmun: +m[4], issue: m[5].trim() });
  }
  let done = 0, pf = 0;
  for (let i = 0; i < items.length; i++) {
    const r = vmap.get(i + 1);
    if (!r) { pf++; continue; }
    saveScore(items[i].id, r); done++;
  }
  if (pf) appendFileSync(`${LOGDIR}/redraw_score_pf_${TS}.txt`, `청크[${items.map((i) => i.id).join(',')}] pf${pf}\n${out.slice(0, 800)}\n`);
  log(`  청크[${items.map((i) => i.id.slice(-12)).join(',')}] ${sec}s → 채점 ${done}${pf ? ` / pf ${pf}` : ''}`);
}
(async () => {
  const all = ids();
  log(`══ redraw 채점 시작: ${all.length}도형 · 청크 ${CHUNK} · ${MODEL} · LOG ${LOG}`);
  const items = [];
  for (const id of all) {
    const spec = JSON.parse(readFileSync(`${SPECS}/${id}.json`, 'utf8'));
    const orig = `${REPO}/web/public${spec.img}`;
    let render = `${RENDERS}/${id}.png`;
    if (!NORENDER) { const r = renderOne(id); if (r) render = r; }
    if (!existsSync(orig)) { log(`  ⚠ ${id} 원본없음 skip`); continue; }
    if (!existsSync(render)) { log(`  ⚠ ${id} 재현렌더 실패 skip`); continue; }
    items.push({ id, orig, render, bonmun: bonmun(id) });
  }
  log(`  렌더+준비 ${items.length}도형`);
  for (let i = 0; i < items.length; i += CHUNK) await scoreChunk(items.slice(i, i + CHUNK));
  log(`══ 완료: ${items.length}도형 채점 → /tmp/redraw_specs/*.json (verdict/score/issue)`);
})();
