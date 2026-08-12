#!/usr/bin/env node
// 위젯 spec 자율 워커풀 (블루프린트 §3-4). 큐(함수/도형 정의) → 생성→수학게이트→재시도→영속/스킵.
//   생성=widget_generate(Opus). 검증=widget_validate.validate(이중유도/불변식, import). 멱등(repo에 있으면 스킵).
//   재시도=re-roll 최대 3회(생성 stochastic). accept=web/src/data/concept-widgets/<id>.json 영속. 실패=needs-manual 로그.
//   ※렌더게이트(/dev/interactive-test)는 후속. 현재 수학게이트(린치핀)만 — 좌표 finite·불변식·오라클.
// 사용: node web/scripts/widget_spec_loop.mjs [--n 15]
import { spawn, execSync } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, appendFileSync, copyFileSync } from 'node:fs';
import { validate } from './widget_validate.mjs';
import { fileURLToPath } from 'node:url';
// ★REPO 는 이 스크립트 자기 위치 기준(web/scripts/.. 의 부모)으로 도출 — 하드코딩 절대경로는
//   레포 위치가 머신마다 다르면(laptop ~/Projects/math-study, tme ~/math-study) 깨진다.
const REPO = fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const CDIR = `${REPO}/docs/concepts`, TMP = '/tmp/widget_specs', OUT = `${REPO}/web/src/data/concept-widgets`, LOGDIR = '/tmp/ingest_logs';
for (const d of [TMP, OUT, LOGDIR]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const A = process.argv.slice(2);
const N = parseInt((A[A.indexOf('--n') + 1]) || '15', 10), PAR = 2, MAXTRY = 3;
const PRIORITY = A.includes('--priority'), COMMIT = A.includes('--commit');
const LOG = `${LOGDIR}/widget_loop_${Math.floor(Date.now() / 1000)}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };
const safe = (id) => id.replace(/\//g, '__');

function walk(dir) { const o = []; for (const e of readdirSync(dir, { withFileTypes: true })) { const p = `${dir}/${e.name}`; if (e.isDirectory()) o.push(...walk(p)); else if (e.name.endsWith('.md')) o.push(p); } return o; }
function meta(p) { const raw = readFileSync(p, 'utf8'); const fm = raw.match(/^---\n([\s\S]*?)\n---/); if (!fm) return null; const d = (fm[1].match(/^domain:\s*(.+)$/m) || [])[1]?.trim(); const t = (fm[1].match(/^concept_type:\s*(.+)$/m) || [])[1]?.trim(); return { id: p.replace(`${CDIR}/`, '').replace(/\.md$/, ''), domain: d, type: t }; }

const done = new Set(readdirSync(OUT).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', '')));
const cands = walk(CDIR).map(meta).filter((c) => c && c.type === 'definition' && (c.domain === '함수' || c.domain === '도형') && !done.has(safe(c.id)));
// 수능 단원 중요도(고가치 우선): 미적분 > 수1/2·선택 > 고1 > 중3 > 중2 > 중1
const lvl = (id) => /\/calculus\//.test(id) ? 7 : /\/(math-[12]|geometry-elective|prob-stats-elective|electives?)\//.test(id) ? 6 : /\/high-1\//.test(id) ? 5 : /\/middle-3\//.test(id) ? 3 : /\/middle-2\//.test(id) ? 2 : /\/middle-1\//.test(id) ? 1 : 4;
let queue;
if (PRIORITY) { cands.sort((a, b) => lvl(b.id) - lvl(a.id) || a.id.localeCompare(b.id)); queue = cands.slice(0, N); }
else { const stepN = Math.max(1, Math.floor(cands.length / N)); queue = cands.filter((_, i) => i % stepN === 0).slice(0, N); }
log(`══ 워커풀${PRIORITY ? '(고가치순)' : ''}: 미처리후보 ${cands.length}, 이번 큐 ${queue.length}, par ${PAR}, maxtry ${MAXTRY} · LOG ${LOG}`);

// 자식 stdout 캡처 → widget_generate 가 찍는 `cr=N`(cache_read_input_tokens)을 로그에 남겨 프롬프트
// 캐시 히트 추적 가능하게(이전엔 stdout='ignore'라 캐시 실측이 버려졌음). 연속 호출서 cr 상승=캐시 생존.
const crVals = [];   // 캐시 히트 추적용 — genOnce 가 수집, 종료 시 다이제스트로 cron-runs.md 에 누적.
const ccVals = [];   // cache_creation(쓰기) 추적 — net 절감(쓰기 프리미엄) 정확 계산용.
const genOnce = (id) => new Promise((res) => {
  const c = spawn('node', [`${REPO}/web/scripts/widget_generate.mjs`, id], { stdio: ['ignore', 'pipe', 'ignore'], timeout: 240000 });
  let out = '';
  c.stdout.on('data', (d) => { out += d; });
  c.on('close', (code) => {
    const m = out.match(/cr=(\d+)/);
    const mc = out.match(/cc=(\d+)/);
    if (m) { crVals.push(+m[1]); if (mc) ccVals.push(+mc[1]); log(`  ${id} cache_read=${m[1]} cache_creation=${mc ? mc[1] : '?'}`); }
    res(code);
  });
  c.on('error', res);
});

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
    if (ok) {
      // 안전망: plot이 있는데 geometry가 곡선 없이 점·선분뿐이면 중복·혼란 → 제거(plot만 영속)
      const o = JSON.parse(readFileSync(sf, 'utf8')); const g = o.spec?.geometry, p = o.spec?.plot; let strip = '';
      if (p?.fns?.length && g?.shapes?.length && g.shapes.every((x) => !/circle|polygon|curve|parametric|path|arc|angle/.test(x.type || ''))) { delete o.spec.geometry; strip = ' [중복 geometry 제거]'; }
      writeFileSync(`${OUT}/${safe(id)}.json`, JSON.stringify(o, null, 1));
      accepted++; log(`✓ ${id} accept (누적 ${accepted})${strip}`);
    }
    else { appendFileSync(`${TMP}/needs-manual.txt`, `${id}\t${lastFail}\n`); skipped++; log(`✗ ${id} skip-manual: ${lastFail.slice(0, 70)}`); }
  }
}
(async () => {
  await Promise.all(Array.from({ length: PAR }, worker));
  const rate = queue.length ? Math.round(accepted / queue.length * 100) : 0;
  log(`══ 종료: accept ${accepted} · skip ${skipped} · 영속 ${OUT} · 합격률 ${rate}%`);
  // ★실행 다이제스트를 레포 추적 문서에 누적(00_STATUS 인덱스로 traverse). /tmp 로그는 휘발성이라.
  //   cache=cr 평균/최대(연속 호출서 상승=프롬프트 캐시 생존). 캐시 셋업 검증은 cron-runs.md 참조.
  try {
    const ts = new Date(Date.now() + 9 * 3600 * 1000).toISOString().replace('T', ' ').slice(0, 16); // KST
    const sum = (a) => a.reduce((x, y) => x + y, 0);
    // ★API환산 net 절감(widget=opus 4.8, 입력 $5/1M): cache_read=0.1×·write(5m)=1.25× → cr×0.9×p − cc×0.25×p.
    const P_IN = 5.0;
    const saveUsd = (sum(crVals) * 0.9 * P_IN - sum(ccVals) * 0.25 * P_IN) / 1e6;
    const crStr = crVals.length ? `cr avg ${Math.round(sum(crVals) / crVals.length)} · max ${Math.max(...crVals)} · Σcr ${sum(crVals)} · Σcc ${sum(ccVals)} · save≈$${saveUsd.toFixed(2)} (n=${crVals.length})` : 'cr 없음';
    appendFileSync(`${REPO}/docs/ops/status/cron-runs.md`, `| ${ts} | widget | accept ${accepted} · skip ${skipped} · ${rate}% | ${crStr} |\n`);
  } catch (e) { log(`다이제스트 기록 실패: ${String(e.message).slice(0, 80)}`); }
  // ★커밋 게이트는 accepted 가 아니라 "워킹트리가 더러운가"로 판단한다.
  //   예전엔 `accepted > 0` 이라 큐가 마르면(고가치 후보 소진, 2026-07-07~) 커밋이 영영 안 걸렸고,
  //   그동안 무조건 append 되는 다이제스트(cron-runs.md)와 그림 크론 산출물(concept-illustrations.json,
  //   gen_daily_illustration.mjs 는 자체 커밋이 없다)이 미커밋으로 37일치 쌓였다. 3시 크론이 데이터 스위퍼 역할.
  const DATA_PATHS = [
    'web/src/data/concept-widgets/',
    'web/src/data/concept-widgets-index.json',
    'web/src/data/concept-illustrations.json',
    'docs/ops/status/cron-runs.md',
  ];
  if (COMMIT) {
    if (accepted > 0) { try { execSync('node web/scripts/gen_widget_index.mjs', { cwd: REPO, stdio: 'pipe' }); } catch { /* 인덱스(SSOT) 재생성 best-effort */ } }
    let dirty = false;
    try { execSync(`git add -- ${DATA_PATHS.join(' ')}`, { cwd: REPO, stdio: 'pipe' }); dirty = execSync(`git diff --cached --name-only -- ${DATA_PATHS.join(' ')}`, { cwd: REPO, encoding: 'utf8' }).trim().length > 0; }
    catch (e) { log(`스테이징 실패: ${String(e.message).slice(0, 120)}`); }
    if (!dirty) log('커밋할 데이터 변경 없음 — 스킵');
    else try {
      const msg = accepted > 0
        ? `data(widget): 일일 고가치 위젯 ${accepted}건 자동생성·검증 + 인덱스 갱신 + 크론 다이제스트`
        : 'data(cron): 일일 그림 캐시 + 크론 다이제스트 갱신';
      execSync(`git commit -q -m "${msg}"`, { cwd: REPO, stdio: 'pipe' }); log(`커밋 완료 (+${accepted})`);
      // ★컨테이너는 root 로 도는데 여기서 만들어지는 .git 산물(objects/ 팬아웃 디렉터리 755,
      //   COMMIT_EDITMSG 644)이 전부 root:root 로 남는다. 그러면 **호스트 사용자의 git 이
      //   "insufficient permission for adding an object" / "Permission denied" 로 통째 막힌다**
      //   (실제로 704개가 쌓여 막혀 있었음). 레포 루트 소유자로 되돌린다 — .git 은 857엔트리라 저렴.
      //   root 가 아니면 chown 이 실패하는데, 그 경우엔 애초에 오염이 없다(|| true).
      try { execSync('chown -R --reference=. .git 2>/dev/null || true', { cwd: REPO, stdio: 'pipe', shell: '/bin/sh' }); } catch { /* best-effort */ }
    }
    catch (e) { log(`커밋 실패: ${String(e.message).slice(0, 120)}`); }
    // --no-verify: 데이터(json)만 커밋이라 pre-push 타입체크 불필요 + 3am astro check가 dev 서버 dep 캐시 stale 시키는 footgun 회피
    // (컨테이너엔 SSH 키가 없어 대개 실패 → 크론이 호스트에서 다시 push 한다. 커밋 없을 땐 시도조차 안 함.)
    if (dirty) {
      try { execSync('git push -q --no-verify', { cwd: REPO, stdio: 'pipe' }); log('푸시 완료'); }
      catch (e) { log(`푸시 실패(로컬 커밋 유지): ${String(e.message).slice(0, 80)}`); }
    }
  }
})();
