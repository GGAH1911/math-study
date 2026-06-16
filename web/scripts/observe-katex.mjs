// 헤드리스 chromium(CDP)으로 /test-katex 를 실제 로드 → 케이스별 .katex 렌더 수 + raw $ 관측.
// 캐시된 playwright chromium 바이너리를 직접 띄워 CDP 로 구동(playwright 패키지 불필요).
import { spawn } from 'node:child_process';
import { readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const base = join(homedir(), '.cache/ms-playwright');
const dir = readdirSync(base).filter((d) => /^chromium-\d/.test(d)).sort().pop();
const exe = join(base, dir, 'chrome-linux64', 'chrome');

const PORT = 9333;
const proc = spawn(exe, [
  `--remote-debugging-port=${PORT}`, '--headless=new', '--no-sandbox',
  '--disable-gpu', '--hide-scrollbars', 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function cdp() {
  for (let i = 0; i < 40; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error('CDP 안 뜸');
}

async function run() {
  const wsUrl = await cdp();
  const ws = new WebSocket(wsUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0;
  const pending = new Map();
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });

  await send('Page.enable');
  await send('Runtime.enable');
  await send('Page.navigate', { url: 'http://localhost:4323/test-katex' });
  await sleep(3500); // 하이드레이션 + katex 동적 import + 렌더 대기

  const expr = `(${(() => {
    const out = [];
    for (const el of document.querySelectorAll('.case')) {
      const name = el.getAttribute('data-case');
      const katex = el.querySelectorAll('.katex').length;
      // .katex span 제거 후 남은 raw $ / raw 명령
      const clone = el.cloneNode(true);
      clone.querySelectorAll('.katex').forEach((k) => k.remove());
      const txt = clone.textContent || '';
      const rawDollar = (txt.match(/\\$/g) || []).length;
      const rawCmd = (txt.match(/\\\\(?:text|frac|nP|nC)/g) || []).length;
      out.push({ name, katex, rawDollar, rawCmd, leftover: txt.replace(/\\s+/g, ' ').trim().slice(0, 90) });
    }
    return JSON.stringify(out);
  }).toString()})()`;

  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
  const val = r?.result?.value;          // CDP: {result:{result:{value}}}
  if (val === undefined) {
    console.error('evaluate 실패:', JSON.stringify(r?.result?.exceptionDetails ?? r, null, 2).slice(0, 500));
    ws.close(); proc.kill(); process.exit(2);
  }
  const rows = JSON.parse(val);
  let pass = 0;
  for (const row of rows) {
    const ok = row.katex >= 1 && row.rawDollar === 0 && row.rawCmd === 0;
    if (ok) pass++;
    console.log(`${ok ? '✅' : '❌'} ${row.name}: .katex ${row.katex}, raw$ ${row.rawDollar}, rawCmd ${row.rawCmd}`);
    if (!ok) console.log(`   남은텍스트: ${row.leftover}`);
  }
  console.log(`\n관측 결과: ${pass}/${rows.length} 통과`);
  ws.close();
  proc.kill();
  process.exit(pass === rows.length ? 0 : 1);
}

run().catch((e) => { console.error(e); proc.kill(); process.exit(2); });
