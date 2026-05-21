#!/usr/bin/env node
// 28번 다단 작도의 end-to-end 흐름 검증:
//   Turn 1: /api/chat → assistantText1 (python block 포함)
//   Turn 2: /api/sympy 실행 → stdout (VERIFY OK 기대)
//   Turn 3: /api/chat ([자동 계산 결과] inject) → geometry block
//   Turn 4: /api/chat ([시각 검증] inject) → [검증 통과] 또는 수정 spec
//
// 사용: cd web && node scripts/test-flow-28.mjs

const BASE = process.env.BASE ?? 'http://127.0.0.1:4321';
const SLUG = '2022_6월모평_미적분_28';
const COLL = 'problems';
const MODEL = 'haiku';

async function callChat(messages) {
  const res = await fetch(`${BASE}/api/chat`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ slug: SLUG, collection: COLL, messages, model: MODEL }),
  });
  if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = '', out = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf('\n\n')) !== -1) {
      const block = buf.slice(0, idx); buf = buf.slice(idx + 2);
      let event = 'message', data = '';
      for (const line of block.split('\n')) {
        if (line.startsWith('event: ')) event = line.slice(7).trim();
        else if (line.startsWith('data: ')) data = line.slice(6);
      }
      if (!data) continue;
      try {
        const parsed = JSON.parse(data);
        if (event === 'delta' && typeof parsed.text === 'string') out += parsed.text;
      } catch { /* ignore */ }
    }
  }
  return out;
}

async function runSympy(code) {
  const res = await fetch(`${BASE}/api/sympy`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });
  return await res.json();
}

function summary(text, max = 800) {
  if (text.length <= max) return text;
  return text.slice(0, max) + `\n... (+${text.length - max} chars)`;
}

console.log('=== Turn 1: 초기 도형 요청 ===');
const messages = [{ role: 'user', content: '이 문제의 도형을 그려줘.' }];
const t1 = await callChat(messages);
console.log(summary(t1));
console.log();

const pyMatch = t1.match(/```(?:python|py|sympy)\s*\n([\s\S]*?)```/);
if (!pyMatch) {
  console.log('❌ FAIL: Turn 1 응답에 python block 없음. LLM 이 GRAPHICS_GUIDE 의 STEP B 를 따르지 않음.');
  process.exit(1);
}
const code = pyMatch[1];
console.log('=== Turn 2: sympy 자동 실행 ===');
const sj = await runSympy(code);
const stdout = (sj.ok ? sj.stdout : (sj.stderr || sj.error || `exit ${sj.exit_code}`)).trim();
console.log('ok:', sj.ok);
console.log('stdout:');
console.log(stdout);
console.log();

const failed = /\[VERIFY FAIL\]/.test(stdout);
const okCount = (stdout.match(/\[VERIFY OK\]/g) ?? []).length;
const failCount = (stdout.match(/\[VERIFY FAIL\]/g) ?? []).length;
console.log(`VERIFY OK ×${okCount}, FAIL ×${failCount}`);
console.log();

if (failed) {
  console.log('⚠ VERIFY FAIL 감지 — Stage 1 retry 시뮬레이션');
}

console.log('=== Turn 3: [자동 계산 결과] inject → geometry emit ===');
const prefix = failed ? '[자동 계산 결과 — 검증 실패]' : '[자동 계산 결과]';
const tail = failed
  ? '\n\n위 출력에 `[VERIFY FAIL]` 항목이 있다. **이전 가정/수식이 어디서 틀렸는지** 찾아 단계 정의를 다시 읽고 sympy 코드를 다시 작성해 재계산하라. 추정 금지.'
  : '\n\n위 출력의 각 점 좌표를 **글자 그대로 ```geometry``` spec 의 `at: [x, y]` 에 옮겨 적어라**. 추정·반올림 금지. 이번 응답에서 바로 geometry block 작성, 대기 메시지 금지, 기술 용어 노출 금지.';
const injected = `${prefix}\n\`\`\`\n${stdout}\n\`\`\`${tail}`;
const messages3 = [
  ...messages,
  { role: 'assistant', content: t1 },
  { role: 'user', content: injected },
];
const t3 = await callChat(messages3);
console.log(summary(t3));
console.log();

const geomMatch = t3.match(/```geometry\s*\n([\s\S]*?)```/);
if (!geomMatch) {
  console.log('❌ FAIL: Turn 3 응답에 geometry block 없음.');
  console.log(`(t3 length=${t3.length})`);
  process.exit(1);
}
const specStr = geomMatch[1].trim();
let spec;
try { spec = JSON.parse(specStr); }
catch (e) {
  console.log('❌ FAIL: geometry spec JSON parse 실패:', e.message);
  console.log(specStr.slice(0, 500));
  process.exit(1);
}
console.log(`✓ geometry spec: shapes=${spec.shapes?.length}, points=${spec.shapes?.filter(s=>s.type==='point').length}`);
console.log();

console.log('=== Turn 4: [시각 검증] inject ===');
const checkMsg = [
  '[시각 검증]',
  '방금 emit 한 geometry spec:',
  '```json',
  specStr,
  '```',
  '',
  '원본 문제 도형 이미지를 Read 로 다시 본 뒤, 위 spec 으로 그릴 도형이',
  '이미지와 **구조적으로 일치하는지** 확인:',
  '- 점 개수·라벨 일치?',
  '- 선·곡선의 연결 관계 (어느 점이 어느 선·호 위인지) 일치?',
  '- 곡선 종류 (타원 vs 원 vs 쌍곡선) 일치?',
  '',
  '전부 일치하면 정확히 `[검증 통과]` 한 줄만 응답.',
  '어긋남이 있으면:',
  '1. 어긋난 항목 1-2 bullet',
  '2. 수정된 ```geometry``` 블록 전체 다시 emit',
].join('\n');
const messages4 = [
  ...messages3,
  { role: 'assistant', content: t3 },
  { role: 'user', content: checkMsg },
];
const t4 = await callChat(messages4);
console.log(summary(t4, 1500));
console.log();

if (t4.trim() === '[검증 통과]') {
  console.log('✓ [검증 통과] — visual check 통과');
} else if (/```geometry/.test(t4)) {
  console.log('✏ 수정 spec emit — visual check 가 어긋남 감지');
} else {
  console.log('⚠ 예상 외 응답');
}
