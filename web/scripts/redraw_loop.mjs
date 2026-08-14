#!/usr/bin/env node
// redraw 수렴 루프 — ★만점(40/40)까지 반복. 그리기=gemma4, 채점=Opus.
//   라운드: [채점(Opus 벌크)] → 미만점 추림 → [gemma 재그리기(채점 피드백 주입, 2병렬)] → 반복.
//   만점이면 그 도형은 고정(재측정 안 함). 전부 만점 or MAXROUND 도달 시 종료.
// 사용: node web/scripts/redraw_loop.mjs [--list id1,id2] [--target 40] [--rounds 6]
import { spawn, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';

const REPO = process.env.MATHSTUDY_ROOT || new URL('../..', import.meta.url).pathname.replace(/\/$/, '');  // ★레포 위치 자동(이동 내성)
const SPECS = '/tmp/redraw_specs';
const LOGDIR = '/tmp/ingest_logs';
const A = process.argv.slice(2);
const getOpt = (k, d) => { const i = A.indexOf(k); return i >= 0 && A[i + 1] ? A[i + 1] : d; };
const TARGET = parseInt(getOpt('--target', '40'), 10);
const MAXROUND = parseInt(getOpt('--rounds', '6'), 10);
if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const TS = String(Math.floor(Date.now() / 1000));
const LOG = `${LOGDIR}/redraw_loop_${TS}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };
const rd = (id) => JSON.parse(readFileSync(`${SPECS}/${id}.json`, 'utf8'));
const wr = (id, o) => writeFileSync(`${SPECS}/${id}.json`, JSON.stringify(o));

function ids() {
  const list = getOpt('--list', null);
  if (list) return list.split(',').map((s) => s.trim()).filter(Boolean);
  return readdirSync(SPECS).filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, '')).sort();
}
function bonmun(id) {  // md searchable_text (ground truth)
  const m = id.match(/^(.+)_([^_]+)_(\d+)$/); if (!m) return '';
  const [, round, subj, num] = m; const base = `${REPO}/docs/problems/${round.split('_')[0]}`;
  if (!existsSync(base)) return '';
  for (const sub of readdirSync(base)) for (const nm of [`${id}.md`, `${round}_${subj}_${String(num).padStart(2, '0')}.md`]) {
    const p = `${base}/${sub}/${nm}`;
    if (existsSync(p)) { const mm = readFileSync(p, 'utf8').match(/\nsearchable_text: \|\n((?:  .*\n?)*)/); if (mm) return mm[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join(' ').replace(/\{\{[^}]+\}\}/g, '').replace(/\s+/g, ' ').trim().slice(0, 500); }
  }
  return '';
}
function remeasure(id) {  // gemma 재측정(채점 피드백 주입) → spec 갱신, score 삭제(재채점 대상)
  return new Promise((res) => {
    const s = rd(id);
    const img = `${REPO}/web/public${s.img}`;
    const bf = `/tmp/loop_b_${id}.txt`; writeFileSync(bf, bonmun(id) || s.note || '');
    const base = s._best ?? s.spec;   // ★최고점 spec 기반으로 개선(회귀 방지)
    const fbf = `/tmp/loop_fb_${id}.txt`; writeFileSync(fbf, `★이전 재현 spec(이걸 기반으로 지적된 결함만 고치고 잘 된 부분은 그대로 유지):\n${JSON.stringify(base)}\n\n채점(${s._bestScore ?? s.score ?? '?'}/40) 결함: ${s._bestIssue ?? s.issue ?? '(없음)'}\n특히 라벨(누락·겹침·잘림)·본문정합성(곡선식·k값·점위치)·음영영역(맞는 도형)을 점검.`);
    const out = `/tmp/loop_s_${id}.json`;
    const MEAS = process.env.MEASURE_SCRIPT || 'redraw_opus_measure.mjs';   // ★수정=Opus(품질). gemma_measure.mjs 로 오버라이드 가능
    const c = spawn('node', [`${REPO}/web/scripts/${MEAS}`, img, bf, out, fbf], { stdio: ['ignore', 'pipe', 'pipe'] });
    c.on('close', () => {
      if (existsSync(out)) { try { const ns = JSON.parse(readFileSync(out, 'utf8')); s.spec = ns; delete s.score; delete s.verdict; delete s.issue; wr(id, s); log(`    ↻ ${id} 재측정 완료`); } catch { log(`    ✗ ${id} 재측정 파싱실패`); } }
      else log(`    ✗ ${id} 재측정 출력없음`);
      res();
    });
  });
}
async function par2(items, fn) { let i = 0; const w = async () => { while (i < items.length) await fn(items[i++]); }; await Promise.all([w(), w()]); }  // gemma 최대 2병렬

(async () => {
  const all = ids();
  log(`══ redraw 수렴 루프: ${all.length}도형 · 목표 ${TARGET}/40 · 최대 ${MAXROUND}라운드 · LOG ${LOG}`);
  for (let round = 1; round <= MAXROUND; round++) {
    const pending = all.filter((id) => { const s = rd(id); return Math.max(s._bestScore ?? -1, s.score ?? -1) < TARGET; });  // best<40만
    log(`── 라운드 ${round}: 미만점 ${pending.length}/${all.length}`);
    if (!pending.length) { log(`🎉 전부 만점 달성 (라운드 ${round - 1})`); break; }
    log(`   ↻ Opus 재측정 ${pending.length} (${round === 1 ? '신규측정' : 'best 기반 수정'}, 2병렬)`); await par2(pending, remeasure);
    spawnSync('node', [`${REPO}/web/scripts/redraw_score_batch.mjs`, '--list', pending.join(','), '--chunk', '5', '--model', 'opus'], { stdio: 'inherit', timeout: 900000 });
    for (const id of pending) { const s = rd(id); if ((s.score ?? -1) > (s._bestScore ?? -1)) { s._best = s.spec; s._bestScore = s.score; s._bestIssue = s.issue; s._bestBon = s.bonmunFit; wr(id, s); } }  // ★keep-best
    const best = all.map((id) => { const s = rd(id); return { id, b: s._bestScore ?? 0, i: s._bestIssue ?? s.issue ?? '' }; });
    log(`   결과(best): 만점 ${best.filter((x) => x.b >= TARGET).length}/${all.length}`);
    for (const x of best) log(`     ${x.id} best ${x.b}/40 · ${(x.i || '').slice(0, 50)}`);
    if (round === MAXROUND) log(`⏹ 최대 라운드 — best 유지`);
  }
  for (const id of all) { const s = rd(id); if (s._best) { s.spec = s._best; s.score = s._bestScore; s.issue = s._bestIssue; s.bonmunFit = s._bestBon; wr(id, s); } }  // best 복원
  log(`══ 루프 종료`);
})();
