#!/usr/bin/env node
// 위젯 spec 자율 워커풀 (블루프린트 §3-4). 큐(함수/도형 정의) → 생성→수학게이트→재시도→영속/스킵.
//   생성=widget_generate(Opus). 검증=widget_validate.validate(이중유도/불변식, import). 멱등(repo에 있으면 스킵).
//   재시도=re-roll 최대 3회(생성 stochastic). accept=web/src/data/concept-widgets/<id>.json 영속. 실패=needs-manual 로그.
//   ※렌더게이트(/dev/interactive-test)는 후속. 현재 수학게이트(린치핀)만 — 좌표 finite·불변식·오라클.
// 사용: node web/scripts/widget_spec_loop.mjs [--n 15]
import { spawn, execSync } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, appendFileSync, copyFileSync, rmSync } from 'node:fs';
import { validate } from './widget_validate.mjs';
import { fileURLToPath } from 'node:url';
// ★REPO 는 이 스크립트 자기 위치 기준(web/scripts/.. 의 부모)으로 도출 — 하드코딩 절대경로는
//   레포 위치가 머신마다 다르면(laptop ~/Projects/math-study, tme ~/math-study) 깨진다.
const REPO = fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const CDIR = `${REPO}/docs/concepts`, TMP = '/tmp/widget_specs', OUT = `${REPO}/web/src/data/concept-widgets`, LOGDIR = '/tmp/ingest_logs';
for (const d of [TMP, OUT, LOGDIR]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const A = process.argv.slice(2);
// ★생성기·도메인·동시성은 교체 가능해야 한다: Opus(claude -p) ↔ Nous(HTTP) 비교, 도메인 확장(확률통계 등),
//   HTTP 생성기는 프로세스 스폰이 없어 동시성을 더 올릴 수 있다(claude -p 는 2가 한계였음).
const GEN = process.env.WIDGET_GEN || 'widget_generate.mjs';
//   WIDGET_DOMAINS='*' = 도메인 무관 전체(미분류 domain 빈값 노드까지 포함).
const DOMAINS = (process.env.WIDGET_DOMAINS || '함수,도형').split(',').map((s) => s.trim()).filter(Boolean);
const ALL_DOMAINS = DOMAINS.includes('*');
const N = parseInt((A[A.indexOf('--n') + 1]) || '15', 10), PAR = +(process.env.WIDGET_PAR || 2), MAXTRY = 3;
const PRIORITY = A.includes('--priority'), COMMIT = A.includes('--commit');
const LOG = `${LOGDIR}/widget_loop_${Math.floor(Date.now() / 1000)}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };
const safe = (id) => id.replace(/\//g, '__');

function walk(dir) { const o = []; for (const e of readdirSync(dir, { withFileTypes: true })) { const p = `${dir}/${e.name}`; if (e.isDirectory()) o.push(...walk(p)); else if (e.name.endsWith('.md')) o.push(p); } return o; }
function meta(p) { const raw = readFileSync(p, 'utf8'); const fm = raw.match(/^---\n([\s\S]*?)\n---/); if (!fm) return null; const d = (fm[1].match(/^domain:\s*(.+)$/m) || [])[1]?.trim(); const t = (fm[1].match(/^concept_type:\s*(.+)$/m) || [])[1]?.trim(); return { id: p.replace(`${CDIR}/`, '').replace(/\.md$/, ''), domain: d, type: t }; }

const done = new Set(readdirSync(OUT).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', '')));
const cands = walk(CDIR).map(meta).filter((c) => c && c.type === 'definition' && (ALL_DOMAINS || DOMAINS.includes(c.domain)) && !done.has(safe(c.id)));
// 수능 단원 중요도(고가치 우선): 미적분 > 수1/2·선택 > 고1 > 중3 > 중2 > 중1
const lvl = (id) => /\/calculus\//.test(id) ? 7 : /\/(math-[12]|geometry-elective|prob-stats-elective|electives?)\//.test(id) ? 6 : /\/high-1\//.test(id) ? 5 : /\/middle-3\//.test(id) ? 3 : /\/middle-2\//.test(id) ? 2 : /\/middle-1\//.test(id) ? 1 : 4;
let queue;
if (PRIORITY) { cands.sort((a, b) => lvl(b.id) - lvl(a.id) || a.id.localeCompare(b.id)); queue = cands.slice(0, N); }
else { const stepN = Math.max(1, Math.floor(cands.length / N)); queue = cands.filter((_, i) => i % stepN === 0).slice(0, N); }
log(`══ 워커풀${PRIORITY ? '(고가치순)' : ''}: 미처리후보 ${cands.length}, 이번 큐 ${queue.length}, par ${PAR}, maxtry ${MAXTRY} · gen ${GEN} · domains ${ALL_DOMAINS ? '전체' : DOMAINS.join('/')} · LOG ${LOG}`);
// ★LLM 모니터(llm_monitor_server) 리셋 신호 — 전체 큐 크기를 알려야 진행률이 맞는다.
//   생성기는 건별 호출이라 자기 total 을 1 로밖에 못 말한다.
try {
  const MON = `${REPO}/.llm-monitor`; if (!existsSync(MON)) mkdirSync(MON, { recursive: true });
  appendFileSync(`${MON}/events.ndjson`, JSON.stringify({ t: Date.now(), ev: 'run', total: queue.length, model: `${GEN}${process.env.NOUS_MODEL ? ' · ' + process.env.NOUS_MODEL : ''}`, par: PAR }) + '\n');
} catch { /* 모니터는 best-effort */ }

// 자식 stdout 캡처 → widget_generate 가 찍는 `cr=N`(cache_read_input_tokens)을 로그에 남겨 프롬프트
// 캐시 히트 추적 가능하게(이전엔 stdout='ignore'라 캐시 실측이 버려졌음). 연속 호출서 cr 상승=캐시 생존.
const crVals = [];   // 캐시 히트 추적용 — genOnce 가 수집, 종료 시 다이제스트로 cron-runs.md 에 누적.
const ccVals = [];   // cache_creation(쓰기) 추적 — net 절감(쓰기 프리미엄) 정확 계산용.
// prevFail: 직전 시도의 검증 실패 사유. 생성기가 프롬프트에 실어 "그 지점만 고쳐" 재생성한다(repair).
// 이걸 안 넘기면 완전히 같은 입력으로 주사위만 다시 굴리게 되고, 실패 대부분이 기계적 오류
// (mathjs API 오인·오라클 정밀도)라 같은 실패를 3번 반복하고 끝난다.
const genOnce = (id, prevFail) => new Promise((res) => {
  const args = [`${REPO}/web/scripts/${GEN}`, id];
  if (prevFail) args.push('--prev-fail', prevFail);
  const c = spawn('node', args, { stdio: ['ignore', 'pipe', 'ignore'], timeout: 600000 });
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

// ── 오라클 무결성 (A·B·C) ────────────────────────────────────────────────────────
// 오라클 불일치는 "spec 계산값 ≠ 손계산값"일 뿐 **어느 쪽이 틀렸는지 말해주지 않는다**.
//   ① spec 틀림 → 정상 기각  ② 오라클 틀림 → 멀쩡한 위젯을 버림  ③ 둘 다 같이 틀림 → 조용히 통과
// 순진하게 실패 문자열을 그대로 되먹이면 모델이 **공식 대신 정답(expect)을 계산값으로 복사**해
// 통과시킨다 = 시험지를 고쳐 합격하는 것 = ②를 고치는 대신 ③을 제조한다. 그래서:
//   A. 계산값을 가린다(복사할 숫자를 안 준다)
//   B. 다른 검사 통과 여부를 알려준다(불변식은 손계산과 무관한 독립 검증 — 이게 다 통과했으면
//      spec 이 맞고 손계산이 틀렸을 공산이 크다는 근거가 된다)
//   C. 공식을 안 고치고 정답만 바꾼 시도를 결정적으로 기각한다
const kindOf = (f) => f.startsWith('오라클') ? 'oracle' : f.startsWith('불변식') ? 'invariant'
  : f.startsWith('scope') ? 'scope' : f.startsWith('readout') ? 'readout' : f.startsWith('shape') ? 'shape' : 'etc';

// A: "오라클 v=0.63078 ≠ 0.63095 @{...}" → "오라클 불일치: v @{...}" (계산값·기대값 모두 제거)
const maskOracle = (f) => f.replace(/^오라클\s+(\S+)=.*?\s+≠\s+.*?\s+@(.*)$/, '오라클 불일치: $1 @$2');

function buildHint(fails, recipe) {
  const kinds = fails.map(kindOf);
  const uniq = [...new Set(fails.map(maskOracle))].slice(0, 4);
  const lines = uniq.map((f) => '- ' + f);
  const nInv = (recipe?.invariants || []).length;
  // B: 판단 근거 제공
  if (kinds.includes('oracle') && !kinds.includes('invariant') && nInv > 0) {
    lines.push(`- (참고) 불변식 ${nInv}개는 전부 통과했다. 불변식은 손계산과 무관한 독립 검증이므로, **spec 공식이 맞고 oracle 의 손계산이 틀렸을 가능성이 높다** — 그 파라미터에서 값을 처음부터 다시 유도해 보라. 무리수라 1e-6 을 못 맞추겠으면 **정수·유리수로 딱 떨어지는 파라미터로 oracle 을 교체**하라.`);
  } else if (kinds.includes('oracle') && kinds.includes('invariant')) {
    lines.push('- (참고) 불변식도 함께 깨졌다. oracle 이 아니라 **spec 의 공식 자체가 틀렸을 가능성이 높다.**');
  }
  return lines.join('\n');
}

// C: 공식(params+scope)이 그대로인데 oracle 만 바뀌었으면 = 답만 고친 것
const formulaKey = (o) => JSON.stringify([(o.spec?.params || []).map((p) => [p.name, p.min, p.max, p.init, p.step]), (o.spec?.scope || '').replace(/\s+/g, ' ').trim()]);
const oracleKey = (o) => JSON.stringify(o.recipe?.oracle || []);

let accepted = 0, skipped = 0, qi = 0, goalpost = 0;
async function worker() {
  while (qi < queue.length) {
    const { id } = queue[qi++]; const sf = `${TMP}/${safe(id)}.json`;
    let ok = false, lastFail = '', prev = null;
    for (let t = 1; t <= MAXTRY && !ok; t++) {
      if (t > 1 && lastFail) log(`  ↻ ${id} 재시도 ${t}/${MAXTRY} — 되먹임: ${lastFail.replace(/\n/g, ' ').slice(0, 100)}`);
      // ★생성 전 잔여 spec 제거: 안 지우면 생성 실패 시 **이전 실행(다른 모델·프롬프트일 수도)의 산출물**이
      //   그대로 검증·수락된다. 실제로 --par 버그 때 그 경로로 13건이 안착했다.
      try { if (existsSync(sf)) rmSync(sf); } catch { /* 지우기 실패는 무시(어차피 아래서 재검증) */ }
      await genOnce(id, t > 1 ? lastFail : '');
      if (!existsSync(sf)) { lastFail = '- 직전 시도는 출력이 없었다(토큰 예산 절단 의심). 더 짧고 단순한 spec 으로 만들어라.'; continue; }
      let o;
      try { o = JSON.parse(readFileSync(sf, 'utf8')); } catch (e) { lastFail = '- 직전 출력이 JSON 파싱 실패: ' + e.message; continue; }
      // C: 골대 옮기기 탐지 — 공식은 그대로 두고 정답만 갈아끼운 시도는 기각한다.
      if (prev && formulaKey(prev) === formulaKey(o) && oracleKey(prev) !== oracleKey(o)) {
        goalpost++;
        log(`  ⚠ ${id} 골대이동 기각 — params·scope 동일한데 oracle 만 변경`);
        lastFail = '- **금지된 수정을 했다: 공식(params·scope)은 그대로 두고 oracle 의 정답만 계산값에 맞춰 바꿨다.** oracle 은 spec 을 검증하는 독립 기준이지 spec 의 출력이 아니다. 공식이 맞다고 확신하면 oracle 을 **처음부터 다시 손으로 유도**하고(값 베끼기 금지), 아니면 공식을 고쳐라.';
        prev = o; continue;
      }
      prev = o;
      try {
        const r = validate(o.spec, o.recipe);
        if (r.ok) ok = true; else lastFail = buildHint(r.fails, o.recipe);
      } catch (e) { lastFail = '- 검증기 예외: ' + e.message; }
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
  log(`══ 종료: accept ${accepted} · skip ${skipped} · 골대이동기각 ${goalpost} · 영속 ${OUT} · 합격률 ${rate}%`);
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
