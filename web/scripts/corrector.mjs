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
// claude(Sonnet) = --output-format json → {result:"..."} 래퍼. 자가치유용(별도 백엔드·쿼터).
function claudeCall(prompt, imgDir, model = 'sonnet') {
  return new Promise((res) => {
    const c = spawn('claude', ['-p', prompt, '--model', model, '--output-format', 'json', '--add-dir', imgDir], { stdio: ['ignore', 'pipe', 'pipe'] });
    c.stdout.setEncoding('utf8'); let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => { try { res(JSON.parse(out).result || ''); } catch { res(''); } });
  });
}
// 마커 파싱 + sanitize($ 델리미터·제어문자 제거).
function parseCorrected(out) {
  const cm = out.match(/===CORRECTED===\r?\n([\s\S]*?)\r?\n===END===/);
  if (!cm) return null;
  const corrected = cm[1].replace(/\$/g, '').replace(/[\x00-\x09\x0b-\x1f]/g, '').replace(/[ \t]+$/gm, '');
  const fmFix = out.match(/===FIXES===\r?\n([\s\S]*?)\r?\n===CORRECTED===/);
  const fixes = fmFix ? fmFix[1].split('\n').map((l) => l.replace(/^\s*-\s*/, '').trim()).filter(Boolean) : [];
  return { corrected, fixes };
}
// 검증 게이트 — 실패 사유 배열(빈 배열=통과).
const PH = (s) => (s.match(/\{\{(?:FIG|TABLE)\d+\}\}/g) || []).sort().join(',');
function validate(corrected, st) {
  const f = [];
  if (!corrected || !corrected.trim()) return ['빈출력'];
  if (/[\x00-\x09\x0b-\x1f]/.test(corrected)) f.push('제어문자');       // YAML/서버 다운 차단
  if (PH(st) !== PH(corrected)) f.push(`placeholder(${PH(st)}→${PH(corrected)})`);
  const o = (corrected.match(/\{/g) || []).length, c = (corrected.match(/\}/g) || []).length;
  if (o !== c) f.push(`중괄호(${o}/${c})`);                              // LaTeX 균형
  const ratio = corrected.length / Math.max(1, st.length);
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
const img = `${imgDir}/${round}_${subj}_${num}.png`;
const prompt = `너는 한국 수능 기출의 전사 텍스트를 원본 이미지와 한 글자씩 대조해 교정한다.
아래 "추출 전사"는 PDF 텍스트레이어에서 뽑아 깨진 기호·오타·누락이 있을 수 있다. 이미지대로 정확히 교정하라(수식 기호·보기 ①~⑤·숫자 정확히). 환각 금지 — 이미지에 있는 그대로.
★수식: LaTeX 명령(\\frac, \\overline, \\sqrt 등)은 쓰되 **$...$ 델리미터로 감싸지 마라**. 렌더러가 한글/수식을 자동 분리한다 — $ 를 넣으면 KaTeX가 깨진다.
★★전사에 {{FIG0}}·{{TABLE0}} 형태의 placeholder가 **이미 있으면** 그 자리·개수 그대로 두라(그림/표 자리). ★단, 전사에 없는 placeholder를 **새로 만들지 마라** — 이미지에 그림/표가 보여도 placeholder를 추가하지 말고, 전사에 있는 텍스트만 교정하라.
★★placeholder가 가리키는 그림·표·(가)(나) 박스의 **내용을 본문 텍스트로 다시 쓰지 마라**. placeholder 토큰만 남기고 그 내용은 중복 서술 금지(렌더 시 그림/표로 대체되므로 본문에 또 있으면 이중 노출됨).
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

// ② claude(Sonnet) 교정 → ③ 검증. (agy는 토큰 쿼터 한계로 1차에서 폐기 — 25콜에 소진.)
console.log('② claude(Haiku) 교정…');
const out = await claudeCall(prompt, imgDir, 'haiku');  // 1차 = haiku(쿼터 절약). 검증 실패 시만 sonnet 자가치유.
if (!out.trim()) { console.log('claude 빈출력(한도/에러) — ①결정론만 반영'); process.exit(3); }  // exit 3 = 한도(배치 멈춤)
let parsed = parseCorrected(out);
if (!parsed && process.env.CORR_DEBUG) console.error('[DEBUG] claude 마커 파싱 실패. out 앞 600자:\n' + out.slice(0, 600) + '\n---끝---');
let fails = parsed ? validate(parsed.corrected, st) : ['파싱실패'];
let by = 'haiku';

// ④ 자가치유: 검증 실패 → claude 재교정 → 재검증 (1차와 동일 백엔드지만 재시도로 일시 오류 흡수)
if (fails.length) {
  console.log(`③ claude 검증 실패(${fails.join(', ')}) → ④ claude 자가치유 재시도…`);
  const out2 = await claudeCall(prompt, imgDir);
  const parsed2 = parseCorrected(out2);
  const fails2 = parsed2 ? validate(parsed2.corrected, st) : ['파싱실패'];
  if (!fails2.length) { parsed = parsed2; fails = []; by = 'sonnet'; console.log('④ claude 자가치유 통과'); }
  else {
    mkdirSync(dirname(QLOG), { recursive: true });
    appendFileSync(QLOG, `${round}_${subj}_${num}\t1차:${fails.join('|')}\t재시도:${fails2.join('|')}\n`);
    // 영구 격리 마커(반복 재시도·쿼터 낭비 차단) — 원인 수정 후 수동으로 corrector_quarantine 제거하면 재교정됨.
    if (!/^corrector_quarantine:/m.test(txt)) { txt = txt.replace(/\nsearchable_text:/, '\ncorrector_quarantine: true\nsearchable_text:'); writeFileSync(md, txt); }
    console.log(`④ Sonnet도 실패(${fails2.join(', ')}) — 격리(원본 유지 + corrector_quarantine 마커)`);
    process.exit(0);
  }
}

// ⑤ 적용 (검증 통과분만)
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
writeFileSync(md, txt);
console.log(`⑤ 교정 적용(${by}) — 검증 통과 · fixes ${parsed.fixes.length}건`);
