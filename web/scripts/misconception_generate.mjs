#!/usr/bin/env node
// 개념별 **오개념 목록** 생성 (DeepSeek V4 Flash, Nous Portal).
//   튜터 프롬프트에 주입해 "학생이 흔히 여기서 이렇게 잘못 이해한다"를 미리 알려준다.
//   지도력(pedagogy) 점수가 전 모델에서 가장 낮았던 항목이라, 그 지점을 캐시로 보강하는 시도.
//
// ★위젯 생성과 결정적으로 다른 점: **기계 검증기가 없다.** 위젯은 수학게이트(불변식·오라클)가
//   틀린 걸 걸러내지만, 오개념 텍스트는 그대로 튜터의 입으로 나간다. 잘못 지어내면 학습 내용을
//   오염시킨다 → 생성은 저가 모델로, **검증은 반드시 구독(misconception_verify.mjs)** 으로 나눈다.
// ★재료: 개념 본문 + **실제 학생 대화 발췌**(있으면). 상상하게 하지 말고 실물에서 캐는 쪽이 정확하다.
//
// 사용: NOUS_API_KEY=... node web/scripts/misconception_generate.mjs <conceptId> [...]
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const CDIR = `${REPO}/docs/concepts`;
const OUT = `${REPO}/web/src/data/concept-misconceptions`;
const MON = `${REPO}/.llm-monitor`;
for (const d of [OUT, MON]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const emit = (o) => { try { appendFileSync(`${MON}/events.ndjson`, JSON.stringify({ t: Date.now(), ...o }) + '\n'); } catch { /* */ } };

const KEY = process.env.NOUS_API_KEY;
if (!KEY) { console.error('NOUS_API_KEY 없음'); process.exit(1); }
const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';
const MODEL = process.env.NOUS_MODEL || '~deepseek/deepseek-v4-flash-latest';
const safe = (id) => id.replace(/\//g, '__');

// 실제 학생 대화에서 이 개념 관련 발췌 — DB 덤프(선택). 없으면 본문만으로 생성.
let TRANSCRIPTS = {};
try { TRANSCRIPTS = JSON.parse(readFileSync(`${MON}/transcripts_by_slug.json`, 'utf8')); } catch { /* 없으면 스킵 */ }

function bodyOf(id) {
  for (const c of [`${CDIR}/${id}.md`, `${CDIR}/${id.normalize('NFD')}.md`, `${CDIR}/${id.normalize('NFC')}.md`]) {
    if (existsSync(c)) { const m = readFileSync(c, 'utf8').match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/); if (m) return m[1].trim().slice(0, 3000); }
  }
  return '';
}

const HEAD = `**Reasoning language: English ONLY.** 사용자에게 보이는 출력(JSON 안의 한국어 필드)만 한국어로 쓴다.

너는 한국 수능 수학 교육 전문가다. 아래 개념에서 **학생이 실제로 자주 걸려 넘어지는 오개념**을 뽑아라.

지켜야 할 것:
- **지어내지 마라.** 한국 교육과정에서 실제로 관찰되는 것만. 확신이 없으면 개수를 줄여라(3개도 좋다).
- 각 항목은 **학생이 실제로 할 법한 말**로 쓴다("극한은 결국 그 값에 도달한다는 뜻 아니야?"). 교과서 문장 말고.
- **왜 틀렸는지**를 한 줄로, 학생에게 바로 쓸 수 있는 말로 쓴다.
- **어떻게 교정할지**(반례·비유·질문)를 한 줄로. 답을 알려주는 게 아니라 학생이 스스로 깨닫게 하는 방식.
- 이 개념에 **특유한 것**만. "계산 실수를 한다" 같은 일반론 금지.
- **한국 고교 교육과정 범위 안**의 오개념만. 교육과정에 없는 소재(금융공학·연금현가계수·대학 수학 등)로
  가지 마라. 학생이 그런 질문을 했더라도 그건 그 학생 개인의 관심사지 일반적 오개념이 아니다.
- 실제 학생 대화가 주어지면 참고하되, **"이 학생만의 특이한 맥락인가, 누구나 걸리는 지점인가"를 먼저 판정**하라.
  누구나 걸리는 것만 채택한다. 개인 맥락이면 버려라 — 대화에 있다는 이유만으로 승격시키지 마라.
  (실패 사례: 한 학습자가 e 를 복리·연금과 엮어 물었다고 '연금현가계수 오개념'을 만들어 전량 기각됨)
- 어원·명명 유래처럼 **수학적 오류가 아닌 것**은 오개념이 아니다. 제외하라.

출력은 JSON 하나만(코드펜스 없이):
{"items":[{"belief":"학생이 할 법한 잘못된 말","why_wrong":"왜 틀렸는지 한 줄","fix":"교정 방법 한 줄","from_transcript":true/false}]}
항목은 3-6개.`;

async function gen(id) {
  const body = bodyOf(id);
  if (!body) return { id, ok: false, why: '본문없음' };
  const tr = (TRANSCRIPTS[id] || []).slice(0, 8);
  const trBlock = tr.length ? `\n\n--- 이 개념에서 실제 학생이 한 말 (최우선 근거) ---\n${tr.map((t) => `- ${t}`).join('\n')}` : '';
  emit({ ev: 'start', id: `misconception · ${id.split('/').pop()}`, model: MODEL });
  const t0 = Date.now();
  try {
    const r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: `${HEAD}\n\n--- 개념: ${id} ---\n${body}${trBlock}` }],
        response_format: { type: 'json_object' }, max_tokens: 20000,
      }),
    });
    if (!r.ok) { const w = `HTTP ${r.status}`; emit({ ev: 'done', id: `misconception · ${id.split('/').pop()}`, ok: false, why: w }); return { id, ok: false, why: w }; }
    const j = await r.json(); const u = j.usage || {};
    const txt = j.choices?.[0]?.message?.content || '';
    const m = txt.match(/\{[\s\S]*\}/);
    if (!m) return { id, ok: false, why: 'JSON 추출 실패' };
    const obj = JSON.parse(m[0]);
    const items = (obj.items || []).filter((x) => x?.belief && x?.why_wrong);
    if (!items.length) return { id, ok: false, why: '항목 없음' };
    writeFileSync(`${OUT}/${safe(id)}.json`, JSON.stringify({ id, model: MODEL, verified: false, items }, null, 1));
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    emit({ ev: 'done', id: `misconception · ${id.split('/').pop()}`, ok: true, secs: +secs, usage: u });
    return { id, ok: true, n: items.length, secs, cost: u.cost ?? 0, fromTr: items.filter((x) => x.from_transcript).length };
  } catch (e) { return { id, ok: false, why: e.message }; }
}

const ids = process.argv.slice(2).filter((a) => !a.startsWith('--'));
let cost = 0;
for (const id of ids) {
  const r = await gen(id);
  cost += r.cost || 0;
  console.log(r.ok
    ? `✓ ${id.split('/').pop()?.padEnd(22)} 항목 ${r.n} (대화근거 ${r.fromTr}) · ${r.secs}s · $${(r.cost ?? 0).toFixed(5)}`
    : `✗ ${id.split('/').pop()?.padEnd(22)} ${r.why}`);
}
console.log(`\n총 $${cost.toFixed(5)} → ${OUT} (검증 전 · misconception_verify.mjs 필요)`);
