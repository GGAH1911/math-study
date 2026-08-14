// 등록된 3D 스펙을 PNG 로 렌더한다 — 원본 도판과 눈으로 대조하기 위한 도구.
//
// ★왜 필요한가: 좌표가 sympy 로 검증돼도 "원본처럼 보이는가" 는 눈으로만 갈린다.
//   실제로 2022 9월모평 기하 29 는 좌표가 완벽한데 카메라가 접은 반원을 정면으로
//   겹쳐 보게 잡아서 종이를 접은 입체로 읽히지 않았다.
//
// 사용: node scripts/ops/render_figure3d.mjs <stem> [<stem> ...]
//   결과: $FIG3D_OUT (기본 /tmp/fig3d) 아래 <stem>.png
// 환경: MS_DEV_TOKEN(필수, dev 라우트가 admin 게이팅) · MS_BASE(기본 http://100.67.69.121:4324)
//       PLAYWRIGHT_PATH(playwright 모듈 경로)
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.MS_BASE ?? 'http://100.67.69.121:4324';
const OUT = process.env.FIG3D_OUT ?? '/tmp/fig3d';
const PW = process.env.PLAYWRIGHT_PATH ?? '/home/insung/projects/frontend/node_modules/playwright/index.mjs';
const TOKEN = process.env.MS_DEV_TOKEN ?? (fs.existsSync(process.env.MS_DEV_TOKEN_FILE ?? '')
  ? fs.readFileSync(process.env.MS_DEV_TOKEN_FILE, 'utf8').trim() : '');

if (!TOKEN) { console.error('MS_DEV_TOKEN 또는 MS_DEV_TOKEN_FILE 이 필요하다 (dev 라우트는 admin 전용)'); process.exit(2); }
const stems = process.argv.slice(2);
if (stems.length === 0) { console.error('사용: node scripts/ops/render_figure3d.mjs <stem> ...'); process.exit(2); }

const { chromium } = await import(PW);
fs.mkdirSync(OUT, { recursive: true });
// swiftshader: 헤드리스엔 GPU 가 없다. 한 페이지에 캔버스를 여러 개 띄우면 컨텍스트가
// 죽으므로(Context Lost) 스펙 하나당 페이지 하나로 연다.
const b = await chromium.launch({ args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const host = new URL(BASE).hostname;
const ctx = await b.newContext({ viewport: { width: 900, height: 900 } });
await ctx.addCookies([{ name: 'ms_session', value: TOKEN, domain: host, path: '/' }]);

for (const stem of stems) {
  const p = await ctx.newPage();
  const W = process.env.FIG3D_W ?? '800';   // 갤러리(작은 캔버스)와 비교할 때 쓴다
  const url = `${BASE}/dev/figrender3d?src=prob3d&id=${encodeURIComponent(stem)}&w=${W}&capture=1`;
  try {
    await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
    // 첫 프레임 후 __figReady 를 세운다 — 그 전에 찍으면 검은 화면이 나온다.
    try { await p.waitForFunction(() => document.title.includes('READY'), null, { timeout: 45000 }); }
    catch { console.error(`${stem}: READY 안 뜸 (그래도 캡처)`); }
    await p.waitForTimeout(2500);
    await p.screenshot({ path: path.join(OUT, `${stem}.png`) });
    console.log(`ok ${stem} → ${path.join(OUT, `${stem}.png`)}`);
  } catch (e) {
    console.error(`fail ${stem}: ${e.message}`);
  }
  await p.close();
}
await b.close();
