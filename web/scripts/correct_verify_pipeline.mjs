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
const CORRECT_ONLY = process.env.CORRECT_ONLY === '1';  // 1차(gemma 로컬·무료)만 — verify·재교정(sonnet=Claude)은 보류·나중 별도 배치(쿼터 분리)
const VERIFY_MODEL = process.env.VERIFY_MODEL || 'sonnet';  // 검증 모델. haiku 전환 시 Claude 5h burn 급감(verify가 주범 — cache_read 50K/콜×다수). 재교정·1차는 무관(agy·gemma 무료)
const NO_RECORRECT = process.env.NO_RECORRECT === '1';  // 파이프라인은 1차+verify만, 재교정은 별도 러너(recorrect_issues.py)가 agy로 — verify pause/halt와 독립(사용자 지정). agy 더블 방지.
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
  ? (CORRECT_ONLY ? `교정 gemma×${GEMMA_PAR}(로컬26b·무료) — 검증·재교정(Claude) 보류` : `교정 gemma×${GEMMA_PAR}(로컬26b) ∥ 검증 ${PAR_V}(${VERIFY_MODEL}·라인배치+circuit-breaker) ${NO_RECORRECT ? '∥ 재교정=별도러너(agy)' : '∥ 재교정 agy(무료)'}`)
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
let verifyHalt = false; const vWin = []; let vTokEst = 0;  // ★circuit-breaker(parsefail율 급증) + 토큰예산(통제된 양) — 둘 중 하나라도 걸리면 verify 자동중단(1차·재교정은 계속)
const VERIFY_BUDGET = parseInt(process.env.VERIFY_BUDGET || '2500000', 10);  // verify 토큰 예산/run(초과 시 중단, 5h 통제). 라인배치 ~72K/청크
const idle = () => correctQ.length === 0 && cActive === 0 && (CORRECT_ONLY || ((verifyHalt || (verifyQ.length === 0 && vActive === 0)) && recorrectQ.length === 0 && gActive === 0));

// ① 교정 워커(gemma): 미교정 → corrector.mjs(gemma) → 검증큐
async function correctWorker() {
  while (true) {
    if (!correctQ.length) { if (idle()) break; await sleep(300); continue; }
    const slug = correctQ.shift(); const it = items.get(slug); const p = parseSlug(slug);
    cActive++;
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: CORRECT_BACKEND });
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 교정 격리`); }
    else if (r.code === 3) { correctQ.push(slug); await sleep(2000); }   // gemma 빈출력(부하) → 재시도
    else if (CORRECT_ONLY) done++;                                       // 1차만 — verify 보류(corrector_done만, 검증은 나중 별도)
    else verifyQ.push(slug);                                             // 교정 완료 → 검증큐
    cActive--; beat();
  }
}
// ② 검증 워커(sonnet): 같은-라운드 CHUNK개 verify_batch 1콜 → ok 완료 / issues 재교정큐 / 기타 재투입(상한)
async function verifyWorker() {
  while (true) {
    if (verifyHalt) break;   // ★circuit-breaker 발동 → verify 중단(1차·재교정은 계속)
    if (!verifyQ.length) { if (idle()) break; await sleep(300); continue; }
    const r0 = parseSlug(verifyQ[0]).round;
    // ★받는 대로 1건씩 돌리면 배치(CHUNK/콜)가 무의미 → 문제당 ~4배 비쌈. 큐가 CHUNK 미만(트리클)일 때만 대기(쌓아서 배치).
    //   ★백로그(큐≥CHUNK)면 즉시 flush — 헤드라운드가 작아도(다른 라운드가 큐에 많아도) stall 금지(헤드라운드 가용분 최대 CHUNK).
    const noMoreComing = correctQ.length === 0 && cActive === 0 && recorrectQ.length === 0 && gActive === 0;
    if (verifyQ.length < CHUNK && !noMoreComing) { await sleep(500); continue; }
    const chunk = [];
    while (chunk.length < CHUNK && verifyQ.length && parseSlug(verifyQ[0]).round === r0) chunk.push(verifyQ.shift());
    if (!chunk.length) { await sleep(300); continue; }
    vActive++;
    await run('node', ['scripts/verify_batch.mjs', '--list', chunk.join(','), '--chunk', String(CHUNK), '--par', '1', '--force', '--model', VERIFY_MODEL], { RUN_TS: TS });
    for (const slug of chunk) {
      const it = items.get(slug); const st = stateOf(it.md);
      if (st === 'ok') { done++; vWin.push(0); }
      else if (st === 'issues') { if (!NO_RECORRECT) recorrectQ.push(slug); vWin.push(0); }   // NO_RECORRECT: md에 issues 마커만(별도 러너가 agy로 처리)
      else { failed++; vWin.push(1); log(`  ✗ ${slug} parsefail → opus(재시도0)`); }   // ★parsefail 재큐 안 함 = 루프·폭주 차단
    }
    if (VERIFY_MODEL !== 'gemma') {                                                       // ★gemma는 로컬 무료 → 토큰예산 무관(Claude verify 전용). gemma에 적용하면 무료인데도 멋대로 중단됨(버그).
      vTokEst += 72000;                                                                   // 라인배치 ~72K/청크 추정
      if (vTokEst > VERIFY_BUDGET && !verifyHalt) { verifyHalt = true; log(`★verify 토큰예산 ${(VERIFY_BUDGET / 1e6).toFixed(1)}M 도달 — 자동중단(5h 통제). 1차·재교정 계속, 5h 리셋 후 재개.`); }
    }
    if (vWin.length > 40) vWin.splice(0, vWin.length - 40);                                // 슬라이딩 윈도우
    const recent = vWin.slice(-20);
    if (recent.length >= 20 && recent.reduce((a, b) => a + b, 0) / 20 > 0.4) {
      verifyHalt = true;
      log(`★★폭주 차단(circuit-breaker): 최근 20건 parsefail ${Math.round(recent.reduce((a, b) => a + b, 0) / 20 * 100)}% — verify 자동중단. 1차·재교정 계속. 사용자 확인 필요.`);
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
    if (mode === 're' && it.att >= MAXATT) { failed++; log(`  ✗ ${slug} 재교정 상한(${MAXATT}) — issues 잔존 → 오케스트레이터(opus) 손교정 대상`); continue; }
    gActive++;
    const r = await run('node', ['scripts/corrector.mjs', p.round, p.subj, p.num], { CORR_BACKEND: 'agy' });
    if (r.code === 3) { recorrectQ.push(slug); gActive--; await sleep(30000); continue; }  // ★agy 쿼터소진(빈출력) → 시도횟수 안 셈 + 30s 대기 후 agy 재시도(sonnet 폴백 없음 — agy만 지속, 사용자 지정)
    if (mode === 're') it.att++;                                                            // 실제 재교정 시도만 카운트(agy 죽은 건 제외)
    if (stateOf(it.md) === 'quarantine') { failed++; log(`  ⚠ ${slug} 격리(agy) — 오케스트레이터 손교정 대상`); }
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
  ...(CORRECT_ONLY ? [] : [                              // CORRECT_ONLY=1: 1차(gemma)만, verify·재교정(Claude) 보류
    ...(NO_RECORRECT ? [] : [agyLaneWorker()]),          // NO_RECORRECT=1: 재교정 레인 빼고 별도 러너가 처리(agy 더블 방지)
    ...(orOn ? [orLaneWorker()] : []),                   // OR 레인 기본 off(무료풀 429), OR_LANE=1로 켬
    ...Array.from({ length: PAR_V }, verifyWorker),
  ]),
] : [
  ...Array.from({ length: PAR_C }, correctWorker),
  ...Array.from({ length: PAR_V }, verifyWorker),
  ...Array.from({ length: PAR_G }, recorrectWorker),
]);

const fin = { ok: 0, issues: 0, parsefail: 0, quarantine: 0, none: 0 };
for (const [, it] of items) { const s = stateOf(it.md); fin[s] = (fin[s] || 0) + 1; }
log(`══ 완료: 대상 ${total} → ok ${fin.ok} · issues ${fin.issues} · parsefail ${fin.parsefail} · 격리 ${fin.quarantine} · 미처리 ${fin.none} (완료 ${done} · 실패 ${failed})`);
