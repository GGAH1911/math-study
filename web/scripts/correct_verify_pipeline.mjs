#!/usr/bin/env node
// 교정↔검증↔재교정 완전 스트리밍 파이프라인 — 3큐 동시(한 오케스트레이터):
//   ① 교정큐(correctQ)  → gemma 워커(PAR_C, 맥북 1대→1): 미교정 문제를 corrector.mjs(gemma)로 교정 → 검증큐로.
//   ② 검증큐(verifyQ)   → sonnet 워커(PAR_V, 기본4): 같은-라운드 CHUNK개씩 verify_batch 1콜 → ok 완료 / issues 재교정큐 / 기타 재투입.
//   ③ 재교정큐(recorrectQ)→ agy 워커(PAR_G, 단일인스턴스→1): issues 를 corrector.mjs(agy)로 재교정 → 검증큐 재투입.
//   gemma 는 ①에 전념, 재교정은 별 백엔드(agy)라 ①∥②∥③ 진짜 병렬. 각 백엔드(gemma/sonnet/agy) 독립.
// 상태(corrector_done / corrector_verify): 미done→교정큐 · done&verify!=ok→검증큐 · ok→완료 · quarantine→종결.
// 사용: node correct_verify_pipeline.mjs [round-필터]   env: PAR_C·PAR_V·PAR_G·MAXATT·CORRECT_BACKEND·RECORRECT_BACKEND·RUN_TS
import { readdirSync, readFileSync, existsSync, appendFileSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';

const REPO = '/home/insung/Projects/math-study';
const PROB = `${REPO}/docs/problems`;
const FILTER = process.argv[2] || '';
const PAR_C = Math.max(1, parseInt(process.env.PAR_C || '1', 10));   // 교정 동시수(gemma 맥북 1대 → 1)
const PAR_V = Math.max(1, parseInt(process.env.PAR_V || '4', 10));   // 검증 동시수(sonnet)
const PAR_G = Math.max(1, parseInt(process.env.PAR_G || '1', 10));   // 재교정 동시수(agy 단일인스턴스 → 1)
const CORRECT_BACKEND = process.env.CORRECT_BACKEND || 'gemma';      // 초기 교정 백엔드(로컬·토큰0)
const RECORRECT_BACKEND = process.env.RECORRECT_BACKEND || 'agy';    // 재교정 백엔드(gemma와 별도라 병렬)
const DUAL = process.env.DUAL === '1';   // gemma+agy 1차 병렬 + agy 공유 재교정레인. agy 단일인스턴스(동시호출 충돌)라 재교정·1차를 agy 워커 1개가 번갈아.
const OR_AVAILABLE = existsSync((process.env.HOME || '') + '/.config/math-study/openrouter.key');  // OpenRouter gemma-4-26b:free 레인(기본 off — 무료풀 429. OR_LANE=1로 켬)
const GEMMA_PAR = Math.max(1, parseInt(process.env.GEMMA_PAR || '2', 10));  // 로컬 26b 동시 워커수(mlx continuous batching → ~N배). 32GB라 2 안전(검증)
const MAXATT = Math.max(1, parseInt(process.env.MAXATT || '3', 10));
const SKIP_TABLE = process.env.SKIP_TABLE === '1' || process.env.CLEAN_ONLY === '1';  // {{TABLE}} 보유 교정완료분 제외(재추출 배치 B용)
const CHUNK = 5;
const LOGDIR = '/tmp/ingest_logs';
if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const TS = process.env.RUN_TS || String(Math.floor(Date.now() / 1000));
const LOG = `${LOGDIR}/pipeline_${TS}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };

function* walk(d) {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const p = `${d}/${e.name}`;
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.endsWith('.md')) yield p;
  }
}
const slugOf = (md) => md.split('/').pop().replace(/\.md$/, '');
const mdText = (md) => readFileSync(md, 'utf8');
function stateOf(md) {
  const t = mdText(md);
  if (/^corrector_quarantine:\s*true/m.test(t)) return 'quarantine';
  const m = t.match(/\ncorrector_verify:\s*(.*)/);
  return m ? m[1].trim() : 'none';
}
const isDone = (md) => /^corrector_done:\s*true/m.test(mdText(md));
function parseSlug(slug) { const m = slug.match(/^(.+)_([가-힣A-Za-z]+)_(\d+)$/); return m ? { slug, round: m[1], subj: m[2], num: m[3] } : null; }
function run(cmd, args, env = {}) {
  return new Promise((res) => {
    const c = spawn(cmd, args, { cwd: `${REPO}/web`, env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] });
    let out = ''; c.stdout.on('data', (d) => out += d); c.stderr.on('data', (d) => out += d);
    c.on('close', (code) => res({ code, out }));
  });
}

// 초기 대상 수집 → 미교정=교정큐, 교정완료&미ok=검증큐
const items = new Map();   // slug -> {md, att}
const correctQ = [], verifyQ = [], recorrectQ = [];
for (const md of walk(PROB)) {
  const slug = slugOf(md); const p = parseSlug(slug); if (!p) continue;
  if (FILTER && !p.round.includes(FILTER)) continue;
  const t = mdText(md);
  if (/^corrector_quarantine:\s*true/m.test(t)) continue;
  if (/^corrector_done:\s*true/m.test(t)) {                       // 이미 교정됨 → 검증 대상(미ok만)
    const stm = t.match(/\ncorrector_verify:\s*(.*)/); const st = stm ? stm[1].trim() : 'none';
    if (st === 'ok') continue;
    if (SKIP_TABLE) {
      const sx = t.match(/\nsearchable_text: \|\n((?:  .*\n?|\n)*?)(?=\n\w)/);
      if ((sx ? sx[1] : '').includes('{{TABLE')) continue;
    }
    items.set(slug, { md, att: 0 }); verifyQ.push(slug);
  } else {                                                        // 미교정 → 교정큐(gemma)
    items.set(slug, { md, att: 0 }); correctQ.push(slug);
  }
}
let cActive = 0, vActive = 0, gActive = 0, done = 0, failed = 0;
const total = items.size;
const orOn = process.env.OR_LANE === '1' && OR_AVAILABLE;
const modeStr = DUAL
  ? `교정 gemma×${GEMMA_PAR}(로컬26b)${orOn ? '+OR' : ''} ∥ 검증 ${PAR_V}(sonnet) ∥ 재교정 agy(쿼터소진→sonnet)${orOn ? '+OR' : ''}`
  : `교정 ${PAR_C}(${CORRECT_BACKEND}) ∥ 검증 ${PAR_V}(sonnet) ∥ 재교정 ${PAR_G}(${RECORRECT_BACKEND})`;
log(`══ pipeline 시작: 대상 ${total}문제${FILTER ? ` (필터:${FILTER})` : ''} (교정대기 ${correctQ.length} · 검증대기 ${verifyQ.length}) · ${modeStr} · LOG ${LOG}`);
if (!total) { log('대상 0 — 종료'); process.exit(0); }

let lastBeat = 0;
function beat() {
  const now = Date.now();
  if (now - lastBeat < 15000) return; lastBeat = now;
  log(`   진행: 완료 ${done}/${total} · 실패 ${failed} · 교정큐 ${correctQ.length}(${cActive}) · 검증큐 ${verifyQ.length}(${vActive}) · 재교정큐 ${recorrectQ.length}(${gActive})`);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// 전 시스템 유휴(3큐 비고 in-flight 0)일 때만 종료 — enqueue 는 항상 active-- 전이라 항목 유실 없음.
const idle = () => correctQ.length === 0 && verifyQ.length === 0 && recorrectQ.length === 0 && cActive === 0 && vActive === 0 && gActive === 0;

// ① 교정 워커(gemma): 미교정 → corrector.mjs(gemma) → 검증큐
async function correctWorker() {
  while (true) {
    if (!correctQ.length) { if (idle()) break; await sleep(300); continue; }
    const slug = correctQ.shift(); const it = items.get(slug); const p = parseSlug(slug);
    cActive++;
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: CORRECT_BACKEND });
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 교정 격리`); }
    else if (r.code === 3) { correctQ.push(slug); await sleep(2000); }   // gemma 빈출력(부하) → 재시도
    else verifyQ.push(slug);                                             // 교정 완료 → 검증큐
    cActive--; beat();
  }
}
// ② 검증 워커(sonnet): 같은-라운드 CHUNK개 verify_batch 1콜 → ok 완료 / issues 재교정큐 / 기타 재투입(상한)
async function verifyWorker() {
  while (true) {
    if (!verifyQ.length) { if (idle()) break; await sleep(300); continue; }
    const r0 = parseSlug(verifyQ[0]).round; const chunk = [];
    while (chunk.length < CHUNK && verifyQ.length && parseSlug(verifyQ[0]).round === r0) chunk.push(verifyQ.shift());
    vActive++;
    await run('node', ['scripts/verify_batch.mjs', '--list', chunk.join(','), '--chunk', String(CHUNK), '--par', '1', '--force'], { RUN_TS: TS });
    for (const slug of chunk) {
      const it = items.get(slug); const st = stateOf(it.md);
      if (st === 'ok') { done++; }
      else if (st === 'issues') { recorrectQ.push(slug); }
      else { it.att++; if (it.att < MAXATT) verifyQ.push(slug); else { failed++; log(`  ✗ ${slug} 검증실패 상한(${st})`); } }
    }
    vActive--; beat();
  }
}
// ③ 재교정 워커(agy): issues → corrector.mjs(agy) → 검증큐 재투입(격리 시 종결)
async function recorrectWorker() {
  while (true) {
    if (!recorrectQ.length) { if (idle()) break; await sleep(300); continue; }
    const slug = recorrectQ.shift(); const it = items.get(slug); const p = parseSlug(slug);
    gActive++;
    if (it.att >= MAXATT) { failed++; gActive--; log(`  ✗ ${slug} 재교정 상한 — issues 잔존`); continue; }
    it.att++;
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: RECORRECT_BACKEND });
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 격리(재교정 실패)`); }
    else if (r.code === 3) { recorrectQ.push(slug); await sleep(2000); }
    else verifyQ.push(slug);
    gActive--; beat();
  }
}

// ③' agy 공유 레인(DUAL): 재교정(우선) + 1차교정(여유분). agy 단일인스턴스라 워커 1개가 둘을 번갈아 → 충돌 0.
async function agyLaneWorker() {
  while (true) {
    let slug, mode;
    if (recorrectQ.length) { slug = recorrectQ.shift(); mode = 're'; }     // 재교정 전용(1차는 gemma×2 전담, agy는 재교정만 — 사용자 지정)
    else { if (idle()) break; await sleep(300); continue; }
    const it = items.get(slug); const p = parseSlug(slug);
    gActive++;
    if (mode === 're') {
      if (it.att >= MAXATT) { failed++; gActive--; log(`  ✗ ${slug} 재교정 상한 — issues 잔존`); continue; }
      it.att++;
    }
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: 'agy' });
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 격리(agy ${mode})`); }
    else if (r.code === 3) { (mode === 're' ? recorrectQ : correctQ).push(slug); await sleep(2000); }
    else verifyQ.push(slug);
    gActive--; beat();
  }
}
// ③'' OpenRouter gemma-4-26b:free 3번째 병렬 레인(agy 미러: 재교정 우선 + 1차 여유분). 별도 무료풀이라 agy와 동시. 429=빈출력→재투입(긴 sleep).
async function orLaneWorker() {
  while (true) {
    let slug, mode;
    if (recorrectQ.length) { slug = recorrectQ.shift(); mode = 're'; }
    else if (correctQ.length) { slug = correctQ.shift(); mode = 'co'; }
    else { if (idle()) break; await sleep(300); continue; }
    const it = items.get(slug); const p = parseSlug(slug);
    gActive++;
    if (mode === 're') {
      if (it.att >= MAXATT) { failed++; gActive--; log(`  ✗ ${slug} 재교정 상한 — issues 잔존`); continue; }
      it.att++;
    }
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: 'or' });
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 격리(or ${mode})`); }
    else if (r.code === 3) { (mode === 're' ? recorrectQ : correctQ).push(slug); await sleep(5000); }  // 429/빈출력 → 재투입, 긴 backoff
    else verifyQ.push(slug);
    gActive--; beat();
  }
}

await Promise.all(DUAL ? [
  ...Array.from({ length: GEMMA_PAR }, correctWorker),   // 로컬 26b ×GEMMA_PAR (mlx continuous batching → ~N배)
  agyLaneWorker(),                                       // agy(쿼터소진→sonnet) 재교정 전용(1차는 gemma×2)
  ...(orOn ? [orLaneWorker()] : []),                     // OR 레인 기본 off(무료풀 429), OR_LANE=1로 켬
  ...Array.from({ length: PAR_V }, verifyWorker),
] : [
  ...Array.from({ length: PAR_C }, correctWorker),
  ...Array.from({ length: PAR_V }, verifyWorker),
  ...Array.from({ length: PAR_G }, recorrectWorker),
]);

const fin = { ok: 0, issues: 0, parsefail: 0, quarantine: 0, none: 0 };
for (const [, it] of items) { const s = stateOf(it.md); fin[s] = (fin[s] || 0) + 1; }
log(`══ 완료: 대상 ${total} → ok ${fin.ok} · issues ${fin.issues} · parsefail ${fin.parsefail} · 격리 ${fin.quarantine} · 미처리 ${fin.none} (완료 ${done} · 실패 ${failed})`);
