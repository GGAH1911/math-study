#!/usr/bin/env node
// 검증 배치 — sonnet 1콜에 N문제를 묶어 검증(★병렬 아님). 호출 수 1/N → usage-pressure↓ +
//   claude -p 의 cache_read 오버헤드(~50K/콜)가 N문제에 분산 → 문제당 비용↓.
//   실측: 1콜 5문제 = 문제당 $0.044 (1콜 1문제 $0.19 의 4.3배 절약), 정확도 유지(figure 위치오류도 탐지).
//   교정된 searchable_text 를 이미지와 대조해 놓침/환각을 잡고 corrector_verify(ok/issues/parsefail) 갱신.
// 멱등: corrector_verify:ok 는 skip (--force 무시). 로그: /tmp/ingest_logs/verify_batch_<ts>.log (append).
// 사용: node verify_batch.mjs --list slug1,slug2  |  --round 2021_수능 [--subj 나형]  [--chunk 5] [--force] [--model sonnet]
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, existsSync, readdirSync, mkdirSync } from 'node:fs';

const REPO = '/home/insung/Projects/math-study';
const LOGDIR = '/tmp/ingest_logs';
const A = process.argv.slice(2);
const getOpt = (k, d = null) => { const i = A.indexOf(k); return i >= 0 && A[i + 1] ? A[i + 1] : d; };
const has = (k) => A.includes(k);
const CHUNK = parseInt(getOpt('--chunk', '5'), 10);            // 1콜당 문제 수 (실측 sweet spot 5)
const PAR = Math.max(1, parseInt(getOpt('--par', process.env.VERIFY_PAR || '1'), 10)); // 동시 청크 수(sonnet 병렬콜)
const MODEL = getOpt('--model', process.env.VERIFY_MODEL || 'sonnet');
const FORCE = has('--force');

if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const TS = process.env.RUN_TS || String(Math.floor(Date.now() / 1000));
const LOG = `${LOGDIR}/verify_batch_${TS}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };

function parseSlug(slug) { const m = slug.match(/^(.+)_([^_]+)_(\d+)$/); return m ? { slug, round: m[1], subj: m[2], num: m[3] } : null; }
function findMd(round, subj, num) {
  const base = `${REPO}/docs/problems/${round.split('_')[0]}`;
  if (!existsSync(base)) return null;
  const n2 = String(num).padStart(2, '0');
  for (const sub of readdirSync(base)) for (const nm of [`${round}_${subj}_${n2}.md`, `${round}_${subj}_${num}.md`]) {
    const p = `${base}/${sub}/${nm}`; if (existsSync(p)) return p;
  }
  return null;
}
function readSt(md) {
  const t = readFileSync(md, 'utf8'); const m = t.match(/\nsearchable_text: \|\n((?:  .*\n?)*)/);
  return m ? m[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join('\n').trim() : null;
}
function fmVerify(md) { const t = readFileSync(md, 'utf8'); const m = t.match(/\ncorrector_verify:\s*(.*)/); return m ? m[1].trim() : null; }

function collectSlugs() {
  const list = getOpt('--list');
  if (list) return list.split(',').map((s) => s.trim()).filter(Boolean);
  const round = getOpt('--round'); const subj = getOpt('--subj');
  if (!round) { console.error('--list 또는 --round 필요'); process.exit(1); }
  const base = `${REPO}/docs/problems/${round.split('_')[0]}`; const out = [];
  if (existsSync(base)) for (const sub of readdirSync(base)) for (const f of readdirSync(`${base}/${sub}`)) {
    if (!f.endsWith('.md')) continue; const s = f.replace(/\.md$/, '');
    if (s.startsWith(round + '_') && (!subj || s.includes(`_${subj}_`))) out.push(s);
  }
  return out.sort();
}

function claudeCall(prompt, imgDir) {
  return new Promise((res) => {
    const c = spawn('claude', ['-p', prompt, '--model', MODEL, '--output-format', 'json', '--add-dir', imgDir], { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = ''; c.stdout.on('data', (d) => (out += d));
    c.on('close', () => { try { res(JSON.parse(out).result || ''); } catch { res(''); } });
  });
}

function writeVerify(md, status, issues) {
  let t = readFileSync(md, 'utf8');
  t = t.replace(/\ncorrector_verify:.*(?=\n)/, '');
  t = t.replace(/\ncorrector_verify_issues:(?:\n  - .*)*(?=\n)/, '');
  let fb = `\ncorrector_verify: ${status}`;
  if (issues.length) fb += `\ncorrector_verify_issues:\n` + issues.map((x) => '  - ' + JSON.stringify(String(x))).join('\n');
  t = t.replace(/\nsearchable_text:/, fb + '\nsearchable_text:');
  writeFileSync(md, t);
}

// 청크 1콜: N문제 이미지+전사 → JSON 배열 [{id,ok,issues}] (모든 문제 같은 round = imgDir 공유)
async function verifyChunk(items) {
  // #1 빈-본문 게이트: searchable_text 가 비면 메타/교정 실패라 검증대상 아님 → 즉시 issues(재전사 필요).
  //    빈 본문이 sonnet "검증할 게 없음 → ok" 로 조용히 통과하던 silent 갭 차단(가형_19 류, 0자인데 ok 였음).
  const EMPTY_MIN = 20;
  const empties = items.filter((it) => (readSt(it.md) || '').trim().length < EMPTY_MIN);
  for (const it of empties) writeVerify(it.md, 'issues', ['빈 본문(메타/교정 실패) — 이미지에서 재전사 필요']);
  if (empties.length) log(`  ⚠ 빈본문 ${empties.length}건 → issues(재전사 필요): [${empties.map((i) => i.num).join(',')}]`);
  items = items.filter((it) => (readSt(it.md) || '').trim().length >= EMPTY_MIN);
  if (!items.length) return;
  const imgDir = `${REPO}/db/raw/${items[0].round}/images`;
  let prompt = `다음 ${items.length}개 수능 수학 문제를 각각 이미지와 "전사 텍스트"를 한 글자씩 대조해 교정 정확도를 검증하라.
- 놓침: 이미지엔 있는데 전사에서 빠지거나 틀린 것(수식 기호·숫자·보기 ①~⑤·첨자·한글 오타).
- 환각: 전사엔 있는데 이미지엔 없는 것.
{{FIG0}}·{{INL0}}·{{TABLE0}} placeholder 는 그림/표 자리표시라 내용은 평가 대상이 아니나({{INL}}은 본문 문장 중간의 인라인 도형 마커), 위치(선택지 앞뒤·문장 내 등)가 이미지와 다르면 issue.
추론 길게 말고 JSON 배열만 출력(설명·코드펜스 없이): [{"id":번호,"ok":참거짓,"issues":["문제 한 줄",...]}]
※ id 는 아래 각 항목의 [문제 N] 의 N(1부터)을 그대로 쓴다.`;
  // ★ id = 청크 내 1-based 인덱스(문항번호 X). 한 자리 문항("01"→정수 1 반환)·과목혼재(가형/나형 동일 num) 매칭 실패 방지.
  items.forEach((it, i) =>
    prompt += `\n\n[문제 ${i + 1}] 이미지: ${imgDir}/${it.round}_${it.subj}_${String(it.num).padStart(2, '0')}.png\n전사: ${readSt(it.md)}`);
  const t0 = Date.now();
  const out = await claudeCall(prompt, imgDir);
  const sec = ((Date.now() - t0) / 1000).toFixed(0);
  let arr;
  const jraw = (out.match(/\[[\s\S]*\]/) || [''])[0];
  // ★ sonnet 은 대개 유효 JSON(\\sqrt 처럼 백슬래시 이미 이스케이프됨)을 준다 → raw parse 먼저.
  //   무효 백슬래시 보정 replace 를 무조건 돌리면 정상 \\ 까지 \\\ 로 깨뜨려 parsefail 됐다(이 버그 수정).
  try { arr = JSON.parse(jraw); }
  catch { try { arr = JSON.parse(jraw.replace(/\\(?!["\\/bfnrtu])/g, '\\\\')); } catch { arr = null; } }
  if (!Array.isArray(arr)) {
    // #3 배치 파싱실패 → 단건 폴백: 청크>1 이면 1개씩 재검증(sonnet 은 단건이면 파싱가능 응답률 높다 —
    //    배치가 한 문제의 깨진 수식 때문에 전체 JSON 을 망가뜨려 멀쩡한 나머지까지 parsefail 시키던 낭비 차단).
    if (items.length > 1) {
      log(`  ↻ 청크[${items.map((i) => i.num).join(',')}] 배치 파싱실패 — ${sec}s → 단건 폴백 ${items.length}개`);
      for (const it of items) await verifyChunk([it]);
      return;
    }
    const dbg = `${LOGDIR}/verify_batch_parsefail_${items[0].round}_${items[0].num}.txt`;
    appendFileSync(dbg, `=== ${new Date().toISOString()} (${sec}s) ===\n${out}\n`);  // catch 삼킴 방지: 실제 out 보존
    log(`  ⚠ 단건[${items[0].num}] 파싱실패 — ${sec}s (raw → ${dbg})`);
    writeVerify(items[0].md, 'parsefail', ['단건 파싱실패']);
    return;
  }
  const byId = new Map(arr.map((r) => [String(parseInt(r.id, 10)), r]));   // 1-based 인덱스 매칭(정수화)
  let ok = 0, iss = 0;
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const r = byId.get(String(i + 1));
    if (!r) { writeVerify(it.md, 'parsefail', ['배치 응답 누락']); continue; }
    const issues = Array.isArray(r.issues) ? r.issues : [];
    const status = r.ok === true ? 'ok' : r.ok === false ? 'issues' : 'parsefail';
    writeVerify(it.md, status, issues);
    if (status === 'ok') ok++; else if (status === 'issues') iss++;
  }
  log(`  청크[${items.map((i) => i.num).join(',')}] ${sec}s → ok ${ok} / issues ${iss}`);
}

(async () => {
  const raw = collectSlugs();
  let items = raw.map(parseSlug).filter(Boolean).map((p) => ({ ...p, md: findMd(p.round, p.subj, p.num) })).filter((p) => p.md);
  if (!FORCE) items = items.filter((p) => fmVerify(p.md) !== 'ok');
  const byRound = new Map();                                   // round별 그룹(imgDir 공유) → 청크
  for (const it of items) { if (!byRound.has(it.round)) byRound.set(it.round, []); byRound.get(it.round).push(it); }
  const chunks = [];                                           // 전 라운드 청크 평탄화
  for (const [, its] of byRound)
    for (let i = 0; i < its.length; i += CHUNK) chunks.push(its.slice(i, i + CHUNK));
  log(`══ verify_batch 시작: ${items.length}문제 · 청크 ${CHUNK} · 총청크 ${chunks.length} · 병렬 ${PAR} · ${MODEL} · LOG ${LOG}`);
  let ci = 0;                                                  // 동시성 PAR 풀 — 워커가 청크를 하나씩 집어간다
  async function worker() { while (ci < chunks.length) { const my = chunks[ci++]; await verifyChunk(my); } }
  await Promise.all(Array.from({ length: Math.min(PAR, chunks.length || 1) }, worker));
  const fin = items.map((p) => fmVerify(p.md));
  log(`══ 완료: ok ${fin.filter((x) => x === 'ok').length} / issues ${fin.filter((x) => x === 'issues').length} / parsefail ${fin.filter((x) => x === 'parsefail').length}`);
})();
