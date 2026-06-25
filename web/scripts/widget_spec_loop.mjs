#!/usr/bin/env node
// 위젯 spec 자율 워커풀 (블루프린트 §3-4). 큐(함수/도형 정의) → 생성→수학게이트→재시도→영속/스킵.
//   생성=widget_generate(Opus). 검증=widget_validate.validate(이중유도/불변식, import). 멱등(repo에 있으면 스킵).
//   재시도=re-roll 최대 3회(생성 stochastic). accept=web/src/data/concept-widgets/<id>.json 영속. 실패=needs-manual 로그.
//   ※렌더게이트(/dev/interactive-test)는 후속. 현재 수학게이트(린치핀)만 — 좌표 finite·불변식·오라클.
// 사용: node web/scripts/widget_spec_loop.mjs [--n 15]
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, appendFileSync, copyFileSync } from 'node:fs';
import { validate } from './widget_validate.mjs';
const REPO = '/home/insung/Projects/math-study';
const CDIR = `${REPO}/docs/concepts`, TMP = '/tmp/widget_specs', OUT = `${REPO}/web/src/data/concept-widgets`, LOGDIR = '/tmp/ingest_logs';
for (const d of [TMP, OUT, LOGDIR]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const A = process.argv.slice(2);
const N = parseInt((A[A.indexOf('--n') + 1]) || '15', 10), PAR = 2, MAXTRY = 3;
const LOG = `${LOGDIR}/widget_loop_${Math.floor(Date.now() / 1000)}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };
const safe = (id) => id.replace(/\//g, '__');

function walk(dir) { const o = []; for (const e of readdirSync(dir, { withFileTypes: true })) { const p = `${dir}/${e.name}`; if (e.isDirectory()) o.push(...walk(p)); else if (e.name.endsWith('.md')) o.push(p); } return o; }
function meta(p) { const raw = readFileSync(p, 'utf8'); const fm = raw.match(/^---\n([\s\S]*?)\n---/); if (!fm) return null; const d = (fm[1].match(/^domain:\s*(.+)$/m) || [])[1]?.trim(); const t = (fm[1].match(/^concept_type:\s*(.+)$/m) || [])[1]?.trim(); return { id: p.replace(`${CDIR}/`, '').replace(/\.md$/, ''), domain: d, type: t }; }

const done = new Set(readdirSync(OUT).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', '')));
const cands = walk(CDIR).map(meta).filter((c) => c && c.type === 'definition' && (c.domain === '함수' || c.domain === '도형') && !done.has(safe(c.id)));
const stepN = Math.max(1, Math.floor(cands.length / N));
const queue = cands.filter((_, i) => i % stepN === 0).slice(0, N);
log(`══ 워커풀: 미처리후보 ${cands.length}, 이번 큐 ${queue.length}, par ${PAR}, maxtry ${MAXTRY} · LOG ${LOG}`);

const genOnce = (id) => new Promise((res) => { const c = spawn('node', [`${REPO}/web/scripts/widget_generate.mjs`, id], { stdio: ['ignore', 'ignore', 'ignore'], timeout: 240000 }); c.on('close', res); c.on('error', res); });

let accepted = 0, skipped = 0, qi = 0;
async function worker() {
  while (qi < queue.length) {
    const { id } = queue[qi++]; const sf = `${TMP}/${safe(id)}.json`;
    let ok = false, lastFail = '';
    for (let t = 1; t <= MAXTRY && !ok; t++) {
      await genOnce(id);
      if (!existsSync(sf)) { lastFail = '생성출력 없음'; continue; }
      try { const o = JSON.parse(readFileSync(sf, 'utf8')); const r = validate(o.spec, o.recipe); if (r.ok) ok = true; else lastFail = r.fails[0] || '검증 실패'; } catch (e) { lastFail = '파싱: ' + e.message; }
    }
    if (ok) { copyFileSync(sf, `${OUT}/${safe(id)}.json`); accepted++; log(`✓ ${id} accept (누적 ${accepted})`); }
    else { appendFileSync(`${TMP}/needs-manual.txt`, `${id}\t${lastFail}\n`); skipped++; log(`✗ ${id} skip-manual: ${lastFail.slice(0, 70)}`); }
  }
}
(async () => {
  await Promise.all(Array.from({ length: PAR }, worker));
  log(`══ 종료: accept ${accepted} · skip ${skipped} · 영속 ${OUT} · 합격률 ${queue.length ? Math.round(accepted / queue.length * 100) : 0}%`);
})();
