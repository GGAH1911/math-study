#!/usr/bin/env node
// sonnet 검증 — 교정된 searchable_text를 이미지와 대조해 "놓침·환각"을 탐지(교정 X, 평가만).
//   corrector(gemma/haiku)는 결정적 게이트만 통과 → 텍스트 정확도(의미·철자)는 이 단계가 본다.
//   결과는 corrector_verify(ok/issues) frontmatter + raw 로그(verify_corrected.log)에 누적.
// 사용: node verify_corrected.mjs <round> <subj> <num>
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';

const REPO = process.env.MATHSTUDY_ROOT || new URL('../..', import.meta.url).pathname.replace(/\/$/, '');  // ★레포 위치 자동(이동 내성)
const VLOG = '/tmp/ingest_logs/verify_corrected.log';
// ★프롬프트 캐싱 위생: clean cwd(벨트) + DISABLE_GIT(멜빵). 이미지는 --add-dir(절대경로)라 cwd 무관.
const CLEAN_DIR = process.env.CLAUDE_P_CWD || '/tmp/claude_p_clean';
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

function claudeCall(prompt, imgDir, model = 'sonnet') {
  return new Promise((res) => {
    const c = spawn('claude', ['-p', prompt, '--model', model, '--output-format', 'json', '--add-dir', imgDir], { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    c.stdout.setEncoding('utf8'); let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => { try { res(JSON.parse(out).result || ''); } catch { res(''); } });
  });
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
if (!round) { console.log('사용: node verify_corrected.mjs <round> <subj> <num>'); process.exit(1); }
const md = findMd(round, subj, num);
if (!md) { console.log('md 못찾음'); process.exit(1); }
let txt = readFileSync(md, 'utf8');
const m = txt.match(/\nsearchable_text: \|\n((?:  .*\n?)*)/);
if (!m) { console.log('searchable_text 없음'); process.exit(1); }
const st = m[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join('\n').trim();
const n2 = String(num).padStart(2, '0');
const imgDir = `${REPO}/db/raw/${round}/images`;
const img = `${round}_${subj}_${n2}.png`;

const prompt = `${imgDir}/${img} 파일을 Read 도구로 열어, 이미지의 수능 수학 문제와 아래 "전사 텍스트"를 한 글자씩 대조하라.
- 놓침: 이미지엔 있는데 전사에서 빠지거나 틀린 것(수식 기호·숫자·보기 ①~⑤·첨자·한글 오타).
- 환각: 전사엔 있는데 이미지엔 없는 것.
{{FIG0}}·{{TABLE0}} 같은 placeholder는 그림/표 자리 표시이므로 그 안 내용은 평가 대상이 아니다(자리만 맞으면 OK).
출력은 JSON만(설명·코드펜스 없이):
{"ok": <놓침·환각 모두 없으면 true, 하나라도 있으면 false>, "issues": ["<구체적 문제 한 줄>", ...]}
--- 전사 텍스트 ---
${st}`;

const t0 = Date.now();
const out = await claudeCall(prompt, imgDir, process.env.VERIFY_MODEL || 'sonnet');
const sec = ((Date.now() - t0) / 1000).toFixed(1);
let res;
try {
  // sonnet 은 대개 유효 JSON(\\lim 처럼 이미 이스케이프됨)을 준다 → raw parse 먼저.
  //   무효 백슬래시 보정 replace 를 무조건 돌리면 정상 \\ 까지 \\\ 로 깨뜨려 parsefail 된다(verify_batch 와 동일 버그).
  const _jraw = (out.match(/\{[\s\S]*\}/) || [''])[0];
  try { res = JSON.parse(_jraw); }
  catch { res = JSON.parse(_jraw.replace(/\\(?!["\\/bfnrtu])/g, '\\\\')); }
} catch { res = { ok: null, issues: ['파싱실패:' + out.slice(0, 120)] }; }
const issues = Array.isArray(res.issues) ? res.issues : [];

// frontmatter: corrector_verify 갱신(ok / issues / parsefail)
txt = txt.replace(/\ncorrector_verify:.*(?=\n)/, '');
txt = txt.replace(/\ncorrector_verify_issues:(?:\n  - .*)*(?=\n)/, '');
const status = res.ok === true ? 'ok' : res.ok === false ? 'issues' : 'parsefail';
let fb = `\ncorrector_verify: ${status}`;
if (issues.length) fb += `\ncorrector_verify_issues:\n` + issues.map((x) => '  - ' + JSON.stringify(String(x))).join('\n');
txt = txt.replace(/\nsearchable_text:/, fb + '\nsearchable_text:');
writeFileSync(md, txt);

appendFileSync(VLOG, `${round}_${subj}_${n2}\t${sec}s\tok=${res.ok}\t${issues.join(' | ')}\n`);
console.log(`검증(${sec}s) ok=${res.ok}${issues.length ? ' — ' + issues.join(' / ') : ''}`);
