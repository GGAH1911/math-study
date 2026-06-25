#!/usr/bin/env node
// redraw 수렴 루프 — ★만점(40/40)까지 반복. 그리기=gemma4, 채점=Opus.
//   라운드: [채점(Opus 벌크)] → 미만점 추림 → [gemma 재그리기(채점 피드백 주입, 2병렬)] → 반복.
//   만점이면 그 도형은 고정(재측정 안 함). 전부 만점 or MAXROUND 도달 시 종료.
// 사용: node web/scripts/redraw_loop.mjs [--list id1,id2] [--target 40] [--rounds 6]
import { spawn, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';

const REPO = '/home/insung/Projects/math-study';
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
    const fbf = `/tmp/loop_fb_${id}.txt`; writeFileSync(fbf, `현재 ${s.score ?? '?'}/40, 결함: ${s.issue || '(없음)'}\n채점기준의 라벨(누락·겹침·앵커링·KaTeX 잘림)·본문정합성을 특히 점검.`);
    const out = `/tmp/loop_s_${id}.json`;
    const c = spawn('node', [`${REPO}/web/scripts/gemma_measure.mjs`, img, bf, out, fbf], { stdio: ['ignore', 'pipe', 'pipe'] });
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
    const toScore = all.filter((id) => { const s = rd(id); return (s.score ?? -1) < TARGET; });  // 미만점만 채점(만점 고정)
    log(`── 라운드 ${round}: 채점대상 ${toScore.length}`);
    if (toScore.length) spawnSync('node', [`${REPO}/web/scripts/redraw_score_batch.mjs`, '--list', toScore.join(','), '--chunk', '5', '--model', 'opus'], { stdio: 'inherit', timeout: 900000 });
    const scored = all.map((id) => ({ id, ...rd(id) }));
    const perfect = scored.filter((s) => (s.score ?? 0) >= TARGET);
    const failing = scored.filter((s) => (s.score ?? 0) < TARGET);
    log(`   결과: 만점 ${perfect.length}/${all.length} · 미만점 ${failing.length}`);
    for (const s of failing) log(`     ${s.id} ${s.score ?? '?'}/40 ·①${s.bonmunFit ?? '?'} · ${(s.issue || '').slice(0, 50)}`);
    if (!failing.length) { log(`🎉 전부 만점 달성 (라운드 ${round})`); break; }
    if (round === MAXROUND) { log(`⏹ 최대 라운드 도달 — 미만점 ${failing.length} 잔존(최선값 유지)`); break; }
    log(`   ↻ gemma 재측정 ${failing.length}도형 (피드백 주입, 2병렬)`);
    await par2(failing.map((s) => s.id), remeasure);
  }
  log(`══ 루프 종료`);
})();
