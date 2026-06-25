#!/usr/bin/env node
// 개념 노드 인터랙티브 위젯 수요 서베이(파일럿). 함수/도형 정의 노드 → LLM 분류.
//   판정: 위젯 가치(Y/N)·상호작용(slider/drag/animate/none)·InteractiveSpec 적합(Y/partial/N)·한줄 스케치.
//   백엔드: --backend opus(claude -p 캐싱·1벌크) | gemma(맥북 gemma4 API·청크 2병렬).
// 사용: node web/scripts/widget_survey.mjs [--n 30] [--backend opus|gemma]
import { spawn } from 'node:child_process';
import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
const REPO = '/home/insung/Projects/math-study';
const CDIR = `${REPO}/docs/concepts`;
const A = process.argv.slice(2);
const N = parseInt((A[A.indexOf('--n') + 1]) || '30', 10);
const BACKEND = (A[A.indexOf('--backend') + 1]) || 'opus';
const CLEAN = '/tmp/claude_p_clean'; if (!existsSync(CLEAN)) mkdirSync(CLEAN, { recursive: true });
const GEMMA_URL = process.env.GEMMA_URL || 'http://100.79.230.49:8080/v1/chat/completions';
const GEMMA_MODEL = process.env.GEMMA_MODEL || 'mlx-community/gemma-4-26B-A4B-it-qat-4bit';

function walk(dir) { const out = []; for (const e of readdirSync(dir, { withFileTypes: true })) { const p = `${dir}/${e.name}`; if (e.isDirectory()) out.push(...walk(p)); else if (e.name.endsWith('.md')) out.push(p); } return out; }
function parseFile(p) {
  const raw = readFileSync(p, 'utf8');
  const fm = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/); if (!fm) return null;
  const domain = (fm[1].match(/^domain:\s*(.+)$/m) || [])[1]?.trim();
  const type = (fm[1].match(/^concept_type:\s*(.+)$/m) || [])[1]?.trim();
  const id = p.replace(`${CDIR}/`, '').replace(/\.md$/, '');
  return { id, domain, type, body: fm[2].replace(/\s+/g, ' ').trim().slice(0, 360) };
}
const all = walk(CDIR).map(parseFile).filter((c) => c && c.type === 'definition' && (c.domain === '함수' || c.domain === '도형') && c.body.length > 40);
const pick = (arr, k) => { const step = Math.max(1, Math.floor(arr.length / k)); return arr.filter((_, i) => i % step === 0).slice(0, k); };
const cands = [...pick(all.filter((c) => c.domain === '함수'), Math.ceil(N / 2)), ...pick(all.filter((c) => c.domain === '도형'), Math.floor(N / 2))];
console.log(`[${BACKEND}] 후보 ${all.length} 중 ${cands.length} 샘플`);

const HEAD = `너는 한국 수학 학습 시스템의 개념 노드가 "인터랙티브 시각화 위젯"으로 이득을 보는지 분류한다.
판단 핵심: 정적 그림으로 충분한가? 아니면 **값을 바꿔가며 탐구**(슬라이더로 파라미터 변화 → 도형/그래프 실시간 갱신)할 때 이해가 확연히 깊어지는가?
우리 인터랙티브 렌더러(InteractiveSpec) 표현 가능: 슬라이더 파라미터 + mathjs scope 계산 + Geometry(점·선·원·다각형, 좌표에 "=식") / Graph(함수 플롯) / 3D. **불가**: 자유 드로잉·물리시뮬·복잡 커스텀 애니메이션.
각 개념마다 정확히 한 줄, 파이프(|) 구분:
ID | 위젯가치(Y 또는 N) | 상호작용(slider/drag/animate/none) | InteractiveSpec적합(Y/partial/N) | 한줄스케치
설명·머리말 없이 줄만 출력.\n\n개념들:\n`;
const promptFor = (subset) => HEAD + subset.map((c) => `[${c.id}] (${c.domain}) ${c.body}`).join('\n');

function rowsOf(text) { return text.split('\n').map((l) => l.trim()).filter((l) => (l.match(/\|/g) || []).length >= 3).map((l) => l.replace(/^[-*\d.\s]+/, '').split('|').map((x) => x.trim())); }
function aggregate(rows, meta) {
  const Y = (s) => (s || '').toUpperCase().startsWith('Y');
  const valY = rows.filter((r) => Y(r[1]));
  const fit = (s) => { const u = (s || '').toUpperCase(); return u === 'Y' ? 'Y' : u.startsWith('PART') ? 'partial' : 'N'; };
  const fy = valY.filter((r) => fit(r[3]) === 'Y'), fp = valY.filter((r) => fit(r[3]) === 'partial'), fn = valY.filter((r) => fit(r[3]) === 'N');
  const types = {}; for (const r of valY) { const t = (r[2] || '?').toLowerCase().split(/[\s,/]/)[0]; types[t] = (types[t] || 0) + 1; }
  return [
    `══ 위젯 수요 서베이 [${meta.backend}] (${rows.length}노드, 함수/도형 정의) ══  ${meta.info}`,
    ``,
    `▶ 위젯 가치 있음: ${valY.length}/${rows.length} (${rows.length ? Math.round(valY.length / rows.length * 100) : 0}%)`,
    `▶ InteractiveSpec 적합(가치중): Y ${fy.length} · partial ${fp.length} · N(bespoke) ${fn.length}`,
    `▶ 상호작용 유형: ${Object.entries(types).map(([k, v]) => `${k}=${v}`).join(' · ')}`,
    ``,
    ...valY.map((r) => `  ${fit(r[3]) === 'Y' ? '✓' : fit(r[3]) === 'partial' ? '~' : '✗'} ${r[0]} [${r[2]}] ${r[4] || ''}`.slice(0, 150)),
    ``, `── 가치 N ──`, ...rows.filter((r) => !Y(r[1])).map((r) => `  · ${r[0]}`),
  ].join('\n');
}

const t0 = Date.now();
if (BACKEND === 'opus') {
  const c = spawn('claude', ['-p', promptFor(cands), '--model', 'opus', '--output-format', 'json'], { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
  let out = ''; c.stdout.on('data', (d) => (out += d));
  c.on('close', () => {
    let result = '', u = {}; try { const j = JSON.parse(out); result = j.result || ''; u = j.usage || {}; } catch { result = out; }
    const rep = aggregate(rowsOf(result), { backend: 'opus', info: `cr=${u.cache_read_input_tokens ?? '?'} out=${u.output_tokens ?? '?'} ${Math.round((Date.now() - t0) / 1000)}s` });
    writeFileSync('/tmp/widget_survey_opus.txt', rep); console.log(rep);
  });
} else {
  // gemma4: 청크(6) 2병렬
  const chunks = []; for (let i = 0; i < cands.length; i += 6) chunks.push(cands.slice(i, i + 6));
  const results = new Array(chunks.length).fill('');
  let ci = 0;
  const callGemma = async (subset) => {
    const body = { model: GEMMA_MODEL, max_tokens: 1400, temperature: 0.2, messages: [{ role: 'user', content: promptFor(subset) }] };
    const r = await fetch(GEMMA_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const j = await r.json(); return j.choices?.[0]?.message?.content ?? '';
  };
  const worker = async () => { while (ci < chunks.length) { const k = ci++; try { results[k] = await callGemma(chunks[k]); console.log(`  청크 ${k + 1}/${chunks.length} 완료`); } catch (e) { console.log(`  청크 ${k + 1} 실패: ${e.message}`); } } };
  await Promise.all([worker(), worker()]);   // 2병렬
  const rep = aggregate(rowsOf(results.join('\n')), { backend: 'gemma4', info: `${chunks.length}청크 2병렬 ${Math.round((Date.now() - t0) / 1000)}s` });
  writeFileSync('/tmp/widget_survey_gemma.txt', rep); console.log(rep);
}
