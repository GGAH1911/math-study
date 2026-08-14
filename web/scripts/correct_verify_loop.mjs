#!/usr/bin/env node
// 교정→검증→재교정 루프 드라이버.
//   대상 = corrector_done:true 인데 corrector_verify != ok 인 문제(이미 교정됐으나 sonnet 미검증).
//   ① verify_batch(sonnet, 1콜N) 로 검증 → ② corrector_verify:issues 면 corrector.mjs(gemma) 재교정
//   → ③ 재검증(verify_batch --force) → issues 없을 때까지 루프(최대 MAXROUND). 전부 직렬(usage-pressure 최소).
// 사용: node correct_verify_loop.mjs [round-필터]   (예: 2019, 2020/9월모평; 없으면 전체 corrected-unverified)
//   env: MAXROUND(기본3) · CORR_BACKEND(재교정 백엔드, 기본 gemma) · RUN_TS(로그 타임스탬프)
import { readdirSync, readFileSync, existsSync, appendFileSync, mkdirSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const REPO = process.env.MATHSTUDY_ROOT || new URL('../..', import.meta.url).pathname.replace(/\/$/, '');  // ★레포 위치 자동(이동 내성)
const PROB = `${REPO}/docs/problems`;
const FILTER = process.argv[2] || '';
const MAXROUND = parseInt(process.env.MAXROUND || '3', 10);
const CORR_BACKEND = process.env.CORR_BACKEND || 'gemma';
const LOGDIR = '/tmp/ingest_logs';
if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const TS = process.env.RUN_TS || String(Math.floor(Date.now() / 1000));
const LOG = `${LOGDIR}/corrverify_${TS}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };

function* walk(d) {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const p = `${d}/${e.name}`;
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.endsWith('.md')) yield p;
  }
}
const slugOf = (md) => md.split('/').pop().replace(/\.md$/, '');
function fmVerify(md) { const m = readFileSync(md, 'utf8').match(/\ncorrector_verify:\s*(.*)/); return m ? m[1].trim() : null; }
function isDone(md) { return /^corrector_done:\s*true/m.test(readFileSync(md, 'utf8')); }

// 대상 = corrector_done & verify!=ok (필터 적용)
function targets() {
  const out = [];
  for (const md of walk(PROB)) {
    const slug = slugOf(md);
    const mm = slug.match(/^(.+)_([가-힣A-Za-z]+)_(\d+)$/);
    if (!mm) continue;
    if (FILTER && !mm[1].includes(FILTER)) continue;
    if (!isDone(md)) continue;
    if (fmVerify(md) === 'ok') continue;
    out.push({ slug, round: mm[1], subj: mm[2], num: mm[3], md });
  }
  return out.sort((a, b) => a.slug.localeCompare(b.slug));
}

function runNode(args, env = {}) {
  const r = spawnSync('node', args, { cwd: `${REPO}/web`, env: { ...process.env, ...env }, stdio: 'inherit', encoding: 'utf8' });
  return r.status;
}

const t0 = targets();
log(`══ correct_verify_loop 시작: 대상 ${t0.length}문제${FILTER ? ` (필터:${FILTER})` : ''} · MAXROUND ${MAXROUND} · 재교정=${CORR_BACKEND} · LOG ${LOG}`);
if (!t0.length) { log('대상 0 — 종료'); process.exit(0); }

// ① 1차 검증 (전체 대상, verify_batch 가 round별 청크·직렬)
log(`① 검증(sonnet) 시작 — ${t0.length}문제`);
runNode(['scripts/verify_batch.mjs', '--list', t0.map((x) => x.slug).join(','), '--chunk', '5'], { RUN_TS: TS });

// ②③ 재교정 루프
for (let round = 1; round <= MAXROUND; round++) {
  const bad = targets().filter((x) => fmVerify(x.md) === 'issues');
  log(`── 루프 ${round}/${MAXROUND}: issues ${bad.length}개`);
  if (!bad.length) { log('issues 0 — 루프 종료'); break; }
  for (const b of bad) {
    log(`  재교정(${CORR_BACKEND}) ${b.slug}`);
    runNode(['scripts/corrector.mjs', b.round, b.subj, b.num], { CORR_BACKEND });
  }
  log(`  재검증 ${bad.length}개`);
  runNode(['scripts/verify_batch.mjs', '--list', bad.map((x) => x.slug).join(','), '--chunk', '5', '--force'], { RUN_TS: TS });
}

const fin = targets();
const ok = fin.filter((x) => fmVerify(x.md) === 'ok').length;
const iss = fin.filter((x) => fmVerify(x.md) === 'issues').length;
const pf = fin.filter((x) => fmVerify(x.md) === 'parsefail').length;
log(`══ 완료: 대상 ${t0.length} → 남은 미검증 ${fin.length} (issues ${iss} · parsefail ${pf}) · 이번 실행 ok 전환분 포함 ok누계 확인은 분포로`);
log(`   (ok=${t0.length - fin.length} 전환 / 잔여 ${fin.length})`);
