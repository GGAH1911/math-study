// 맥북 gemma4(mlx_vlm.server, OpenAI호환)로 기출 함수그래프 → RedrawPlot spec 산출.
// 사용: node web/scripts/gemma_measure.mjs <imgPath> <bonmunFile> <outPath>
//   bonmunFile = 본문(ground truth) 텍스트 파일.  out = RedrawPlot spec JSON.
import { readFileSync, writeFileSync } from 'node:fs';
const GEMMA = process.env.GEMMA_URL || 'http://100.79.230.49:8080/v1/chat/completions';
const MODEL = process.env.GEMMA_MODEL || 'mlx-community/gemma-4-26B-A4B-it-qat-4bit';
const [imgPath, bonmunFile, outPath] = process.argv.slice(2);
const img = readFileSync(imgPath).toString('base64');
const ext = imgPath.endsWith('.png') ? 'png' : 'jpeg';
const bonmun = readFileSync(bonmunFile, 'utf8').trim();

const prompt = `너는 한국 수능 기출 함수그래프를 function-plot 기반 RedrawPlot spec 으로 재현하는 측정가다.

★대원칙: **본문이 ground truth**. 본문의 곡선식·조건·값을 그대로 쓰고, 이미지는 레이아웃·배치·정의역(곡선이 어디부터 어디까지 그려졌나)·음영영역만 본다. 이미지에서 곡선모양 추정 금지.

본문(ground truth):
${bonmun}

이미지(레이아웃 참조): 첨부.

RedrawPlot spec(JSON):
{
 "range":[xmin,xmax], "yRange":[ymin,ymax],
 "curves":[{"fn":"mathjs식","range":[a,b]}],   // fn: x변수·^거듭제곱·log(x)=자연로그ln·sin/cos·pi·exp. 본문 식 그대로. range=이미지에 곡선이 실제 그려진 구간(원점부터 시작하면 0부터!).
 "lines":[{"from":[x,y],"to":[x,y],"dashed":false}],   // 직선·세로선(x=c)·점근선(dashed:true)
 "points":[{"x":,"y":,"label":"LaTeX","dir":"우상"}],   // label은 LaTeX(예 "A","P_1"). dir=라벨방향
 "regions":[{"pts":[[x,y],...],"opacity":0.45}],   // 음영=다각형. 곡선변은 곡선식으로 6~10점 샘플
 "texts":[{"x":,"y":,"text":"LaTeX","dir":"우"}]   // 곡선식·축눈금 라벨. **LaTeX**(예 "y=\\\\log_2 x","x=\\\\frac{\\\\pi}{2}","y=\\\\frac{\\\\cos x}{x}")
}
dir: 위·아래·좌·우·좌상·우상·좌하·우하.

규칙:
- 곡선 range는 **이미지에 그려진 그대로**. 곡선이 원점(0)부터 그려졌으면 range도 0부터. 일부만 그렸으면 그만큼만.
- 점좌표는 본문 조건으로 유도(교점=식 연립). 이미지로 검산.
- 라벨(texts·label)은 모두 **LaTeX 문자열**(분수 \\\\frac, 첨자 _, 그리스 \\\\pi 등). 라벨끼리 겹치지 않게 dir·위치 잘 잡아라.
- 음영영역은 본문이 지정한 영역과 정확히 일치.

출력은 RedrawPlot spec JSON 하나만. 설명·코드펜스 없이 순수 JSON.`;

const body = { model: MODEL, max_tokens: 2200, temperature: 0.2, messages: [{ role: 'user', content: [{ type: 'text', text: prompt }, { type: 'image_url', image_url: { url: `data:image/${ext};base64,${img}` } }] }] };
const t0 = Date.now();
const r = await fetch(GEMMA, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
const j = await r.json();
const content = j.choices?.[0]?.message?.content ?? '';
const m = content.match(/\{[\s\S]*\}/);
if (!m) { console.error('JSON 추출 실패:', content.slice(0, 300)); process.exit(1); }
let spec;
try { spec = JSON.parse(m[0]); } catch (e) { console.error('JSON 파싱 실패:', e.message, '\n', m[0].slice(0, 400)); process.exit(1); }
writeFileSync(outPath, JSON.stringify(spec, null, 1));
console.log(`gemma4 spec → ${outPath} · ${Math.round((Date.now() - t0) / 1000)}s · curves ${(spec.curves || []).length} lines ${(spec.lines || []).length} regions ${(spec.regions || []).length} texts ${(spec.texts || []).length}`);
