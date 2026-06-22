#!/usr/bin/env node
// 교정기(corrector) — 통합 파이프라인 + 안전장치.
//   ① 결정론 추출: extract_figures.py (이미지·표·placeholder).  ② Gemini(agy) 텍스트 교정.
//   ③ 검증 게이트: 제어문자0·placeholder보존·중괄호균형·길이·선택지 → 통과만 적용.
//   ④ 자가치유: 검증 실패 시 Sonnet(claude) 재교정 → 재검증 → 통과 적용, 둘 다 실패 시 격리.
// 출력 형식은 JSON 금지(LaTeX 백슬래시 손상) → ===FIXES===/===CORRECTED===/===END=== 마커 raw.
// 사용: node corrector.mjs <round> <subj> <num>
import { spawnSync, spawn } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = dirname(fileURLToPath(import.meta.url));
const REPO = '/home/insung/Projects/math-study';
const GEMINI = process.env.CORR_MODEL || 'Gemini 3.5 Flash (Medium)';
const QLOG = '/tmp/ingest_logs/corrector_quarantine.log';
// ★claude -p 캐시 친화: 레포 cwd면 git status(미커밋 변경)가 매 호출 시스템 프롬프트 env 블록을
//   바꿔 프롬프트 캐시를 깬다(콜당 ~17k 재기록). 깨끗한 빈 cwd에서 spawn → prefix 안정 → cache_read 생존.
//   이미지 접근은 --add-dir(절대경로)로 유지. 참고: docs/CLAUDE_P_CACHING.md, lib/claude_p.mjs.
const CLEAN_DIR = process.env.CLAUDE_P_CWD || '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

// agy(Gemini) = plain text. 쿼터 소진 = 빈 출력.
function agyCall(prompt, imgDir, retries = 2) {
  return new Promise((res) => {
    const run = (n) => {
      const c = spawn('agy', ['-p', prompt, '--model', GEMINI, '--add-dir', imgDir, '--print-timeout', '6m'], { stdio: ['ignore', 'pipe', 'pipe'] });
      c.stdout.setEncoding('utf8'); let out = '';
      c.stdout.on('data', (d) => (out += d));
      c.on('close', () => {
        // 빈출력(쿼터/부하) 또는 마커 없음(agy 단일 인스턴스 큐 충돌 "백그라운드 태스크 대기") → 8s 후 재시도.
        // 진짜 쿼터 소진은 재시도해도 계속 빈출력 → 결국 res(빈문자열) → exit 3.
        if ((!out.trim() || !/===CORRECTED===/.test(out)) && n > 0) setTimeout(() => run(n - 1), 8000);
        else res(out);
      });
    };
    run(retries);
  });
}
// claude(Sonnet) = --output-format json → {result:"..."} 래퍼. 자가치유·재교정용(별도 백엔드·쿼터).
// ★cwd: CLEAN_DIR → 프롬프트 캐시 생존(verify_batch와 동일 패턴). maxTurns>0이면 --max-turns 부여
//   = 이미지 Read→교정→자가검증을 한 warm-cache 프로세스 안에서 도는 에이전트 루프(상한).
function claudeCall(prompt, imgDir, model = 'sonnet', maxTurns = 0) {
  return new Promise((res) => {
    const args = ['-p', prompt, '--model', model, '--output-format', 'json', '--add-dir', imgDir];
    if (maxTurns > 0) args.push('--max-turns', String(maxTurns));
    const c = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR });
    c.stdout.setEncoding('utf8'); let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => {
      try {
        const j = JSON.parse(out); const u = j.usage || {};
        appendFileSync('/tmp/corr_usage.log', `${model}\tcreate=${u.cache_creation_input_tokens ?? '?'}\tread=${u.cache_read_input_tokens ?? '?'}\tin=${u.input_tokens ?? '?'}\tout=${u.output_tokens ?? '?'}\n`);
        res(j.result || '');
      } catch { res(''); }
    });
  });
}
// gemma4 (맥북 mlx_vlm.server, OpenAI 호환 /v1/chat/completions) — 이미지 base64 첨부. 로컬이라 토큰·쿼터 0.
const GEMMA_URL = process.env.GEMMA_URL || 'http://100.79.230.49:8080/v1/chat/completions';
async function gemmaCall(prompt, imgPath) {
  try {
    const b64 = readFileSync(imgPath).toString('base64');
    const res = await fetch(GEMMA_URL, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        model: process.env.GEMMA_MODEL || 'mlx-community/gemma-4-26B-A4B-it-qat-4bit', max_tokens: 3000, temperature: 0,  // 26B-A4B(MoE) 기본·env로 토글. 1400→3000: 긴 킬러 출력 잘림 방지
        messages: [{ role: 'user', content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } },
        ] }],
      }),
    });
    const j = await res.json();
    return j.choices?.[0]?.message?.content || '';
  } catch (e) { console.error('[gemma 에러]', e?.message || e); return ''; }
}
// OpenRouter 무료 비전 폴백(gemma-4-26b:free — Google AI Studio, agy와 별도 쿼터풀). agy 쿼터 소진 시 사용. 키=레포밖 파일.
const OR_KEY = (() => { try { return readFileSync((process.env.HOME || '') + '/.config/math-study/openrouter.key', 'utf8').trim(); } catch { return ''; } })();
async function orCall(prompt, imgPath, retries = 2) {
  if (!OR_KEY) return '';
  const b64 = readFileSync(imgPath).toString('base64');
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST', headers: { Authorization: 'Bearer ' + OR_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: 'google/gemma-4-26b-a4b-it:free', max_tokens: 3000, temperature: 0,
          messages: [{ role: 'user', content: [{ type: 'text', text: prompt }, { type: 'image_url', image_url: { url: `data:image/png;base64,${b64}` } }] }] }),
      });
      const j = await res.json();
      if (j.error) { if (String(j.error.code) === '429' && i < retries) { await new Promise((r) => setTimeout(r, 8000)); continue; } return ''; }
      return j.choices?.[0]?.message?.content || '';
    } catch { if (i < retries) { await new Promise((r) => setTimeout(r, 8000)); continue; } return ''; }
  }
  return '';
}
// 마커 파싱 + sanitize($ 델리미터·제어문자 제거).
function parseCorrected(out) {
  const cm = out.match(/===CORRECTED===\r?\n([\s\S]*?)\r?\n===END===/);
  if (!cm) return null;
  const corrected = cm[1].replace(/\$/g, '').replace(/[\x00-\x09\x0b-\x1f]/g, '').replace(/[ \t]+$/gm, '')
    // 선택지 연속중복 제거(corrector가 보기 두 줄 분할 시 첫 보기를 복제하는 글리치): "① X ① X" → "① X".
    .replace(/([①②③④⑤])[ \t]*([^\n①②③④⑤]+?)[ \t]+\1[ \t]*\2(?=[ \t]|\n|$|[①②③④⑤])/g, '$1 $2');
  const fmFix = out.match(/===FIXES===\r?\n([\s\S]*?)\r?\n===CORRECTED===/);
  const NOFIX = /^(없음|없습니다|none|n\/a|해당\s*없음|(수정|변경|교정|고친\s*것|고칠\s*것)\s*(사항\s*)?(은\s*)?없음)\.?$/i;
  const fixes = fmFix ? fmFix[1].split('\n').map((l) => l.replace(/^\s*-\s*/, '').trim()).filter((x) => x && !NOFIX.test(x)) : [];
  return { corrected, fixes };
}
// 검증 게이트 — 실패 사유 배열(빈 배열=통과).
const PH = (s) => (s.match(/\{\{(?:(?:FIG|INL|TABLE)\d+|BOX\d+_(?:START|END))\}\}/g) || []).sort().join(',');
// placeholder 화해: extract(st)의 placeholder 집합에 corrected 를 맞춘다 — gemma 가 추가한 backing 없는
//   {{FIG/TABLE/BOX}}(extract 미감지·벡터 그래프 등)는 제거, gemma 가 누락한 건 끝에 복원. PH 게이트 노이즈 격리 차단.
function reconcilePH(corrected, st) {
  const RE = /\{\{(?:(?:FIG|INL|TABLE)\d+|BOX\d+_(?:START|END))\}\}/g;
  const stSet = new Set(st.match(RE) || []), corrArr = corrected.match(RE) || [];
  const corrSet = new Set(corrArr);
  let out = corrected; const changed = [];
  // gemma 추가분은 '제거 안 함' — 비전이 extract보다 정확(extract가 못 잡은 벡터그래프·도식을 gemma가 봄).
  //   strip 하면 verify가 '도형 누락' 지적 → 재교정 → agy 재추가 → strip 무한루프(느려짐의 주범). 그래서 보존.
  for (const ph of stSet) {
    if (corrSet.has(ph)) continue;                                   // 누락분만 복원
    if (ph.includes('INL')) {
      // ★INL 은 인라인(줄 중간) — 끝에 append 하면 위치 깨짐. st 의 ph 앞 컨텍스트를 corrected 에서 찾아 그 자리에 삽입.
      const before = (st.split(ph)[0] || '').replace(/\s+$/, '').slice(-14).trim();
      const i = before ? out.indexOf(before) : -1;
      if (i >= 0) { const at = i + before.length; out = out.slice(0, at) + ' ' + ph + ' ' + out.slice(at); changed.push('+' + ph + '@인라인'); }
      else changed.push('?' + ph + '@위치불명(복원skip→재교정에 맡김)');   // 끝 append 안 함
    } else {
      out = out.replace(/\s*$/, '') + '\n' + ph; changed.push('+' + ph);   // 블록(FIG/TABLE/BOX)은 끝줄에 복원
    }
  }
  out = out.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  if (changed.length) console.log(`   placeholder 누락복원: ${changed.join(' ')}`);
  return out;
}
function validate(corrected, st) {
  const f = [];
  if (!corrected || !corrected.trim()) return ['빈출력'];
  if (/[\x00-\x09\x0b-\x1f]/.test(corrected)) f.push('제어문자');       // YAML/서버 다운 차단
  const _re = /\{\{(?:(?:FIG|INL|TABLE)\d+|BOX\d+_(?:START|END))\}\}/g;
  const _corrP = new Set(corrected.match(_re) || []);
  const _miss = [...new Set(st.match(_re) || [])].filter((p) => !_corrP.has(p));
  if (_miss.length) f.push(`placeholder누락(${_miss.join(',')})`);   // gemma 추가분 허용(비전 우선) · 누락만 실패
  const o = (corrected.match(/\{/g) || []).length, c = (corrected.match(/\}/g) || []).length;
  if (o !== c) f.push(`중괄호(${o}/${c})`);                              // LaTeX 균형
  // 도형 설명 [그림:...] 블록은 교정이 정당하게 제거(OK 문제 표준=본문에 설명 없음) → 길이비 기준에서 제외.
  // 안 그러면 짧은 문제(예 가형_28)가 설명 제거 후 0.35로 떨어져 false-positive 격리됨.
  const _stripFig = (s) => s.replace(/\[그림:[^\]]*\]/g, '');
  const ratio = _stripFig(corrected).length / Math.max(1, _stripFig(st).length);
  if (ratio < 0.4 || ratio > 3.0) f.push(`길이비(${ratio.toFixed(2)})`);  // 환각·누락. 상한 완화: 원본 텍스트레이어가 깨져 짧은 경우 corrected가 정상이어도 비율이 커짐(false positive 방지)
  if (/①/.test(st) && !/①/.test(corrected)) f.push('선택지누락');
  if (/\$/.test(corrected)) f.push('잔여$');                             // 방향A 위반
  return f;
}
function findMd(round, subj, num) {
  const base = `${REPO}/docs/problems/${round.split('_')[0]}`;
  if (!existsSync(base)) return null;
  const n2 = String(num).padStart(2, '0');
  for (const sub of readdirSync(base))
    for (const nm of [`${round}_${subj}_${n2}.md`, `${round}_${subj}_${num}.md`]) {
      const p = `${base}/${sub}/${nm}`;
      if (existsSync(p)) return p;
    }
  return null;
}

const [round, subj, num] = process.argv.slice(2);
if (!round) { console.log('사용: node corrector.mjs <round> <subj> <num>'); process.exit(1); }

// ① 결정론 추출
console.log('① 결정론 추출(extract_figures)…');
const ex = spawnSync('python3', [`${DIR}/extract_figures.py`, round, subj, num, '--apply'], { encoding: 'utf8' });
process.stdout.write(ex.stdout || ''); if (ex.stderr) process.stderr.write(ex.stderr);

const md = findMd(round, subj, num);
if (!md) { console.log('md 못찾음'); process.exit(1); }
let txt = readFileSync(md, 'utf8');
const m = txt.match(/\nsearchable_text: \|\n((?:  .*\n?)*)/);
if (!m) { console.log('searchable_text 없음'); process.exit(1); }
const st = m[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join('\n').trim();

const imgDir = `${REPO}/db/raw/${round}/images`;
const img = `${imgDir}/${round}_${subj}_${String(num).padStart(2, '0')}.png`;
const _back = process.env.CORR_BACKEND || 'haiku';
const prompt = _back === 'gemma'
  ? `이미지의 수능 수학 문제를 전사·교정하라. 수식은 LaTeX로 쓰되 $ 기호 없이(렌더러가 한글/수식 자동 분리). 객관식이면 보기 ①~⑤를 값과 함께 포함(★각 ①~⑤는 한 번씩만 — 두 줄로 나눠 배치해도 보기를 복제하지 마라). 전사에 {{FIG0}}·{{INL0}}·{{TABLE0}}가 있으면 그 자리에 그대로 두고({{INLn}}은 문장 중간 인라인 도형이니 별도 줄로 빼지 말 것), 없으면 새로 만들지 마라. 그림/표 내용을 본문에 풀어쓰지 마라. ★도형 라벨 제거: 도형 안의 점 라벨(O·A·B·P·Q·A_n 같은 낱글자/기호)이나 각도(π/3 등)가 본문(특히 {{FIG}} 근처·선택지 앞)에 낱개로 나열돼 있으면 제거하라 — 그건 도형의 일부지 문제 문장이 아니다.
★★줄바꿈 보존: 이미지에 줄이 나뉜 대로 한 줄씩 전사하라(절대 한 줄로 합치지 마라). 특히 조건 (가)(나)(다)·불릿(◦·•)·유도단계 (ⅰ)(ⅱ)(ⅲ)·결론식·질문("…값은?"/"…구하시오")을 이미지처럼 각각 별도 줄로 개행. 렌더러가 줄 구조로 박스를 판정하므로 줄바꿈이 곧 레이아웃이다. ★연속/반복 생략 기호가 이미지에 있으면 **방향·위치 그대로** 전사하라 — 누락 금지. 세로 생략(도형/수식이 위→아래 반복, 보통 도형들 아래·선택지 위)이면 **⋮**, 가로 생략(좌→우 반복, 예: a_1, a_2, ⋯, a_n)이면 **⋯**(또는 …)로, 이미지의 방향대로 옮겨라.
아래 형식 그대로만 출력:
===FIXES===
- 고친 항목을 하나씩 모두 나열(고친 곳마다 한 줄, 없으면 이 줄 비움)
===CORRECTED===
교정 전사 전문($ 없이, placeholder 유지)
===END===
--- 추출 전사 ---
${st}`
  : `너는 한국 수능 기출의 전사 텍스트를 원본 이미지와 한 글자씩 대조해 교정한다.
아래 "추출 전사"는 PDF 텍스트레이어에서 뽑아 깨진 기호·오타·누락이 있을 수 있다. 이미지대로 정확히 교정하라(수식 기호·보기 ①~⑤·숫자 정확히). 환각 금지 — 이미지에 있는 그대로.
★수식: LaTeX 명령(\\frac, \\overline, \\sqrt 등)은 쓰되 **$...$ 델리미터로 감싸지 마라**. 렌더러가 한글/수식을 자동 분리한다 — $ 를 넣으면 KaTeX가 깨진다.
★★줄바꿈 보존: 이미지에 줄이 나뉜 대로 **한 줄씩** 전사하라(절대 한 줄로 합치지 마라). 특히 조건 (가)(나)(다)·불릿(◦·•)·유도단계 (ⅰ)(ⅱ)(ⅲ)·결론식·질문("…값은?"/"…구하시오")을 이미지처럼 **각각 별도 줄로 개행**. 렌더러가 줄 구조로 박스를 판정하므로 줄바꿈이 곧 레이아웃이다. ★연속/반복 생략 기호가 이미지에 있으면 **방향·위치 그대로** 전사하라 — 누락 금지. 세로 생략(도형/수식이 위→아래 반복, 보통 도형들 아래·선택지 위)이면 **⋮**, 가로 생략(좌→우 반복, 예: a_1, a_2, ⋯, a_n)이면 **⋯**(또는 …)로, 이미지의 방향대로 옮겨라.
★★전사에 {{FIG0}}·{{INL0}}·{{TABLE0}} 형태의 placeholder가 **이미 있으면** 그 자리·개수 그대로 두라(그림/표 자리). {{INLn}}은 본문 문장 중간의 인라인 도형 마커이니 **그 문장 안 제자리에 그대로** 두라(별도 줄로 빼지 마라 — {{FIG}}/{{TABLE}}만 자기 줄). {{INLn}} 은 도형 자체이니 그 **옆에 같은 도형을 글자(⌒·◠·△ 등)로 중복 표기하지 마라**(마커만 남기고 중복 기호 제거). ★여러 {{FIGn}}이 있으면 **번호 오름차순**(작은 번호가 위/앞 — {{FIG0}}이 {{FIG1}}보다 먼저)으로 배치하라(이미지 위→아래 순서 = 번호 순서). ★단, 전사에 없는 placeholder를 **새로 만들지 마라** — 이미지에 그림/표가 보여도 placeholder를 추가하지 말고, 전사에 있는 텍스트만 교정하라.
★★placeholder 토큰({{FIG0}}·{{INL0}}·{{TABLE0}}·{{BOX0_START}}·{{BOX0_END}})은 **그 자리에 반드시 그대로 남겨라 — 절대 지우지 마라**(개수·위치 보존). 다만 그 그림/표/(가)(나) 박스의 **내용(표 셀 값·그림 설명)을 본문 텍스트로 풀어쓰지는 마라**. 즉 "토큰은 유지, 그 내용 중복 서술만 금지"(렌더 시 토큰이 그림/표로 대체됨). {{BOXn_START}}·{{BOXn_END}}는 테두리 박스의 시작/끝 경계 마커이니 각자 그 줄에 그대로 두라(둘 사이 줄들이 박스로 감싸짐).
★★★출력은 아래 형식 그대로(JSON 절대 금지 — LaTeX 백슬래시가 JSON escape로 깨진다). 마커 줄은 정확히 이 글자로:
===FIXES===
- <무엇을 왜 고쳤는지 한 줄>
- <…여러 줄 가능, 없으면 이 줄 비움>
===CORRECTED===
<교정 전사 전문 — placeholder 포함, $ 없이, \\frac·\\overline 등 LaTeX 명령은 백슬래시 그대로 한 번만>
===END===
--- 추출 전사 ---
${st}
--- 원본 이미지 ---
Read 로 볼 것: ${img}`;

// 앞선 sonnet 검증(verify_corrected)이 지적한 사항이 있으면 재교정 프롬프트에 주입(반드시 반영).
const _vi = txt.match(/\ncorrector_verify_issues:\n((?:  - .*\n?)+)/);
const promptF = _vi ? prompt + '\n\n★앞선 검증이 지적한 교정 필요 사항(반드시 반영):\n' + _vi[1].replace(/^  - /gm, '- ') : prompt;

// ② 교정 → ③ 검증. CORR_BACKEND=gemma(로컬 맥북, 토큰0) / 기본 claude(haiku).
const t0 = Date.now();
const BACKEND = process.env.CORR_BACKEND || 'haiku';
let out, by;
if (BACKEND === 'gemma') {
  console.log('② gemma4(로컬 맥북) 교정…');
  out = await gemmaCall(promptF, img); by = 'gemma4';
} else if (BACKEND === 'agy') {
  console.log('② agy(Gemini) 재교정…');                 // 재교정 전용(gemma는 본교정에 전념 → 별 백엔드라 병렬)
  out = await agyCall(promptF, imgDir); by = 'gemini';
  // ★agy 쿼터소진(빈출력)이어도 sonnet 폴백 안 함 — agy만 사용(무료). 빈출력→아래 exit 3→파이프라인이 재큐+대기 후 agy 재시도(사용자 지정).
} else if (BACKEND === 'or') {
  console.log('② OpenRouter gemma-4-26b:free 교정…');   // 3번째 병렬 레인(별도 무료풀, 429는 빈출력→재시도)
  out = await orCall(promptF, img); by = 'or-gemma26b';
} else if (BACKEND === 'sonnet') {
  console.log('② claude(Sonnet) 재교정…');               // 병렬 가능(PAR_G>1) — gemma4 실패분 빠르게 재교정
  out = await claudeCall(promptF, imgDir, 'sonnet'); by = 'sonnet';
} else if (BACKEND === 'agent') {
  // ★재교정 에이전트 루프: claude -p가 이미지를 Read→대조→교정→자가검증을 한 warm-cache 프로세스에서.
  //   clean cwd로 캐시 생존, --max-turns로 상한. agy(다운) 대체 + 오케스트레이터 수동 재교정 자동화.
  const am = process.env.AGENT_MODEL || 'sonnet';
  const at = parseInt(process.env.AGENT_MAXTURNS || '6', 10);
  console.log(`② claude(${am}) agent-loop 재교정 (max-turns ${at}, clean cwd)…`);
  out = await claudeCall(promptF, imgDir, am, at); by = `agent-${am}`;
} else {
  console.log('② claude(Haiku) 교정…');
  out = await claudeCall(promptF, imgDir, 'haiku'); by = 'haiku';
}
if (!out.trim()) { console.log('빈출력(한도/에러) — ①결정론만 반영'); process.exit(3); }  // exit 3 = 한도(배치 멈춤)
let parsed = parseCorrected(out);
if (!parsed && process.env.CORR_DEBUG) console.error('[DEBUG] 마커 파싱 실패. out 앞 600자:\n' + out.slice(0, 600) + '\n---끝---');
if (parsed) parsed.corrected = reconcilePH(parsed.corrected, st);   // placeholder 노이즈 화해(격리 방지)
let fails = parsed ? validate(parsed.corrected, st) : ['파싱실패'];

// ④ 자가치유: 검증 실패 → 재교정 → 재검증 (gemma는 재시도, claude는 sonnet 승격)
if (fails.length) {
  console.log(`③ 검증 실패(${fails.join(', ')}) → ④ 자가치유 재시도…`);
  const out2 = BACKEND === 'gemma' ? await gemmaCall(promptF, img)
    : BACKEND === 'agy' ? await agyCall(promptF, imgDir)
    : BACKEND === 'or' ? await orCall(promptF, img)
    : BACKEND === 'agent' ? await claudeCall(promptF, imgDir, process.env.AGENT_MODEL || 'sonnet', parseInt(process.env.AGENT_MAXTURNS || '6', 10))
    : BACKEND === 'sonnet' ? await claudeCall(promptF, imgDir, 'sonnet')
    : await claudeCall(promptF, imgDir);
  const parsed2 = parseCorrected(out2);
  if (parsed2) parsed2.corrected = reconcilePH(parsed2.corrected, st);   // 자가치유분도 화해
  const fails2 = parsed2 ? validate(parsed2.corrected, st) : ['파싱실패'];
  if (!fails2.length) { parsed = parsed2; fails = []; if (BACKEND !== 'gemma' && BACKEND !== 'agy' && BACKEND !== 'or' && BACKEND !== 'sonnet' && BACKEND !== 'agent') by = 'sonnet'; console.log('④ 자가치유 통과'); }  // 자가치유는 같은 백엔드 재시도 → by 유지(haiku만 sonnet 승격)
  else {
    mkdirSync(dirname(QLOG), { recursive: true });
    appendFileSync(QLOG, `${round}_${subj}_${num}\t1차:${fails.join('|')}\t재시도:${fails2.join('|')}\n`);
    // 영구 격리 마커(반복 재시도·쿼터 낭비 차단) — 원인 수정 후 수동으로 corrector_quarantine 제거하면 재교정됨.
    if (!/^corrector_quarantine:/m.test(txt)) { txt = txt.replace(/\nsearchable_text:/, '\ncorrector_quarantine: true\nsearchable_text:'); writeFileSync(md, txt); }
    console.log(`④ ${by} 재시도도 실패(${fails2.join(', ')}) — 격리(원본 유지 + corrector_quarantine 마커)`);
    process.exit(0);
  }
}

// ⑤ 적용 (검증 통과분만)
// 결정적 SSOT 보정: 리터럴 집합 중괄호 {1,2,3} → \{1,2,3\} (KaTeX 에서 { } 는 그룹화라 안 보임).
//   그룹화 중괄호(_{2n}·^{}·\frac{}{}·\begin{cases}·]{})는 보존. LLM 의존 없이 코드로 SSOT 를 KaTeX-correct 하게.
function escSetBraces(t) {
  // {{FIGn}}·{{INLn}}·{{TABLEn}}·{{BOXn_START/END}} placeholder 보호(escape 금지 — reconstruct.ts 매칭이 깨진다)
  const ph = []; t = t.replace(/\{\{(?:(?:FIG|INL|TABLE)\d+|BOX\d+_(?:START|END))\}\}/g, (m) => { ph.push(m); return `@@PH${ph.length - 1}@@`; });
  const out = []; const stack = []; let lastGroupClose = false;
  for (let i = 0; i < t.length; i++) {
    const ch = t[i];
    if (ch === '{' && t[i - 1] !== '\\') {
      const prev = (t.slice(0, i).match(/(\S)\s*$/) || [, ''])[1];
      const grouping = /[_^a-zA-Z\]]/.test(prev) || (prev === '}' && lastGroupClose);
      stack.push(!grouping); out.push(grouping ? '{' : '\\{');
    } else if (ch === '}' && t[i - 1] !== '\\') {
      const lit = stack.length ? stack.pop() : false; lastGroupClose = !lit; out.push(lit ? '\\}' : '}');
    } else out.push(ch);
  }
  return out.join('').replace(/@@PH(\d+)@@/g, (_, i) => ph[+i]);
}
parsed.corrected = escSetBraces(parsed.corrected);
const block = 'searchable_text: |\n' + parsed.corrected.split('\n').map((l) => '  ' + l).join('\n') + '\n';
txt = txt.slice(0, m.index + 1) + block + txt.slice(m.index + m[0].length);
txt = txt.replace(/\ncorrector_fixes:(?:\n  - .*)*(?=\n)/, '');
txt = txt.replace(/\ncorrector_by:.*(?=\n)/, '');
if (parsed.fixes.length) {
  const fb = '\ncorrector_fixes:\n' + parsed.fixes.map((x) => '  - ' + JSON.stringify(String(x))).join('\n');
  txt = txt.replace(/\nsearchable_text:/, fb + '\nsearchable_text:');
}
if (!/^corrector_by:/m.test(txt)) txt = txt.replace(/\nsearchable_text:/, `\ncorrector_by: ${by}\nsearchable_text:`);
if (!/^corrector_done:/m.test(txt)) txt = txt.replace(/\nsearchable_text:/, '\ncorrector_done: true\nsearchable_text:');
txt = txt.replace(/\ncorrector_quarantine: true(?=\n)/, '');  // ★재교정 성공 → 격리 마커 해제(stale 방지)
writeFileSync(md, txt);
const _sec = ((Date.now() - t0) / 1000).toFixed(1);
console.log(`⑤ 교정 적용(${by}, ${_sec}s) — fixes ${parsed.fixes.length}건${parsed.fixes.length ? ': ' + parsed.fixes.join(' / ') : ' (변경 없음)'}`);
// ★변경내역 로깅: 교정 전(st) ↔ 후 객관적 line diff 를 전용 로그에 — LLM 자기보고(fixes)와 별개로 '실제 무엇이 바뀌었나' 가시화.
try {
  const DLOG = '/tmp/ingest_logs/corrector_diff.log';
  const oldL = st.split('\n').map((s) => s.trim()).filter(Boolean);
  const newL = parsed.corrected.split('\n').map((s) => s.trim()).filter(Boolean);
  const oldS = new Set(oldL), newS = new Set(newL);
  const removed = oldL.filter((l) => !newS.has(l)), added = newL.filter((l) => !oldS.has(l));
  const hdr = `\n=== ${round}_${subj}_${num} [${by}, ${_sec}s] ${new Date().toISOString()} ===`;
  if (removed.length || added.length) {
    const d = [hdr, ...removed.slice(0, 15).map((l) => '- ' + l.slice(0, 160)), ...added.slice(0, 15).map((l) => '+ ' + l.slice(0, 160))];
    appendFileSync(DLOG, d.join('\n') + '\n');
    console.log(`   변경: -${removed.length}/+${added.length} 줄 (→ ${DLOG})`);
  } else {
    appendFileSync(DLOG, hdr + '\n(텍스트 변경 없음 — 이미 동일)\n');
  }
} catch (e) { /* 로깅 실패는 교정에 영향 없음 */ }
