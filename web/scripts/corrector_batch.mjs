#!/usr/bin/env node
// 전체 문제 교정기 배치. corrector_done 멱등 skip, agy 쿼터(corrector.mjs exit 3) 도달 시 멈춤+보고.
// 사용: node corrector_batch.mjs [round-필터]   (필터 없으면 전체)
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import yaml from 'js-yaml';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = dirname(fileURLToPath(import.meta.url));
const REPO = process.env.MATHSTUDY_ROOT || new URL('../..', import.meta.url).pathname.replace(/\/$/, '');  // ★레포 위치 자동(이동 내성)
const PROB = `${REPO}/docs/problems`;
const FILTER = process.argv[2] || '';

function* walk(d) {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const p = `${d}/${e.name}`;
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.endsWith('.md')) yield p;
  }
}

const probs = [];
let alreadyDone = 0;
for (const md of walk(PROB)) {
  const txt = readFileSync(md, 'utf8');
  if (/^corrector_done:\s*true/m.test(txt) || /^corrector_quarantine:\s*true/m.test(txt)) { alreadyDone++; continue; }  // 멱등·격리 skip(반복 방지)
  const base = md.split('/').pop().replace(/\.md$/, '');
  const mm = base.match(/^(.+)_([가-힣A-Za-z]+)_(\d+)$/);  // {round}_{subj}_{num}
  if (!mm) continue;
  if (FILTER && !mm[1].includes(FILTER)) continue;
  probs.push({ round: mm[1], subj: mm[2], num: mm[3] });
}
console.log(`대상 ${probs.length}문제 (이미 corrector_done ${alreadyDone}개 skip)${FILTER ? ` · 필터:${FILTER}` : ''}`);

// B 빌드 체크: YAML 전수 파싱 → 깨진 수. corrector.mjs validate가 1차 방어, 이건 누적 안전망(서버 다운 차단).
function buildCheck() {
  let bad = 0;
  for (const md of walk(PROB)) {
    const t = readFileSync(md, 'utf8'); if (!t.startsWith('---')) continue;
    const i = t.indexOf('\n---', 3); if (i < 0) continue;
    try { yaml.load(t.slice(3, i)); } catch { bad++; }
  }
  return bad;
}
const CONC = +(process.env.CORR_CONC || 6);  // 동시 워커(쿼터 총량 불변·속도↑)
let idx = 0, done = 0, fail = 0, quota = false;
async function worker() {
  while (!quota) {
    const i = idx++; if (i >= probs.length) break;
    const p = probs[i]; const tag = `${p.round}/${p.subj}_${p.num}`;
    const code = await new Promise((res) => {
      const c = spawn('node', [`${DIR}/corrector.mjs`, p.round, p.subj, p.num], { stdio: 'ignore' });
      c.on('close', res);
    });
    if (code === 3) { quota = true; console.log(`${tag}: ⛔ agy 쿼터 도달 — 멈춤`); break; }
    if (code === 0) done++; else fail++;
    if ((done + fail) % 5 === 0 || code !== 0) console.log(`[${done + fail}/${probs.length}] ${tag}: ${code === 0 ? '✓' : '✗(' + code + ')'}`);
    if (done > 0 && done % 100 === 0) {  // B 빌드체크: 100개마다 YAML 전수
      const bad = buildCheck();
      if (bad) { quota = true; console.log(`⛔ 빌드체크 실패: YAML 깨진 ${bad}개 — 즉시 멈춤(서버 다운 방지)`); break; }
      console.log(`✓ 빌드체크 OK (${done}개째 · YAML 0 깨짐)`);
    }
  }
}
console.log(`동시성 ${CONC} 워커 시작`);
await Promise.all(Array.from({ length: CONC }, () => worker()));
const ql = '/tmp/ingest_logs/corrector_quarantine.log';
const quar = existsSync(ql) ? readFileSync(ql, 'utf8').split('\n').filter(Boolean).length : 0;
console.log(`\n=== 배치 종료 ===\n교정 ${done} · 실패 ${fail} · 격리누적 ${quar} · 쿼터중단:${quota} · 남은대상 ${probs.length - done - fail}`);
