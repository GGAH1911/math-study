#!/usr/bin/env node
// LLM 실시간 모니터 — .llm-monitor/events.ndjson 를 tail 해서 SSE 로 중계 + 대시보드 HTML 서빙.
//   ★호스트에서 돈다(의존성 0, node 내장만). 생성기는 컨테이너에서 돌지만 레포가 바인드마운트라
//   같은 파일을 본다(/app/.llm-monitor == ~/math-study/.llm-monitor).
// 사용: node web/scripts/llm_monitor_server.mjs [--port 4380]
//   접속: http://100.67.69.121:4380  (Tailscale, 무인증 — dev 관측용)
import { createServer } from 'node:http';
import { existsSync, mkdirSync, statSync, createReadStream, writeFileSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const MON = `${REPO}/.llm-monitor`;
const EV = `${MON}/events.ndjson`;
if (!existsSync(MON)) mkdirSync(MON, { recursive: true });
if (!existsSync(EV)) writeFileSync(EV, '');
const A = process.argv.slice(2);
const PORT = +(A[A.indexOf('--port') + 1] || process.env.MON_PORT || 4380);

const HTML = `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM 모니터 — 위젯 생성</title><style>
:root{--bg:#0e1116;--pan:#161b22;--bd:#2a3038;--tx:#e6edf3;--dim:#8b949e;--ok:#3fb950;--no:#f85149;--run:#d29922;--ac:#58a6ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.5 ui-sans-serif,system-ui,"Noto Sans KR",sans-serif}
header{padding:10px 14px;border-bottom:1px solid var(--bd);display:flex;gap:16px;align-items:center;flex-wrap:wrap;position:sticky;top:0;background:var(--bg);z-index:5}
h1{font-size:15px;margin:0;font-weight:600}
.stat{font-size:12px;color:var(--dim)}.stat b{color:var(--tx);font-size:15px;font-variant-numeric:tabular-nums}
.wrap{display:grid;grid-template-columns:minmax(240px,340px) 1fr;gap:12px;padding:12px;align-items:start}
@media(max-width:820px){.wrap{grid-template-columns:1fr}}
.pan{background:var(--pan);border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.pan>h2{font-size:12px;margin:0;padding:8px 12px;color:var(--dim);border-bottom:1px solid var(--bd);font-weight:600;letter-spacing:.04em}
.item{padding:8px 12px;border-bottom:1px solid var(--bd);cursor:pointer;display:flex;gap:8px;align-items:baseline}
.item:hover{background:#1c2430}.item.sel{background:#1f2937;box-shadow:inset 3px 0 0 var(--ac)}
.item .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px}
.chip{font-size:11px;padding:1px 7px;border-radius:20px;white-space:nowrap;font-weight:600}
.c-run{background:#3d2f0d;color:var(--run)}.c-ok{background:#0f2f18;color:var(--ok)}.c-no{background:#3d1418;color:var(--no)}
.meta{font-size:11px;color:var(--dim);font-variant-numeric:tabular-nums;white-space:nowrap}
.tabs{display:flex;gap:2px;padding:6px 10px;border-bottom:1px solid var(--bd)}
.tab{font-size:12px;padding:4px 10px;border-radius:6px;cursor:pointer;color:var(--dim)}
.tab.on{background:#1f2937;color:var(--tx)}
pre{margin:0;padding:12px;white-space:pre-wrap;word-break:break-word;font:12px/1.65 ui-monospace,SFMono-Regular,Menlo,monospace;max-height:62vh;overflow:auto}
.reason{color:#a9b4c0}.err{color:var(--no);padding:10px 12px;font-size:12px;border-top:1px solid var(--bd);white-space:pre-wrap}
.cursor{display:inline-block;width:7px;height:14px;background:var(--ac);animation:b 1s steps(2) infinite;vertical-align:-2px}
@keyframes b{50%{opacity:0}}
.empty{padding:24px 12px;color:var(--dim);font-size:13px;text-align:center}
.dot{width:8px;height:8px;border-radius:50%;background:var(--no);display:inline-block}.dot.on{background:var(--ok)}
</style></head><body>
<header>
 <h1>LLM 모니터</h1>
 <span class="stat"><span class="dot" id="live"></span> <span id="conn">연결중</span></span>
 <span class="stat">모델 <b id="model">-</b></span>
 <span class="stat">진행 <b id="prog">0/0</b></span>
 <span class="stat">합격 <b id="pass">0</b></span>
 <span class="stat">실패 <b id="fail">0</b></span>
 <span class="stat">누적비용 <b id="cost">$0</b></span>
</header>
<div class="wrap">
 <div class="pan"><h2>개념</h2><div id="list"><div class="empty">아직 실행 없음</div></div></div>
 <div class="pan">
  <div class="tabs"><div class="tab on" data-t="reason">사고과정</div><div class="tab" data-t="content">출력(JSON)</div><div class="tab" data-t="spec">검증결과</div></div>
  <pre id="body" class="reason"><span class="empty">왼쪽에서 개념을 고르세요</span></pre>
  <div class="err" id="err" style="display:none"></div>
 </div>
</div>
<script>
const S={}, order=[]; let sel=null, tab='reason', cost=0, total=0, pass=0, fail=0;
const $=(i)=>document.getElementById(i);
function chip(s){return s==='run'?'<span class="chip c-run">생성중</span>':s==='ok'?'<span class="chip c-ok">PASS</span>':'<span class="chip c-no">FAIL</span>'}
function renderList(){
 const L=$('list'); if(!order.length){L.innerHTML='<div class="empty">아직 실행 없음</div>';return}
 L.innerHTML=order.map(id=>{const s=S[id];const u=s.usage||{};
  return '<div class="item'+(id===sel?' sel':'')+'" data-id="'+encodeURIComponent(id)+'">'+chip(s.st)+
   '<span class="nm" title="'+esc(id)+'">'+esc(id.split('/').pop())+'</span>'+
   '<span class="meta">'+(s.secs?s.secs+'s ':'')+(u.completion_tokens?u.completion_tokens+'tok':'')+'</span></div>'}).join('');
 [...L.querySelectorAll('.item')].forEach(e=>e.onclick=()=>{sel=decodeURIComponent(e.dataset.id);renderList();renderBody()});
}
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function renderBody(){
 const b=$('body'), er=$('err');
 if(!sel||!S[sel]){b.innerHTML='<span class="empty">왼쪽에서 개념을 고르세요</span>';er.style.display='none';return}
 const s=S[sel];
 let t = tab==='reason'?s.reason : tab==='content'?s.content : (s.spec?JSON.stringify(s.spec,null,1):'(검증 통과분만 spec 표시)');
 b.className = tab==='reason'?'reason':'';
 b.innerHTML=esc(t||'(비어있음)')+(s.st==='run'?'<span class="cursor"></span>':'');
 if(s.st==='run'&&stick)b.scrollTop=b.scrollHeight;
 if(s.why){er.style.display='';er.textContent='↳ '+s.why}else er.style.display='none';
}
let stick=true;
$('body').addEventListener('scroll',e=>{const el=e.target;stick=el.scrollHeight-el.scrollTop-el.clientHeight<40});
[...document.querySelectorAll('.tab')].forEach(e=>e.onclick=()=>{
 document.querySelector('.tab.on').classList.remove('on');e.classList.add('on');tab=e.dataset.t;stick=true;renderBody()});
function stats(){$('prog').textContent=(pass+fail)+'/'+total;$('pass').textContent=pass;$('fail').textContent=fail;$('cost').textContent='$'+cost.toFixed(5)}
const es=new EventSource('/events');
es.onopen=()=>{$('conn').textContent='연결됨';$('live').classList.add('on')};
es.onerror=()=>{$('conn').textContent='끊김';$('live').classList.remove('on')};
es.onmessage=(m)=>{
 const e=JSON.parse(m.data);
 if(e.ev==='run'){total=e.total;$('model').textContent=e.model+(e.par?' ×'+e.par:'');pass=fail=0;cost=0;for(const k in S)delete S[k];order.length=0;renderList();stats();return}
 if(e.ev==='start'){S[e.id]={st:'run',reason:'',content:'',why:'',usage:{}};if(!order.includes(e.id))order.push(e.id);
  if(!sel||S[sel]?.st!=='run')sel=e.id; total=e.total||total; renderList();renderBody();stats();return}
 const s=S[e.id]; if(!s)return;
 if(e.ev==='reason'){s.reason+=e.d; if(e.id===sel)renderBody()}
 else if(e.ev==='content'){s.content+=e.d; if(e.id===sel&&tab==='content')renderBody()}
 else if(e.ev==='done'){s.st=e.ok?'ok':'no';s.why=e.why||'';s.secs=e.secs;s.usage=e.usage||{};s.spec=e.spec;
  e.ok?pass++:fail++; cost+=(e.usage&&e.usage.cost)||0; renderList();renderBody();stats()}
 else if(e.ev==='summary'){$('conn').textContent='완료'}
};
</script></body></html>`;

// ── SSE: 파일을 처음부터 한 번 흘려주고(재접속 시 맥락 복원), 이후 증분만 tail ──────────────
const clients = new Set();
let pos = 0, tail = '';

function pump() {
  let sz; try { sz = statSync(EV).size; } catch { return; }
  if (sz < pos) { pos = 0; tail = ''; }           // 파일이 새로 시작됨(트렁케이트)
  if (sz === pos) return;
  const rs = createReadStream(EV, { start: pos, end: sz - 1, encoding: 'utf8' });
  let chunk = '';
  rs.on('data', (d) => (chunk += d));
  rs.on('end', () => {
    pos = sz;
    tail += chunk;
    const lines = tail.split('\n'); tail = lines.pop();
    for (const ln of lines) {
      if (!ln.trim()) continue;
      for (const c of clients) { try { c.write(`data: ${ln}\n\n`); } catch { /* 끊긴 클라 */ } }
    }
  });
}
setInterval(pump, 300);

createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname === '/events') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive', 'X-Accel-Buffering': 'no' });
    res.write(': ok\n\n');
    // 신규 접속엔 기존 이벤트 전량 리플레이(중간에 들어와도 화면이 채워지도록)
    try {
      const all = existsSync(EV) ? readFileSync(EV, 'utf8') : '';
      for (const ln of all.split('\n')) if (ln.trim()) res.write(`data: ${ln}\n\n`);
    } catch { /* 리플레이 실패해도 이후 tail 은 동작 */ }
    clients.add(res);
    const ka = setInterval(() => { try { res.write(': ka\n\n'); } catch { /* noop */ } }, 15000);
    req.on('close', () => { clearInterval(ka); clients.delete(res); });
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(HTML);
}).listen(PORT, '0.0.0.0', () => {
  console.log(`LLM 모니터 → http://100.67.69.121:${PORT}  (이벤트: ${EV})`);
});
