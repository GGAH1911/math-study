#!/usr/bin/env node
// 오개념 목록 **적대적 검증** (claude -p, 구독).
//   생성은 DeepSeek(저가·배치)이 하지만 이 텍스트는 **튜터의 입으로 그대로 나간다** — 위젯처럼
//   기계 게이트가 없으므로 사람 대신 강모델이 항목 단위로 기각한다. **기본값은 거부.**
//   (개념 dedup 때 얻은 교훈: 생성형 LLM 산출물은 과생성·과병합이 많아 반드시 적대적 검증.)
//
// 항목별 판정: 수학적으로 정확한가 · 진짜 흔한 오개념인가(지어낸 것 아닌가) · 교정법이 실제로 통하는가.
// 하나라도 어긋나면 reject. 통과분만 verified:true 로 남긴다.
//
// 사용: node web/scripts/misconception_verify.mjs [--model opus]
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const DIR = `${REPO}/web/src/data/concept-misconceptions`;
const CDIR = `${REPO}/docs/concepts`;
const CLEAN = '/tmp/claude_p_clean';
try { mkdirSync(CLEAN, { recursive: true }); } catch { /* 있음 */ }
const A = process.argv.slice(2);
const MODEL = A.includes('--model') ? A[A.indexOf('--model') + 1] : 'opus';

function bodyOf(id) {
  for (const c of [`${CDIR}/${id}.md`, `${CDIR}/${id.normalize('NFD')}.md`, `${CDIR}/${id.normalize('NFC')}.md`]) {
    if (existsSync(c)) { const m = readFileSync(c, 'utf8').match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/); if (m) return m[1].trim().slice(0, 2500); }
  }
  return '';
}

const RUBRIC = `너는 한국 수학 교육 내용을 감수하는 엄격한 검수자다. 아래는 어떤 개념에 대해 자동 생성된
**오개념 목록**이고, 이건 그대로 AI 튜터의 프롬프트에 들어가 학생에게 말해질 것이다. 틀린 게 섞이면
튜터가 확신을 갖고 잘못 가르친다. **기본값은 거부(reject)** 로 두고, 확실한 것만 통과시켜라.

각 항목을 셋으로 본다:
1. accurate — why_wrong 과 fix 의 **수학적 내용이 정확한가**. 부분적으로만 맞거나 중요한 조건이 빠졌으면 거부.
   (예: 0.245454...를 245/999 로 고치라 하면서 분모를 990 이 아닌 99 로 안내 → 거부)
2. real — 한국 교육과정에서 **실제로 흔한** 오개념인가. 그럴듯하게 지어낸 것이거나, 이 개념에 특유하지
   않은 일반론("계산 실수")이면 거부.
3. useful — fix 가 학생이 스스로 깨닫게 하는 방식인가. 그냥 정답 통보면 감점하되 거부까지는 아니다.

출력은 JSON 하나만(코드펜스 없이):
{"verdicts":[{"index":0,"verdict":"pass"|"reject","reason":"한 줄","corrected":"거부지만 고치면 살릴 수 있으면 수정본 why_wrong/fix 를 한 문장으로, 아니면 null"}]}
index 는 주어진 항목 순서(0부터).`;

function ask(prompt) {
  return new Promise((res) => {
    const c = spawn('claude', ['-p', prompt, '--model', MODEL, '--output-format', 'json', '--tools', ''], {
      stdio: ['ignore', 'pipe', 'ignore'], cwd: CLEAN, timeout: 300000,
      env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' },
    });
    let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => {
      let text = out;
      try { const j = JSON.parse(out); if (j.is_error) { console.error(`검증 실패: ${String(j.result).slice(0, 70)}`); return res(null); } text = j.result || out; } catch { /* raw */ }
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) return res(null);
      try { res(JSON.parse(m[0])); } catch { res(null); }
    });
    c.on('error', () => res(null));
  });
}

const files = readdirSync(DIR).filter((f) => f.endsWith('.json'));
let totIn = 0, totPass = 0;
for (const f of files) {
  const d = JSON.parse(readFileSync(`${DIR}/${f}`, 'utf8'));
  const items = d.items || [];
  totIn += items.length;
  const listed = items.map((x, i) => `[${i}] 학생말: "${x.belief}"\n    why_wrong: ${x.why_wrong}\n    fix: ${x.fix}`).join('\n\n');
  const v = await ask(`${RUBRIC}\n\n--- 개념: ${d.id} ---\n${bodyOf(d.id)}\n\n--- 검수 대상 항목 ---\n${listed}`);
  if (!v?.verdicts) { console.log(`? ${d.id.split('/').pop()} 검증 실패 — 보류(verified 안 붙임)`); continue; }
  const keep = [], drop = [];
  for (const vd of v.verdicts) {
    const it = items[vd.index];
    if (!it) continue;
    if (vd.verdict === 'pass') keep.push(it); else drop.push({ ...it, reason: vd.reason, corrected: vd.corrected });
  }
  totPass += keep.length;
  writeFileSync(`${DIR}/${f}`, JSON.stringify({ ...d, verified: true, verifiedBy: MODEL, items: keep, rejected: drop }, null, 1));
  console.log(`${d.id.split('/').pop()?.padEnd(22)} 통과 ${keep.length}/${items.length}`);
  for (const r of drop) console.log(`   ✗ "${r.belief.slice(0, 46)}" — ${String(r.reason).slice(0, 84)}`);
}
console.log(`\n총 ${totPass}/${totIn} 통과 (심판 ${MODEL} · 구독)`);
