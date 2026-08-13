#!/usr/bin/env node
// 비전 **판독력만** 따로 채점 — 정답 정확도는 '읽기 + 추론 + 출력형식'이 뒤섞여 있어 읽기를 못 잰다.
//   실제로 llama4-scout 은 문제를 정확히 읽고도 JSON 을 안 지켜 '전사 0자'로 집계됐다.
//   여기선 모델이 뱉은 **아무 텍스트나**(JSON 전사든 산문이든) 원본 본문과 대조해 판독 충실도만 본다.
//
// ★기준은 DB 본문이 아니라 **원본 이미지**다. text_markdown 을 기준으로 삼았다가 두 번 데였다:
//   ① (year,session,subject,number) 키가 고1/고2 사이에서 충돌해 엉뚱한 문제 본문을 기준으로 씀
//   ② 키를 고쳐도 DB 본문 자체에 오류가 있었다(이미지는 'y축과 만나는 점 B'인데 DB는 'x축').
//   그래서 심판에게 타일 이미지를 직접 보여준다(심판은 비전 모델). 기준의 품질에 결과가 매이지 않는다.
//
// 채점 기준은 튜터에 필요한 것 — 식·숫자·조건·보기를 **틀리게 읽지 않았는가**.
//   누락(안 쓴 것)보다 **오독(다르게 읽은 것)** 을 훨씬 무겁게 본다: 튜터가 학생 풀이를 오독하면
//   틀린 지도를 확신 있게 하게 되고, 그건 아예 못 읽는 것보다 해롭다.
// 사용: NOUS_API_KEY=... node web/scripts/vision_read_judge.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const MON = `${REPO}/.llm-monitor`;
// ★심판은 **구독(claude -p)**. 포털은 제품 튜터 전용이다.
//   비전 채점이라 심판이 원본 이미지를 봐야 하는데, claude CLI 는 --add-dir 로 디렉터리를 열어주고
//   Read 도구로 직접 읽게 하면 된다(제품 문제 페이지 튜터와 동일한 메커니즘).
const JUDGES = (process.env.JUDGES || 'opus,sonnet').split(',');
const CLEAN = '/tmp/claude_p_clean';
try { mkdirSync(CLEAN, { recursive: true }); } catch { /* 이미 있음 */ }

const results = JSON.parse(readFileSync(`${MON}/vision_results.json`, 'utf8'));
const SET = JSON.parse(readFileSync(`${MON}/vision_set.json`, 'utf8'));
const TILES = Object.fromEntries(SET.map((x) => [x.id, x.tiles]));
const HOST_REPO = '/home/insung/math-study';
const localize = (p) => (p.startsWith(HOST_REPO) && REPO !== HOST_REPO ? REPO + p.slice(HOST_REPO.length) : p);

const RUBRIC = `너는 OCR/판독 충실도를 채점한다. **Read 도구로 열어 볼 이미지가 원본 문제**다(이것이 유일한 정답 기준).
아래는 여러 모델이 그 이미지를 보고 옮겨 적은 것이다. 모델이 누구인지는 모른다(라벨 무작위).
먼저 이미지를 스스로 정확히 읽은 뒤, 각 응답을 이미지와 대조하라.

각 응답을 채점(0-10):
- fidelity: 식·숫자·첨자·지수·부호·조건을 정확히 읽었는가. **틀리게 읽은 것(오독)은 크게 감점.**
  안 쓴 것(누락)은 가볍게 감점. 표현이 달라도 수학적으로 같으면 감점 없음.
- figure: 그림/도형이 있는 문제라면 그림의 내용(도형 종류·표시된 값·위치관계)을 옳게 서술했는가.
  원본에 그림 언급이 없으면 5점(중립)으로 둔다.
- 응답이 JSON 이 아니라 산문이어도 **형식은 채점하지 마라** — 오직 읽어낸 내용만 본다.

misreads: 구체적으로 틀리게 읽은 항목을 배열로 나열하라(예 "a_{12} 를 a_{21} 로 읽음", "-8 을 8 로 읽음").
없으면 빈 배열.

출력은 JSON 하나만:
{"scores":{"<라벨>":{"fidelity":n,"figure":n,"misreads":["..."],"note":"한 줄"}}}`;

function judge(prompt, model, imgPaths) {
  return new Promise((res) => {
    const local = imgPaths.map(localize);
    const dirs = [...new Set(local.map((p) => p.replace(/\/[^/]+$/, '')))];
    const withImgs = `${prompt}\n\n--- 원본 이미지 (Read 도구로 먼저 열어 볼 것) ---\n${local.map((p, i) => `  ${i + 1}. ${p}`).join('\n')}`;
    const args = ['-p', withImgs, '--model', model, '--output-format', 'json',
      '--allowedTools', 'Read', '--disallowedTools', 'Bash,Edit,Write,Glob,Grep,WebFetch,WebSearch',
      '--max-turns', '8'];
    for (const d of dirs) args.push('--add-dir', d);
    const c = spawn('claude', args, {
      stdio: ['ignore', 'pipe', 'ignore'], cwd: CLEAN, timeout: 420000,
      env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' },
    });
    let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => {
      let text = out;
      try { const j = JSON.parse(out); if (j.is_error) { console.error(`심판 ${model}: ${String(j.result).slice(0, 80)}`); return res(null); } text = j.result || out; } catch { /* raw */ }
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) return res(null);
      try { res(JSON.parse(m[0])); } catch { res(null); }
    });
    c.on('error', () => res(null));
  });
}

function shuffled(arr, seed) {
  const a = [...arr]; let s = seed * 9301 + 49297;
  for (let i = a.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor((s / 233280) * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

// 모델이 뱉은 '읽은 내용'을 형식 불문하고 회수한다(JSON 전사 우선, 없으면 산문 raw).
const readingOf = (r) => ((r.transcription || '').trim() || (r.raw || '').trim());

const byProb = new Map();
for (const r of results) {
  if (r.error) continue;
  const t = readingOf(r);
  if (!t) continue;
  if (!byProb.has(r.id)) byProb.set(r.id, []);
  byProb.get(r.id).push({ cand: r.cand, text: t });
}

const LETTERS = 'ABCDEFGH';
const out = [];
const items = [...byProb.entries()];
let qi = 0;
async function worker() {
  while (qi < items.length) {
    const i = qi++;
    const [id, rs] = items[i];
    const tiles = TILES[id];
    if (!tiles?.length) { console.log(`타일 없음 ${id}`); continue; }
    const order = shuffled(rs, i + 1);
    const map = {};
    const blocks = order.map((r, n) => { const L = LETTERS[n]; map[L] = r.cand; return `### 응답 ${L}\n${r.text.slice(0, 4000)}`; }).join('\n\n');
    const prompt = `${RUBRIC}\n\n--- 모델들이 이 이미지를 보고 옮긴 것 ---\n${blocks}`;
    const vs = await Promise.all(JUDGES.map((j) => judge(prompt, j, tiles).then((v) => ({ judge: j, v }))));
    for (const { judge: jm, v } of vs) if (v) out.push({ id, map, judge: jm, verdict: v });
    console.log(`[${i + 1}/${items.length}] ${id.padEnd(28)} 응답 ${rs.length}개 채점`);
  }
}
await Promise.all(Array.from({ length: 3 }, worker));
writeFileSync(`${MON}/vision_read_judged.json`, JSON.stringify(out, null, 1));

const agg = {};
for (const o of out) {
  for (const [L, cand] of Object.entries(o.map)) {
    const s = o.verdict.scores?.[L]; if (!s) continue;
    agg[cand] ??= { n: 0, fid: 0, fig: 0, mis: 0, misList: [] };
    agg[cand].n++;
    agg[cand].fid += Number(s.fidelity) || 0;
    agg[cand].fig += Number(s.figure) || 0;
    const ms = Array.isArray(s.misreads) ? s.misreads : [];
    agg[cand].mis += ms.length;
    for (const m of ms.slice(0, 2)) agg[cand].misList.push(`${o.id}: ${m}`);
  }
}
// 시도 대비 커버리지(응답 자체가 없던 건 판독 실패로 남긴다)
const attempted = {}, produced = {};
for (const r of results) { attempted[r.cand] = (attempted[r.cand] || 0) + 1; if (!r.error && readingOf(r)) produced[r.cand] = (produced[r.cand] || 0) + 1; }

console.log('\n── 판독 충실도 (블라인드, 심판 2명 · 형식 무관) ──');
console.log('모델'.padEnd(15) + '충실도  그림   오독수  판독시도  ');
const rows = Object.entries(agg).map(([c, a]) => ({
  cand: c, fid: a.fid / a.n, fig: a.fig / a.n, mis: a.mis / a.n,
  cover: `${produced[c] || 0}/${attempted[c] || 0}`, misList: a.misList,
})).sort((x, y) => y.fid - x.fid);
for (const r of rows) console.log(`${r.cand.padEnd(15)}${r.fid.toFixed(1).padStart(5)}${r.fig.toFixed(1).padStart(7)}${r.mis.toFixed(1).padStart(8)}${r.cover.padStart(9)}`);
console.log('\n── 대표 오독 ──');
for (const r of rows) { if (r.misList.length) console.log(`[${r.cand}] ${r.misList.slice(0, 3).join(' / ')}`); }
writeFileSync(`${MON}/vision_read_summary.json`, JSON.stringify(rows, null, 1));
