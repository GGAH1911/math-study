#!/usr/bin/env node
// 개념 → InteractiveSpec + 검증 recipe 생성기 (Opus claude -p, 캐싱).
//   출력 {spec, recipe} → /tmp/widget_specs/<id>.json. recipe는 이중유도 검증기(widget_validate)가 먹는 형식.
// 사용: node web/scripts/widget_generate.mjs <conceptId> [<conceptId> ...]
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
// ★REPO 는 이 스크립트 자기 위치 기준(web/scripts/.. 의 부모) — 하드코딩 절대경로는 레포 위치가
//   머신마다 다르면(laptop ~/Projects/math-study, tme ~/math-study) 깨진다.
const REPO = fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const CDIR = `${REPO}/docs/concepts`;
const OUT = '/tmp/widget_specs'; if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });
const CLEAN = '/tmp/claude_p_clean'; if (!existsSync(CLEAN)) mkdirSync(CLEAN, { recursive: true });

function bodyOf(id) {
  for (const cand of [`${CDIR}/${id}.md`, `${CDIR}/${id.normalize('NFD')}.md`, `${CDIR}/${id.normalize('NFC')}.md`]) {
    if (existsSync(cand)) { const m = readFileSync(cand, 'utf8').match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/); if (m) return m[1].replace(/\s+/g, ' ').trim().slice(0, 700); }
  }
  return '';
}

const HEAD = `너는 한국 수학 개념을 **인터랙티브 시각화(InteractiveSpec)**로 만든다. 출력은 {"spec":..., "recipe":...} JSON 하나만(코드펜스 없이).

InteractiveSpec 형식:
{ "title", "params":[{"name","label","type":"slider","min","max","init","step","unit"}], "scope":"mathjs ;구분 대입식(슬라이더값→보조변수)", "geometry":{"range":[x0,x1],"yRange":[y0,y1],"showAxes":true,"showGrid":true,"shapes":[{"type":"circle|point|segment|line|polygon", ...좌표/값에 \\"=식\\" 가능}]}, "plot":{"range","yRange","fns":[{"fn","label","color"}]}, "readout":[{"label","expr","digits"}] }
- \\"=식\\"은 어디든 mathjs로 scope에서 평가(scope변수 사용). **함수 그래프가 핵심이면 plot만 써라** — plot이 있는데 geometry에 곡선 없이 점·선분만 찍는 건 **금지**(중복·혼란). geometry는 곡선이 없는 진짜 도형(원·다각형·단위원·벡터·각)일 때만. 슬라이더 돌리면 실시간 갱신.
예시(단위원·삼각비): {"params":[{"name":"theta","label":"θ","type":"slider","min":0,"max":360,"init":30,"step":1}],"scope":"rad=theta*pi/180; cx=cos(rad); sy=sin(rad)","geometry":{"range":[-1.4,1.4],"yRange":[-1.4,1.4],"showAxes":true,"shapes":[{"type":"circle","center":[0,0],"radius":1},{"type":"point","at":["=cx","=sy"],"label":"P"}]},"readout":[{"label":"sin","expr":"sy"}]}

recipe(검증용 — 매우 중요): {"samples":[{슬라이더값}×3~4],"invariants":["scope변수로 쓴 수학 항등식; 모든 샘플서 절댓값 ≈0이어야"],"oracle":[{"params":{슬라이더값},"expect":{"scope변수":손계산값}}×2~3],"tol":1e-6}
- invariants는 개념의 **수학적 사실에서 유도**: 단위원→"cx^2+sy^2-1", 곡선 위 점이면 그 점이 식 만족, 접선기울기=도함수 등.
- oracle의 expect는 **네가 독립적으로 손계산한 정답**(예 theta=30°면 sy=0.5).
- expect는 tol=1e-6 으로 대조한다. 어림값 금지 — 소수 8자리 이상 정확히 쓰거나, **정수·유리수로 딱 떨어지는 파라미터를 골라라**.

**mathjs 문법(scope·readout·invariants·"=식" 전부 해당). 벗어나면 검증기가 즉시 reject 한다:**
- 조건분기는 삼항연산자 "조건 ? a : b" 만. **if(...) 함수는 없다.**
- 화살표함수("x -> ...")·JS 문법 없음. map/filter 콜백도 쓰지 마라. 합은 닫힌 식이나 sum([a,b,c]) 로.
- 조합·순열은 combinations(n,r) · permutations(n,r) · factorial(n). **comb·nCr·C(n,r) 은 없다.**
- 쓸 수 있는 것: ^(거듭제곱) mod(a,b) sqrt abs exp log(x)=자연로그 log(x,b) log10 round(x,n) floor ceil max min sum mean sign
- 상수는 pi · e. 삼각함수는 **라디안**(sin cos tan asin acos atan atan2) — 도수는 deg*pi/180 으로 직접 변환.
- 변수명은 영문·숫자·밑줄만(한글 변수 금지). scope 문장 구분자는 ; 이다.

개념의 핵심을 슬라이더로 탐구하게 하는 spec + 그 정답을 강제하는 recipe를 만들어라. 본문:
`;

function gen(id) {
  return new Promise((res) => {
    const body = bodyOf(id);
    if (!body) { console.log(`✗ ${id} 본문없음`); return res(); }
    const prompt = `${HEAD}\n[${id}]\n${body}`;
    const c = spawn('claude', ['-p', prompt, '--model', 'opus', '--output-format', 'json'], { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    let out = ''; c.stdout.on('data', (d) => (out += d));
    c.on('close', () => {
      let result = '', u = {}; try { const j = JSON.parse(out); result = j.result || ''; u = j.usage || {}; } catch { result = out; }
      const m = result.match(/\{[\s\S]*\}/);
      if (!m) { console.log(`✗ ${id} JSON 추출 실패`); return res(); }
      try {
        const obj = JSON.parse(m[0]);
        if (!obj.spec || !obj.recipe) { console.log(`✗ ${id} spec/recipe 누락`); return res(); }
        writeFileSync(`${OUT}/${id.replace(/\//g, '__')}.json`, JSON.stringify({ id, ...obj }, null, 1));
        console.log(`✓ ${id} (params ${(obj.spec.params || []).length}, invariants ${(obj.recipe.invariants || []).length}, cr=${u.cache_read_input_tokens ?? '?'}, cc=${u.cache_creation_input_tokens ?? '?'})`);
      } catch (e) { console.log(`✗ ${id} 파싱: ${e.message}`); }
      res();
    });
  });
}

const ids = process.argv.slice(2);
(async () => { for (const id of ids) await gen(id); console.log('생성 완료 →', OUT); })();
