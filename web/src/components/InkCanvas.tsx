import { useRef, useEffect, useState, useCallback, type CSSProperties } from 'react';

// 저지연 필기 캔버스 + 레이어 — 애플펜슬/S펜/터치/마우스. 채점·LLM·API 무관.
//   저지연: desynchronized · getCoalescedEvents · getPredictedEvents · 진행 overlay · 압력 · 팜리젝션
//   레이어: ★스택형 per-layer 캔버스 — 가시 토글=display, 지우개 격리=그 레이어에 destination-out(자동).
//   벡터 스트로크 모델(선택·변형 토대). 영속=localStorage(per storageKey, v2 레이어 포맷). 스펙: docs/architecture/handwriting-canvas.md
type PE = PointerEvent & { getPredictedEvents?: () => PointerEvent[] };
type Pt = { x: number; y: number; p: number };
type Stroke = { tool: 'pen' | 'eraser'; color: string; width: number; dashed: boolean; pressure: boolean; pts: Pt[] };
type LayerMeta = { id: string; name: string; visible: boolean };
type Action = { type: 'add' | 'remove'; layerId: string; strokes: Stroke[] };
type Paper = 'blank' | 'ruled' | 'grid';

const COLORS = ['#2A261E', '#39487D', '#C13D38', '#2E7B4F'];
const WIDTHS = [1.5, 2.5, 4];
const ERASER_W = 18;
const nid = () => 'L' + Math.random().toString(36).slice(2, 8);

export default function InkCanvas({ storageKey, height = 560 }: { storageKey: string; height?: number }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const overRef = useRef<HTMLCanvasElement>(null);
  const overCtx = useRef<CanvasRenderingContext2D | null>(null);
  const strokesOf = useRef(new Map<string, Stroke[]>());                 // layerId → strokes
  const elOf = useRef(new Map<string, { c: HTMLCanvasElement; ctx: CanvasRenderingContext2D | null }>());
  const cur = useRef<Stroke | null>(null);
  const removed = useRef<Stroke[]>([]);
  const undoStack = useRef<Action[]>([]);
  const redoStack = useRef<Action[]>([]);
  const penSeen = useRef(false);
  const recentPen = useRef(false); // 최근 펜 접촉 윈도우 — 획 사이 빠른 2탭(iOS 더블탭 선택 콜아웃) 차단용
  const sizeRef = useRef({ w: 0, h: 0, dpr: 1 });

  const [layers, setLayers] = useState<LayerMeta[]>([{ id: 'L1', name: '레이어 1', visible: true }]);
  const [activeId, setActiveId] = useState('L1');
  const [panel, setPanel] = useState(false);
  const [rev, setRev] = useState(0); // 썸네일·패널 갱신
  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');
  const [eraserMode, setEraserMode] = useState<'precise' | 'stroke'>('precise');
  const [pressure, setPressure] = useState(false);
  const [dashed, setDashed] = useState(false);
  const [color, setColor] = useState(COLORS[0]);
  const [width, setWidth] = useState(WIDTHS[1]);
  const [paper, setPaper] = useState<Paper>('grid');
  const [gap, setGap] = useState(24);
  const [full, setFull] = useState(false);
  const live = useRef({ tool, eraserMode, pressure, dashed, color, width, activeId });
  live.current = { tool, eraserMode, pressure, dashed, color, width, activeId };
  const layersRef = useRef(layers); layersRef.current = layers; // save()가 effect 재실행 없이 최신 레이어 읽게

  const KEY = `ink:${storageKey}`;
  const pw = (s: Stroke, p: number) => s.pressure ? s.width * (0.45 + 1.3 * (p > 0 ? p : 0.5)) : s.width;

  const drawStroke = useCallback((ctx: CanvasRenderingContext2D, s: Stroke) => {
    if (s.pts.length === 0) return;
    ctx.save(); ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = s.tool === 'eraser' ? 'destination-out' : 'source-over';
    ctx.strokeStyle = s.color;
    if (s.pts.length === 1) { const a = s.pts[0]; ctx.fillStyle = s.color; ctx.beginPath(); ctx.arc(a.x, a.y, pw(s, a.p) / 2, 0, Math.PI * 2); ctx.fill(); ctx.restore(); return; }
    if (s.dashed && s.tool === 'pen') {
      ctx.lineCap = 'butt'; ctx.lineWidth = s.width; ctx.setLineDash([s.width * 2.6, s.width * 3]);
      ctx.beginPath(); ctx.moveTo(s.pts[0].x, s.pts[0].y);
      for (let i = 1; i < s.pts.length; i++) ctx.lineTo(s.pts[i].x, s.pts[i].y); ctx.stroke();
    } else {
      ctx.lineCap = 'round'; ctx.setLineDash([]);
      for (let i = 1; i < s.pts.length; i++) { const a = s.pts[i - 1], b = s.pts[i]; ctx.beginPath(); ctx.lineWidth = pw(s, (a.p + b.p) / 2); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
    }
    ctx.restore();
  }, []);

  const drawLayer = useCallback((id: string) => {
    const e = elOf.current.get(id); if (!e?.ctx) return;
    e.ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
    for (const s of strokesOf.current.get(id) ?? []) drawStroke(e.ctx, s);
  }, [drawStroke]);

  // 캔버스 사이즈(retina) + 컨텍스트. sizeRef 가 정해진 뒤 호출.
  const sizeCanvas = useCallback((c: HTMLCanvasElement, lowLatency = false): CanvasRenderingContext2D | null => {
    const { w, h, dpr } = sizeRef.current;
    c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); c.style.width = w + 'px'; c.style.height = h + 'px';
    // ★진행 overlay만 desynchronized(저지연). 확정 레이어는 일반 컨텍스트 —
    //   desynchronized 캔버스를 여러 개 겹치면 일부가 하드웨어 overlay plane으로 빠져 합성이 안 돼
    //   보이지 않을 수 있음(필기 그렸다가 확정 시 사라지는 버그의 원인).
    const ctx = c.getContext('2d', lowLatency ? ({ desynchronized: true } as CanvasRenderingContext2DSettings) : undefined);
    ctx?.scale(dpr, dpr); return ctx;
  }, []);

  const save = useCallback(() => {
    try {
      const strokes: Record<string, Stroke[]> = {};
      for (const l of layersRef.current) strokes[l.id] = strokesOf.current.get(l.id) ?? [];
      localStorage.setItem(KEY, JSON.stringify({ v: 2, layers: layersRef.current, strokes, activeId: live.current.activeId }));
    } catch { /* quota */ }
  }, [KEY]);

  const hit = (id: string, x: number, y: number, rad: number): number => {
    const arr = strokesOf.current.get(id) ?? [];
    for (let i = arr.length - 1; i >= 0; i--) { const s = arr[i]; if (s.tool !== 'pen') continue; for (const pt of s.pts) if ((pt.x - x) ** 2 + (pt.y - y) ** 2 <= rad * rad) return i; }
    return -1;
  };

  // 마운트: 로드(마이그레이션) + 사이즈 + 오버레이 핸들러 + 리사이즈.
  useEffect(() => {
    const wrap = wrapRef.current, over = overRef.current; if (!wrap || !over) return;
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        const d = JSON.parse(raw);
        if (Array.isArray(d)) { strokesOf.current.set('L1', d); } // v1(단일) → 마이그레이션
        else if (d?.v === 2) { strokesOf.current.clear(); for (const l of d.layers) strokesOf.current.set(l.id, d.strokes[l.id] ?? []); setLayers(d.layers); setActiveId(d.activeId ?? d.layers[0].id); }
      }
    } catch { /* */ }
    if (!strokesOf.current.has('L1') && strokesOf.current.size === 0) strokesOf.current.set('L1', []);

    const setupAll = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      sizeRef.current = { w: wrap.clientWidth, h: wrap.clientHeight, dpr };
      overCtx.current = sizeCanvas(over, true); // 진행 overlay만 저지연
      for (const [id, e] of elOf.current) { e.ctx = sizeCanvas(e.c); drawLayer(id); } // 확정 레이어=일반
    };
    setupAll();

    const pt = (e: PointerEvent): Pt => { const b = over.getBoundingClientRect(); return { x: e.clientX - b.left, y: e.clientY - b.top, p: e.pressure }; };
    const accept = (e: PointerEvent) => !(penSeen.current && e.pointerType === 'touch');
    const activeCtx = () => elOf.current.get(live.current.activeId)?.ctx ?? null;
    const renderOverlay = (predicted?: Pt[]) => {
      const ctx = overCtx.current; if (!ctx || !cur.current) return;
      ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); drawStroke(ctx, cur.current);
      if (predicted?.length) { const last = cur.current.pts[cur.current.pts.length - 1]; drawStroke(ctx, { ...cur.current, pts: [last, ...predicted] }); }
    };
    const eraseStrokeAt = (x: number, y: number) => {
      const id = live.current.activeId, idx = hit(id, x, y, ERASER_W);
      if (idx >= 0) { const [s] = (strokesOf.current.get(id) ?? []).splice(idx, 1); removed.current.push(s); drawLayer(id); }
    };

    const down = (e: PointerEvent) => {
      if (e.pointerType === 'pen') penSeen.current = true;
      if (!accept(e)) return; e.preventDefault();
      markPen(); // 펜 접촉 윈도우 갱신(다음 빠른 탭의 선택 콜아웃 차단)
      try { (window.getSelection?.())?.removeAllRanges?.(); } catch { /* iOS 선택 콜아웃 방지 */ }
      over.setPointerCapture(e.pointerId);
      const L = live.current;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { removed.current = []; const p0 = pt(e); eraseStrokeAt(p0.x, p0.y); cur.current = { tool: 'eraser', color: '', width: 0, dashed: false, pressure: false, pts: [] }; return; }
      redoStack.current = [];
      cur.current = { tool: L.tool, color: L.color, width: L.tool === 'eraser' ? ERASER_W : L.width, dashed: L.dashed, pressure: L.pressure, pts: [pt(e)] };
      if (L.tool === 'eraser') drawStroke(activeCtx()!, cur.current); else renderOverlay();
    };
    const move = (e: PointerEvent) => {
      if (!cur.current || !accept(e)) return; e.preventDefault();
      const L = live.current;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { const p = pt(e); eraseStrokeAt(p.x, p.y); return; }
      for (const ce of (e.getCoalescedEvents?.() ?? [e]) as PointerEvent[]) cur.current.pts.push(pt(ce));
      if (cur.current.tool === 'eraser') drawStroke(activeCtx()!, cur.current);
      else { const pred = cur.current.dashed ? [] : ((e as PE).getPredictedEvents?.() ?? []) as PointerEvent[]; renderOverlay(pred.map(pt)); }
    };
    const up = (e: PointerEvent) => {
      markPen(); // 손 뗀 직후 윈도우 갱신(획 직후 빠른 2번째 탭 차단)
      if (!cur.current) return; try { over.releasePointerCapture(e.pointerId); } catch { /* */ }
      const L = live.current, id = L.activeId;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { if (removed.current.length) { undoStack.current.push({ type: 'remove', layerId: id, strokes: removed.current.slice() }); save(); setRev((r) => r + 1); } cur.current = null; return; }
      if (cur.current.tool === 'pen') { drawStroke(activeCtx()!, cur.current); overCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); }
      (strokesOf.current.get(id) ?? strokesOf.current.set(id, []).get(id)!).push(cur.current);
      undoStack.current.push({ type: 'add', layerId: id, strokes: [cur.current] });
      cur.current = null; save(); setRev((r) => r + 1);
    };

    over.addEventListener('pointerdown', down); over.addEventListener('pointermove', move);
    over.addEventListener('pointerup', up); over.addEventListener('pointercancel', up);
    // ★iOS Safari 텍스트 선택 콜아웃(복사/번역 메뉴) 차단. ★핵심: 펜 빠른 2탭(짧은 간격)=iOS 더블탭 단어선택 제스처 → 콜아웃.
    //   "그리는 중(cur.current)"만으론 획과 획 사이 2번째 탭을 못 막음 → "최근 펜 접촉(recentPen)" 윈도우 동안 문서 전역 선택·더블클릭 차단.
    let penTimer: ReturnType<typeof setTimeout> | undefined;
    // recentPen 윈도우 동안 ①문서 전역 selectstart/dblclick 차단 ②★페이지 전체 -webkit-user-select:none
    //   (iOS 터치 더블탭 선택은 selectstart를 안 거칠 수 있어 CSS 비선택이 가장 확실).
    const markPen = () => {
      recentPen.current = true;
      document.body.style.setProperty('-webkit-user-select', 'none');
      if (penTimer) clearTimeout(penTimer);
      penTimer = setTimeout(() => { recentPen.current = false; document.body.style.removeProperty('-webkit-user-select'); }, 900);
    };
    const killSel = (ev: Event) => ev.preventDefault();
    const docSel = (ev: Event) => { if (cur.current || recentPen.current) ev.preventDefault(); };
    wrap.addEventListener('selectstart', killSel); wrap.addEventListener('contextmenu', killSel);
    over.addEventListener('contextmenu', killSel);
    document.addEventListener('selectstart', docSel); document.addEventListener('dblclick', docSel);
    const onResize = () => { if (cur.current) return; const w = wrap.clientWidth, h = wrap.clientHeight; if (!w || !h) return; if (w === sizeRef.current.w && h === sizeRef.current.h && overCtx.current) return; setupAll(); };
    const ro = new ResizeObserver(onResize); ro.observe(wrap);
    return () => {
      over.removeEventListener('pointerdown', down); over.removeEventListener('pointermove', move); over.removeEventListener('pointerup', up); over.removeEventListener('pointercancel', up);
      wrap.removeEventListener('selectstart', killSel); wrap.removeEventListener('contextmenu', killSel); over.removeEventListener('contextmenu', killSel);
      document.removeEventListener('selectstart', docSel); document.removeEventListener('dblclick', docSel);
      if (penTimer) clearTimeout(penTimer); document.body.style.removeProperty('-webkit-user-select');
      ro.disconnect();
    };
  }, [KEY, drawStroke, drawLayer, sizeCanvas, save]);

  // 새 레이어 캔버스(나중에 추가된)도 사이즈+그림 보장.
  useEffect(() => {
    if (!sizeRef.current.w) return;
    for (const [id, e] of elOf.current) if (!e.ctx) { e.ctx = sizeCanvas(e.c); drawLayer(id); }
  }, [layers, sizeCanvas, drawLayer]);

  const layerRef = useCallback((el: HTMLCanvasElement | null) => {
    if (!el) return; const id = el.dataset.lid!; if (!elOf.current.has(id) || elOf.current.get(id)!.c !== el) elOf.current.set(id, { c: el, ctx: sizeRef.current.w ? sizeCanvas(el) : null });
    if (elOf.current.get(id)!.ctx) drawLayer(id);
  }, [sizeCanvas, drawLayer]);

  // ── 레이어/undo 조작 ──
  const addLayer = () => { const id = nid(); strokesOf.current.set(id, []); setLayers((ls) => [...ls, { id, name: `레이어 ${ls.length + 1}`, visible: true }]); setActiveId(id); setRev((r) => r + 1); save(); };
  const delLayer = (id: string) => {
    if (layers.length <= 1) return; if (!confirm('이 레이어를 삭제할까요?')) return;
    strokesOf.current.delete(id); elOf.current.delete(id);
    const next = layers.filter((l) => l.id !== id); setLayers(next);
    if (activeId === id) setActiveId(next[0].id); setRev((r) => r + 1); save();
  };
  const toggleVis = (id: string) => { setLayers((ls) => ls.map((l) => l.id === id ? { ...l, visible: !l.visible } : l)); setRev((r) => r + 1); save(); };
  const rename = (id: string) => { const n = prompt('레이어 이름', layers.find((l) => l.id === id)?.name); if (n != null) { setLayers((ls) => ls.map((l) => l.id === id ? { ...l, name: n } : l)); save(); } };
  const moveLayer = (id: string, dir: -1 | 1) => { setLayers((ls) => { const i = ls.findIndex((l) => l.id === id), j = i + dir; if (j < 0 || j >= ls.length) return ls; const n = ls.slice(); [n[i], n[j]] = [n[j], n[i]]; return n; }); setRev((r) => r + 1); save(); };

  const undo = () => { const a = undoStack.current.pop(); if (!a) return; redoStack.current.push(a); const arr = strokesOf.current.get(a.layerId) ?? []; if (a.type === 'add') { for (const s of a.strokes) { const i = arr.indexOf(s); if (i >= 0) arr.splice(i, 1); } } else arr.push(...a.strokes); drawLayer(a.layerId); save(); setRev((r) => r + 1); };
  const redoFn = () => { const a = redoStack.current.pop(); if (!a) return; undoStack.current.push(a); const arr = strokesOf.current.get(a.layerId) ?? []; if (a.type === 'add') arr.push(...a.strokes); else for (const s of a.strokes) { const i = arr.indexOf(s); if (i >= 0) arr.splice(i, 1); } drawLayer(a.layerId); save(); setRev((r) => r + 1); };
  const clearActive = () => { const arr = strokesOf.current.get(activeId) ?? []; if (!arr.length || !confirm('이 레이어 필기를 지울까요?')) return; undoStack.current.push({ type: 'remove', layerId: activeId, strokes: arr.slice() }); arr.length = 0; drawLayer(activeId); save(); setRev((r) => r + 1); };

  // 썸네일: 레이어 strokes 를 작은 캔버스에 축소 렌더.
  const thumbRef = (id: string) => (el: HTMLCanvasElement | null) => {
    if (!el) return; const W = el.width, H = el.height; const ctx = el.getContext('2d'); if (!ctx) return;
    ctx.clearRect(0, 0, W, H); const sx = W / (sizeRef.current.w || 1), sy = H / (sizeRef.current.h || 1); const sc = Math.min(sx, sy);
    ctx.save(); ctx.scale(sc, sc); for (const s of strokesOf.current.get(id) ?? []) drawStroke(ctx, s); ctx.restore();
  };

  const RULE = 'color-mix(in oklab, var(--color-border) 55%, transparent)';
  const paperBg = () => paper === 'blank' ? 'none'
    : paper === 'ruled' ? `repeating-linear-gradient(to bottom, transparent 0, transparent ${gap - 1}px, ${RULE} ${gap - 1}px, ${RULE} ${gap}px)`
    : `repeating-linear-gradient(to bottom, transparent 0, transparent ${gap - 1}px, ${RULE} ${gap - 1}px, ${RULE} ${gap}px), repeating-linear-gradient(to right, transparent 0, transparent ${gap - 1}px, ${RULE} ${gap - 1}px, ${RULE} ${gap}px)`;

  const btn = (active: boolean): CSSProperties => ({ padding: '4px 9px', borderRadius: 8, fontSize: 13, cursor: 'pointer', lineHeight: 1.4, border: `1px solid ${active ? 'var(--color-accent)' : 'var(--color-border)'}`, background: active ? 'color-mix(in oklab, var(--color-accent) 16%, transparent)' : 'var(--color-surface)', color: active ? 'var(--color-accent)' : 'var(--color-text)' });
  const sep = <span style={{ width: 1, height: 18, background: 'var(--color-border)', margin: '0 2px' }} />;

  return (
    <div style={full ? { position: 'fixed', inset: 0, zIndex: 1000, background: 'var(--color-bg)', display: 'flex', flexDirection: 'column', padding: 10, gap: 8 } : { display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <button style={btn(tool === 'pen')} onClick={() => setTool('pen')}>✏️ 펜</button>
        <button style={btn(tool === 'eraser')} onClick={() => setTool('eraser')}>지우개</button>
        {tool === 'eraser' && (<>
          <button style={btn(eraserMode === 'precise')} onClick={() => setEraserMode('precise')}>정밀</button>
          <button style={btn(eraserMode === 'stroke')} onClick={() => setEraserMode('stroke')}>획</button>
        </>)}
        {sep}
        {COLORS.map((c) => (<button key={c} onClick={() => { setColor(c); setTool('pen'); }} title={c} style={{ width: 20, height: 20, borderRadius: '50%', background: c, cursor: 'pointer', border: color === c ? '2px solid var(--color-accent)' : '2px solid var(--color-border)' }} />))}
        {WIDTHS.map((w) => (<button key={w} onClick={() => setWidth(w)} style={btn(width === w)}><span style={{ display: 'inline-block', width: 16, height: w + 2, borderRadius: 99, background: 'currentColor', verticalAlign: 'middle' }} /></button>))}
        <button style={btn(dashed)} onClick={() => setDashed((v) => !v)} title="점선/실선">{dashed ? '┈ 점선' : '─ 실선'}</button>
        <button style={btn(pressure)} onClick={() => setPressure((v) => !v)} title="필압(수학엔 무감지 권장)">{pressure ? '✍️ 필압' : '═ 균일'}</button>
        {sep}
        <select value={paper} onChange={(e) => setPaper(e.target.value as Paper)} style={{ ...btn(false), padding: '4px 6px' }} title="종이"><option value="blank">백지</option><option value="ruled">줄</option><option value="grid">격자</option></select>
        {paper !== 'blank' && <input type="range" min={14} max={48} value={gap} onChange={(e) => setGap(+e.target.value)} title={`간격 ${gap}px`} style={{ width: 64 }} />}
        <span style={{ flex: 1 }} />
        <button style={btn(panel)} onClick={() => setPanel((v) => !v)} title="레이어">▤ 레이어</button>
        <button style={btn(false)} onClick={undo}>↶</button>
        <button style={btn(false)} onClick={redoFn}>↷</button>
        <button style={btn(false)} onClick={clearActive}>레이어지움</button>
        <button style={btn(full)} onClick={() => setFull((v) => !v)}>{full ? '✕ 닫기' : '⛶ 전체화면'}</button>
      </div>
      <div style={{ display: 'flex', gap: 8, flex: full ? 1 : undefined, minHeight: 0 }}>
        <div ref={wrapRef} style={{ position: 'relative', flex: 1, height: full ? undefined : height, borderRadius: 12, border: '1px solid var(--color-border)', overflow: 'hidden', background: 'var(--color-surface)', touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none', backgroundImage: paperBg() }}>
          {layers.map((l, i) => (<canvas key={l.id} data-lid={l.id} ref={layerRef} style={{ position: 'absolute', inset: 0, zIndex: i, display: l.visible ? 'block' : 'none', touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }} />))}
          <canvas ref={overRef} style={{ position: 'absolute', inset: 0, zIndex: 998, touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }} />
        </div>
        {panel && (
          <div style={{ width: 168, flexShrink: 0, display: 'flex', flexDirection: 'column', gap: 6, padding: 8, borderRadius: 12, border: '1px solid var(--color-border)', background: 'var(--color-surface)', overflowY: 'auto', maxHeight: full ? undefined : height + 46 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--color-muted)' }}>레이어</span>
              <button style={btn(false)} onClick={addLayer}>＋</button>
            </div>
            {[...layers].reverse().map((l) => (
              <div key={l.id} onClick={() => setActiveId(l.id)} style={{ display: 'flex', flexDirection: 'column', gap: 3, padding: 5, borderRadius: 8, cursor: 'pointer', border: `1px solid ${activeId === l.id ? 'var(--color-accent)' : 'var(--color-border)'}`, background: activeId === l.id ? 'color-mix(in oklab, var(--color-accent) 10%, transparent)' : 'transparent' }}>
                <canvas key={`${l.id}-${rev}`} ref={thumbRef(l.id)} width={148} height={84} style={{ width: '100%', height: 'auto', borderRadius: 5, border: '1px solid var(--color-border)', background: 'var(--color-surface)', opacity: l.visible ? 1 : 0.35 }} />
                <div style={{ display: 'flex', alignItems: 'center', gap: 3, fontSize: 11 }}>
                  <button onClick={(e) => { e.stopPropagation(); toggleVis(l.id); }} title="표시/숨김" style={{ cursor: 'pointer', border: 'none', background: 'transparent', fontSize: 13 }}>{l.visible ? '👁' : '🚫'}</button>
                  <span onDoubleClick={(e) => { e.stopPropagation(); rename(l.id); }} style={{ flex: 1, color: 'var(--color-text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{l.name}</span>
                  <button onClick={(e) => { e.stopPropagation(); moveLayer(l.id, 1); }} title="위로" style={{ cursor: 'pointer', border: 'none', background: 'transparent', color: 'var(--color-muted)' }}>▲</button>
                  <button onClick={(e) => { e.stopPropagation(); moveLayer(l.id, -1); }} title="아래로" style={{ cursor: 'pointer', border: 'none', background: 'transparent', color: 'var(--color-muted)' }}>▼</button>
                  <button onClick={(e) => { e.stopPropagation(); delLayer(l.id); }} title="삭제" style={{ cursor: 'pointer', border: 'none', background: 'transparent', color: 'var(--color-mastery-unknown)' }}>✕</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
