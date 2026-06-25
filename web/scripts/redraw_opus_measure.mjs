#!/usr/bin/env node
// Opus(claude -p)로 기출 함수그래프 → RedrawPlot spec 정밀 측정/수정. gemma 대체(품질).
//   프롬프트 캐싱: clean cwd(/tmp/claude_p_clean) + CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1 → 시스템프롬프트
//   prefix 안정 → cache_read ~76% 입력비용↓. 이미지는 --add-dir 로 전달(Opus가 Read).
// 사용: node web/scripts/redraw_opus_measure.mjs <img> <bonmunFile> <out> [feedbackFile]
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
const REPO = '/home/insung/Projects/math-study';
const [imgPath, bonmunFile, outPath, fbFile] = process.argv.slice(2);
const bonmun = readFileSync(bonmunFile, 'utf8').trim();
const feedback = (fbFile && existsSync(fbFile)) ? readFileSync(fbFile, 'utf8').trim() : '';
const RUBRIC = readFileSync(`${REPO}/docs/REDRAW_RUBRIC.md`, 'utf8');
const CLEAN_DIR = '/tmp/claude_p_clean'; if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });
const LOGDIR = '/tmp/ingest_logs'; if (!existsSync(LOGDIR)) mkdirSync(LOGDIR, { recursive: true });
const imgDir = imgPath.substring(0, imgPath.lastIndexOf('/'));
const MODEL = process.env.OPUS_MEASURE_MODEL || 'opus';

const prompt = `너는 한국 수능 기출 함수그래프를 function-plot 기반 RedrawPlot spec(JSON)으로 **정밀 재현/수정**한다. 아래 채점기준 만점(40/40)을 목표로 한다.

${RUBRIC}

RedrawPlot spec 형식(JSON):
{
 "range":[x0,x1], "yRange":[y0,y1],
 "curves":[{"fn":"mathjs식","range":[a,b]}],   // fn=x변수만(^거듭제곱·log(x)=자연로그ln·sin·cos·pi·exp). k·a·b 등 파라미터는 본문/이미지로 구체값 치환. 미치환=렌더실패.
 "lines":[{"from":[x,y],"to":[x,y],"dashed":false}],   // 직선·세로선(x=c)·점근선(dashed:true)
 "points":[{"x":,"y":,"label":"LaTeX","dir":"우상","open":false}],   // open=빈원(불연속)
 "regions":[{"pts":[[x,y],...],"opacity":0.45}],   // 음영 다각형(곡선변은 곡선식으로 6~10점 샘플)
 "texts":[{"x":,"y":,"text":"LaTeX","dir":"우"}]   // 곡선식·축눈금 자유라벨
}
dir: 위·아래·좌·우·좌상·우상·좌하·우하. 라벨(label·text)은 KaTeX TeX(예 "y=\\\\log_{2}x","x=\\\\frac{\\\\pi}{2}").

★만점 체크: ①본문 식·조건 그대로(fn에 x만, 점좌표 본문유도) ②곡선 정의역=이미지 실제 구간(원점부터 수렴하면 0근처부터) ③음영=본문 지정 영역 정확(직선변 사각형이면 직선, 곡선변이면 점샘플) ④라벨 **하나도 빠뜨리지 말고**(곡선식·점·축눈금) 겹침/잘림 없이 정확히 앵커 ⑤군더더기 없음.

원본 이미지: ${imgPath} (Read 로 정확히 봐라). 본문(ground truth): ${bonmun}
${feedback ? `\n[재시도 — 이전 결과의 결함을 고쳐라]\n${feedback}\n위 지적된 결함만 수정하고 잘 된 부분(라벨·곡선·점·음영)은 그대로 유지하라.` : ''}

출력은 RedrawPlot spec JSON 하나만(코드펜스·설명 없이 순수 JSON).`;

const t0 = Date.now();
const c = spawn('claude', ['-p', prompt, '--model', MODEL, '--output-format', 'json', '--add-dir', imgDir], { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
let out = '';
c.stdout.on('data', (d) => (out += d));
c.on('close', () => {
  let result = '', usage = {};
  try { const j = JSON.parse(out); result = j.result || ''; usage = j.usage || {}; } catch { result = out; }
  appendFileSync(`${LOGDIR}/opus_measure_usage.log`, `${MODEL}\tcr=${usage.cache_read_input_tokens ?? '?'}\tin=${usage.input_tokens ?? '?'}\tout=${usage.output_tokens ?? '?'}\n`);
  const m = result.match(/\{[\s\S]*\}/);
  if (!m) { console.error('JSON 추출 실패:', result.slice(0, 200)); process.exit(1); }
  try {
    const spec = JSON.parse(m[0]);
    writeFileSync(outPath, JSON.stringify(spec, null, 1));
    console.log(`opus spec → ${outPath} · ${Math.round((Date.now() - t0) / 1000)}s · curves ${(spec.curves || []).length} texts ${(spec.texts || []).length} cr=${usage.cache_read_input_tokens ?? '?'}`);
  } catch (e) { console.error('파싱실패:', e.message); process.exit(1); }
});
