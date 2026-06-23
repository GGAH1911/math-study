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
// ★claude -p 캐시 친화: 레포 cwd 면 git status(미커밋 변경 다발)가 매 호출 시스템 프롬프트의
//   env 블록을 바꿔 프롬프트 캐시를 깬다(실측: 콜당 ~17k 토큰 재기록). 깨끗한 빈 cwd 에서 실행하면
//   prefix 가 안정돼 cache_read 가 살아난다(~76% 입력비용 절감). 이미지·전사는 --add-dir/프롬프트로 전달.
const CLEAN_DIR = '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });
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
    // CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1: git 블록 제거 → prefix 안정(clean cwd 보강, 실측 cache_read 고정).
    const c = spawn('claude', ['-p', prompt, '--model', MODEL, '--output-format', 'json', '--add-dir', imgDir], { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    let out = ''; c.stdout.on('data', (d) => (out += d));
    c.on('close', () => { try { const j = JSON.parse(out); const u = j.usage || {}; appendFileSync(`${LOGDIR}/verify_usage.log`, `${MODEL}\tcr=${u.cache_read_input_tokens ?? '?'}\tcc=${u.cache_creation_input_tokens ?? '?'}\tin=${u.input_tokens ?? '?'}\tout=${u.output_tokens ?? '?'}\n`); res(j.result || ''); } catch { res(''); } });
  });
}

// ★gemma 검증(로컬 mlx HTTP) — 무료·CLI오버헤드0. 문제별 1콜(mlx 멀티이미지 배치 비신뢰). 라인 한 줄(ok / issues|이유).
const GEMMA_URL = process.env.GEMMA_URL || 'http://100.79.230.49:8080/v1/chat/completions';
async function gemmaVerify(st, imgPath) {
  try {
    const b64 = readFileSync(imgPath).toString('base64');
    const prompt = `이 수능 수학 문제를 이미지와 아래 "전사"를 글자·수식·기호 한 글자씩 시각 대조해 검증하라. ★문제를 절대 풀지 마라(답·풀이·추론 금지). 출력은 정확히 한 줄만: "ok"(이미지와 일치) 또는 "issues|짧은이유(20자 이내, 1개)"(불일치). 다른 텍스트 절대 금지.\n전사: ${st}`;
    const r = await fetch(GEMMA_URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ model: process.env.GEMMA_MODEL || 'mlx-community/gemma-4-26B-A4B-it-qat-4bit', max_tokens: 120, temperature: 0, messages: [{ role: 'user', content: [{ type: 'text', text: prompt }, { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }] }] }) });
    const j = await r.json();
    return j.choices?.[0]?.message?.content || '';
  } catch { return ''; }
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
  // ★MODEL=gemma: 로컬 무료 검증(문제별 1콜, Claude 0·CLI오버헤드0). 다른 모델(sonnet/haiku)은 아래 배치 1콜.
  if (MODEL === 'gemma') {
    let ok = 0, iss = 0, pf = 0;
    for (const it of items) {
      const imgPath = `${imgDir}/${it.round}_${it.subj}_${String(it.num).padStart(2, '0')}.png`;
      const out = await gemmaVerify(readSt(it.md), imgPath);
      const m = out.match(/\b(ok|issues)\b/i);
      if (!m) { writeVerify(it.md, 'parsefail', ['gemma 검증 무응답']); pf++; continue; }
      const isOk = m[1].toLowerCase() === 'ok';
      writeVerify(it.md, isOk ? 'ok' : 'issues', isOk ? [] : [(out.split('|')[1] || '').trim() || '불일치']);
      if (isOk) ok++; else iss++;
    }
    log(`  청크[${items.map((i) => i.num).join(',')}] gemma검증 → ok ${ok} / issues ${iss}${pf ? ` / pf ${pf}` : ''}`);
    return;
  }
  let prompt = `다음 ${items.length}개 수능 수학 문제를 각각 이미지와 "전사 텍스트"를 한 글자씩 시각 대조해 교정 정확도를 검증하라.
★★문제를 절대 풀지 마라(답 계산·풀이·증명·추론 전부 금지). 오직 전사의 글자·수식·기호가 이미지와 같은지 눈으로 대조만.
- 놓침(이미지엔 있는데 전사 누락/오기) 또는 환각(전사엔 있는데 이미지에 없음)만 본다. {{FIG/INL/TABLE}} placeholder는 자리표시라 내용 평가 안 함(위치 어긋나면 issue).
★★출력은 각 문제당 **정확히 한 줄**, 아래 형식만(JSON·설명·코드펜스·다른 텍스트 전부 금지):
1|ok
2|issues|짧은 이유(20자 이내, 1개만)
3|ok
줄 맨 앞 숫자는 아래 [문제 N]의 N(1,2,3,… 순서 — 전사 속 문제번호가 아님). 총 ${items.length}줄만 출력.`;
  // ★ id = 청크 내 1-based 인덱스(문항번호 X). 한 자리 문항("01"→정수 1 반환)·과목혼재(가형/나형 동일 num) 매칭 실패 방지.
  items.forEach((it, i) =>
    prompt += `\n\n[문제 ${i + 1}] 이미지: ${imgDir}/${it.round}_${it.subj}_${String(it.num).padStart(2, '0')}.png\n전사: ${readSt(it.md)}`);
  const t0 = Date.now();
  const out = await claudeCall(prompt, imgDir);
  const sec = ((Date.now() - t0) / 1000).toFixed(0);
  // ★라인 파싱(JSON.parse 없음 → 장문·LaTeX·따옴표로 안 깨짐 = parsefail 루프 원천차단). 인덱스(1..N) 우선, 전사번호(num) 폴백.
  //   ★single-fallback 제거: parsefail은 그 문제만 표시(재시도·재귀 없음) → 콜 폭증·쿼터 burn 차단.
  const vmap = new Map();
  for (const line of out.split('\n')) {
    const m = line.trim().match(/^(\d+)\s*\|\s*(ok|issues)\b\s*(?:\|\s*(.*))?$/i);
    if (m) vmap.set(parseInt(m[1], 10), { ok: m[2].toLowerCase() === 'ok', issue: (m[3] || '').trim() });
  }
  let ok = 0, iss = 0, pf = 0;
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const r = vmap.get(i + 1) || vmap.get(parseInt(it.num, 10));
    if (!r) { writeVerify(it.md, 'parsefail', ['검증 라인 누락']); pf++; continue; }  // 그 문제만 parsefail → opus 처리(재시도 0)
    writeVerify(it.md, r.ok ? 'ok' : 'issues', r.ok ? [] : [r.issue || '불일치']);
    if (r.ok) ok++; else iss++;
  }
  if (pf) appendFileSync(`${LOGDIR}/verify_parsefail_${TS}.txt`, `=== ${new Date().toISOString()} 청크[${items.map((i) => i.num).join(',')}] pf${pf} ===\n${out.slice(0, 800)}\n`);
  log(`  청크[${items.map((i) => i.num).join(',')}] ${sec}s → ok ${ok} / issues ${iss}${pf ? ` / parsefail ${pf}` : ''}`);
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
