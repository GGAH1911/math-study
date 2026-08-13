// 개념 재매핑 진행 대시보드 — 의존성 없는 단일 파일 서버.
//
// 러너(scripts/remap_concepts.py)가 문제마다 즉시 append 하는 JSONL 을 읽어 보여 준다.
// ★러너와 **단방향**으로만 붙는다(파일 읽기). 대시보드가 죽어도 작업은 계속되고,
//   작업이 죽어도 대시보드는 마지막 상태를 계속 보여 준다.
//
// 실행: node web/scripts/remap_dashboard.mjs [포트]
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';

const PORT = Number(process.argv[2] || 4381);
const JSONL = '/tmp/remap_concepts.jsonl';
// ★분모를 코드에 박아 두면 대상 기준이 바뀔 때마다 화면이 거짓말을 한다(1476 → 4164 로
//   넓혔더니 진행률이 3배 부풀어 보였다). 러너 로그의 '대상 N건' 을 읽어 쓴다.
import { readdirSync } from 'node:fs';
function totalFromLog() {
  try {
    const dir = '/tmp/ingest_logs';
    // ★이름순이 아니라 **최신순**. 이름순으로 뒤졌더니 옛 파일럿 로그(대상 100건)를 읽어
    //   진행률이 608% 로 나왔다.
    const logs = readdirSync(dir).filter((f) => f.startsWith('remap_'))
      .map((f) => ({ f, t: statSync(`${dir}/${f}`).mtimeMs }))
      .sort((a, b) => b.t - a.t).map((x) => x.f);
    for (const f of logs) {
      const head = readFileSync(`${dir}/${f}`, 'utf8').slice(0, 400);
      const m = head.match(/대상 (\d+)건/);
      if (m) return Number(m[1]);
    }
  } catch { /* 로그 없으면 폴백 */ }
  return 4164;
}

function snapshot() {
  if (!existsSync(JSONL)) return { rows: [], mtime: 0 };
  const txt = readFileSync(JSONL, 'utf8');
  const rows = [];
  for (const line of txt.split('\n')) {
    if (!line.trim()) continue;
    try { rows.push(JSON.parse(line)); } catch { /* 쓰는 중인 마지막 줄 */ }
  }
  const st = statSync(JSONL);
  return { rows, mtime: st.mtimeMs, birth: st.birthtimeMs || st.ctimeMs };
}

function summarize(rows, wallSec) {
  const byStatus = {}, byGrade = {}, bySubject = {};
  let sec = 0, flat = 0;
  for (const r of rows) {
    byStatus[r.status] = (byStatus[r.status] || 0) + 1;
    sec += r.sec || 0;
    if (r.unit) {
      const g = r.unit.split('/')[1] ?? '?';
      byGrade[g] = (byGrade[g] || 0) + 1;
      if (!r.unit.includes('/')) flat++;
    }
  }
  const done = rows.length;
  const avg = done ? sec / done : 0;
  // ★ETA 는 **벽시계** 기준이어야 한다. avgSec 은 '한 건이 걸린 시간' 이라 6병렬에서는
  //   실제보다 6배 부풀어 나온다(실측 128분을 762분으로 표시했다).
  const perItem = done && wallSec ? wallSec / done : avg;
  return {
    done, total: totalFromLog(), byStatus, byGrade, bySubject, flat,
    avgSec: Number(avg.toFixed(1)),
    perItemSec: Number(perItem.toFixed(2)),
    recent: rows.slice(-14).reverse(),
  };
}

const PAGE = `<!doctype html><meta charset="utf-8"><title>개념 재매핑 진행</title>
<style>
 :root{--bg:#0f1115;--fg:#e6e8ec;--dim:#8b93a1;--ok:#4ade80;--warn:#fbbf24;--bad:#f87171;--line:#232733}
 *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);
   font:14px/1.55 ui-sans-serif,system-ui,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;padding:22px}
 h1{font-size:17px;margin:0 0 4px} .sub{color:var(--dim);font-size:12px;margin-bottom:18px}
 .bar{height:22px;background:#1b1f27;border-radius:11px;overflow:hidden;margin:10px 0 6px}
 .bar>i{display:block;height:100%;background:linear-gradient(90deg,#3b82f6,#22d3ee);transition:width .4s}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}
 .card{background:#151922;border:1px solid var(--line);border-radius:10px;padding:11px 13px}
 .card b{display:block;font-size:22px;font-weight:600} .card span{color:var(--dim);font-size:12px}
 table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
 th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
 th{color:var(--dim);font-weight:500;font-size:12px}
 code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
 .ok{color:var(--ok)} .warn{color:var(--warn)} .bad{color:var(--bad)}
 .before{color:var(--dim);text-decoration:none}
 .spoke{color:var(--dim);font-size:12px;padding-left:6px}
 .pill{display:inline-block;background:#1b1f27;border:1px solid var(--line);border-radius:20px;
   padding:2px 9px;margin:2px 4px 2px 0;font-size:12px}
</style>
<h1>개념 재매핑 진행</h1>
<div class="sub" id="meta">연결 중…</div>
<div class="bar"><i id="pb" style="width:0%"></i></div>
<div class="sub" id="pct"></div>
<div class="grid" id="cards"></div>
<div id="grades"></div>
<table><thead><tr><th>문제</th><th>이전</th><th>이후 (단원 + 하위 개념)</th><th>초</th></tr></thead><tbody id="rows"></tbody></table>
<script>
const el=(id)=>document.getElementById(id);
function card(v,l,c=''){return \`<div class="card"><b class="\${c}">\${v}</b><span>\${l}</span></div>\`}
async function tick(){
  let d; try{ d=await (await fetch('/data')).json() }catch{ el('meta').textContent='서버 연결 끊김'; return }
  const {done,total,byStatus,byGrade,avgSec,recent,flat}=d;
  const pct=total?Math.min(100,done/total*100):0;
  el('pb').style.width=pct.toFixed(1)+'%';
  const left=Math.max(0,total-done);
  const eta=d.perItemSec&&left?Math.round(left*d.perItemSec/60):0;
  el('pct').textContent=\`\${done} / \${total} (\${pct.toFixed(1)}%) · 남은 예상 \${eta}분\`;
  el('meta').textContent=new Date().toLocaleTimeString('ko-KR')+' 기준 · 4초마다 갱신';
  el('cards').innerHTML=
    card(byStatus.ok||0,'성공','ok')+
    card((byStatus['map-fail']||0)+(byStatus['no-scope']||0),'실패',((byStatus['map-fail']||0)?'bad':''))+
    card(byStatus.partial||0,'부분',(byStatus.partial?'warn':''))+
    card(flat||0,'평면 잔존',(flat?'bad':'ok'))+
    card(avgSec+'s','호출당(모델)')+
    card((d.perItemSec??0)+'s','건당(벽시계)');
  el('grades').innerHTML='<div class="sub">학년 분포</div>'+
    Object.entries(byGrade).sort((a,b)=>b[1]-a[1])
      .map(([g,n])=>\`<span class="pill">\${g} \${n}</span>\`).join('');
  el('rows').innerHTML=recent.map(r=>\`<tr>
    <td><code>\${r.slug}</code></td>
    <td class="before"><code>\${(r.before||'').slice(0,60)}</code></td>
    <td class="\${r.status==='ok'?'ok':'warn'}"><code>\${r.unit||r.status}</code>
        \${(r.concepts||[]).map(c=>'<div class="spoke">└ '+c.split('/').pop()+'</div>').join('')}</td>
    <td>\${r.sec??''}</td></tr>\`).join('');
}
tick(); setInterval(tick,4000);
</script>`;

createServer((req, res) => {
  if (req.url === '/data') {
    const { rows, birth } = snapshot();
    const wallSec = birth ? (Date.now() - birth) / 1000 : 0;
    res.writeHead(200, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' });
    res.end(JSON.stringify(summarize(rows, wallSec)));
    return;
  }
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(PAGE);
}).listen(PORT, '0.0.0.0', () => {
  console.log(`재매핑 대시보드 → http://0.0.0.0:${PORT}  (JSONL: ${JSONL})`);
});
