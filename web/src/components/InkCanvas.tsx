import { useRef, useEffect, useState, useCallback, type CSSProperties } from 'react';

// 저지연 필기 캔버스 — 애플펜슬/S펜/터치/마우스. 채점·LLM·API 무관(순수 필기).
//   저지연: ① desynchronized 컨텍스트 ② getCoalescedEvents(240Hz 중간점) ③ getPredictedEvents(예측 잉크)
//           ④ 2레이어(확정 base / 진행 overlay) ⑤ 압력 굵기 ⑥ 팜리젝션
//   벡터 스트로크 모델 → 선택·변형·재색·스냅의 토대. 영속=localStorage(per storageKey, 후속 DB).
//   스펙·로드맵: docs/architecture/handwriting-canvas.md
// getPredictedEvents는 lib.dom 버전에 따라 없을 수 있어 느슨한 타입으로 받는다.
type PE = PointerEvent & { getPredictedEvents?: () => PointerEvent[] };

type Pt = { x: number; y: number; p: number };
// 설정을 획에 박아 재그림이 일관되게(점선·압력 여부 포함).
type Stroke = { tool: 'pen' | 'eraser'; color: string; width: number; dashed: boolean; pressure: boolean; pts: Pt[] };
type Action = { add: Stroke } | { remove: Stroke[] };

type Paper = 'blank' | 'ruled' | 'grid';
const COLORS = ['#2A261E', '#39487D', '#C13D38', '#2E7B4F']; // 잉크·파랑·빨강·초록
const WIDTHS = [1.5, 2.5, 4];
const ERASER_W = 18; // 정밀 지우개 굵기

export default function InkCanvas({ storageKey, height = 560 }: { storageKey: string; height?: number }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const baseRef = useRef<HTMLCanvasElement>(null);
  const overRef = useRef<HTMLCanvasElement>(null);
  const baseCtx = useRef<CanvasRenderingContext2D | null>(null);
  const overCtx = useRef<CanvasRenderingContext2D | null>(null);
  const strokes = useRef<Stroke[]>([]);
  const undoStack = useRef<Action[]>([]);
  const redoStack = useRef<Action[]>([]);
  const cur = useRef<Stroke | null>(null);
  const removedThisGesture = useRef<Stroke[]>([]);
  const penSeen = useRef(false);
  const sizeRef = useRef({ w: 0, h: 0, dpr: 1 });

  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');
  const [eraserMode, setEraserMode] = useState<'precise' | 'stroke'>('precise');
  const [pressure, setPressure] = useState(false); // ★수학엔 무감지(균일선) 기본
  const [dashed, setDashed] = useState(false);
  const [color, setColor] = useState(COLORS[0]);
  const [width, setWidth] = useState(WIDTHS[1]);
  const [paper, setPaper] = useState<Paper>('grid');
  const [gap, setGap] = useState(24);
  const [full, setFull] = useState(false);
  // 핸들러는 native listener라 최신값을 ref로 읽는다.
  const r = { tool, eraserMode, pressure, dashed, color, width };
  const live = useRef(r); live.current = r;

  const KEY = `ink:${storageKey}`;
  const pw = (s: Stroke, p: number) => s.pressure ? s.width * (0.45 + 1.3 * (p > 0 ? p : 0.5)) : s.width;

  const drawStroke = useCallback((ctx: CanvasRenderingContext2D, s: Stroke) => {
    if (s.pts.length === 0) return;
    ctx.save();
    ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = s.tool === 'eraser' ? 'destination-out' : 'source-over';
    ctx.strokeStyle = s.color;
    const isDash = s.dashed && s.tool === 'pen';
    if (s.pts.length === 1) {
      const a = s.pts[0]; ctx.fillStyle = s.color; ctx.beginPath();
      ctx.arc(a.x, a.y, pw(s, a.p) / 2, 0, Math.PI * 2); ctx.fill(); ctx.restore(); return;
    }
    if (isDash) {
      // ★점선: 전체 경로를 한 path로 → dash가 "경로 길이" 기준 균일(펜 속도·점간격 무관). 압력 무시(균일 굵기).
      ctx.lineCap = 'butt'; ctx.lineWidth = s.width;
      ctx.setLineDash([s.width * 2.6, s.width * 3]);
      ctx.beginPath(); ctx.moveTo(s.pts[0].x, s.pts[0].y);
      for (let i = 1; i < s.pts.length; i++) ctx.lineTo(s.pts[i].x, s.pts[i].y);
      ctx.stroke();
    } else {
      // 실선: 세그먼트별(압력 굵기 가변). round cap으로 매끈.
      ctx.lineCap = 'round'; ctx.setLineDash([]);
      for (let i = 1; i < s.pts.length; i++) {
        const a = s.pts[i - 1], b = s.pts[i];
        ctx.beginPath(); ctx.lineWidth = pw(s, (a.p + b.p) / 2);
        ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
    ctx.restore();
  }, []);

  const redrawBase = useCallback(() => {
    const ctx = baseCtx.current; if (!ctx) return;
    ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
    for (const s of strokes.current) drawStroke(ctx, s);
  }, [drawStroke]);

  const renderOverlay = useCallback((predicted?: Pt[]) => {
    const ctx = overCtx.current; if (!ctx || !cur.current) return;
    ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
    drawStroke(ctx, cur.current);
    if (predicted?.length) {
      const last = cur.current.pts[cur.current.pts.length - 1];
      drawStroke(ctx, { ...cur.current, pts: [last, ...predicted] });
    }
  }, [drawStroke]);

  const save = useCallback(() => {
    try { localStorage.setItem(KEY, JSON.stringify(strokes.current)); } catch { /* quota */ }
  }, [KEY]);

  // 획 지우개: (x,y) 근처를 지나는 펜 획 index (없으면 -1).
  const hitStroke = (x: number, y: number, rad: number): number => {
    for (let i = strokes.current.length - 1; i >= 0; i--) {
      const s = strokes.current[i]; if (s.tool !== 'pen') continue;
      for (const pt of s.pts) { if ((pt.x - x) ** 2 + (pt.y - y) ** 2 <= rad * rad) return i; }
    }
    return -1;
  };

  useEffect(() => {
    const wrap = wrapRef.current, base = baseRef.current, over = overRef.current;
    if (!wrap || !base || !over) return;
    const setup = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      const w = wrap.clientWidth, h = wrap.clientHeight;
      sizeRef.current = { w, h, dpr };
      for (const c of [base, over]) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); c.style.width = w + 'px'; c.style.height = h + 'px'; }
      const opt = { desynchronized: true } as CanvasRenderingContext2DSettings;
      baseCtx.current = base.getContext('2d', opt); overCtx.current = over.getContext('2d', opt);
      for (const ctx of [baseCtx.current, overCtx.current]) ctx?.scale(dpr, dpr);
      redrawBase();
    };
    try { const raw = localStorage.getItem(KEY); if (raw) strokes.current = JSON.parse(raw); } catch { /* */ }
    setup();

    const pt = (e: PointerEvent): Pt => { const b = over.getBoundingClientRect(); return { x: e.clientX - b.left, y: e.clientY - b.top, p: e.pressure }; };
    const accept = (e: PointerEvent) => !(penSeen.current && e.pointerType === 'touch');

    const eraseStrokeAt = (x: number, y: number) => {
      const idx = hitStroke(x, y, ERASER_W);
      if (idx >= 0) { const [s] = strokes.current.splice(idx, 1); removedThisGesture.current.push(s); redrawBase(); }
    };

    const down = (e: PointerEvent) => {
      if (e.pointerType === 'pen') penSeen.current = true;
      if (!accept(e)) return; e.preventDefault();
      over.setPointerCapture(e.pointerId);
      const L = live.current;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { removedThisGesture.current = []; const p0 = pt(e); eraseStrokeAt(p0.x, p0.y); cur.current = { tool: 'eraser', color: '', width: 0, dashed: false, pressure: false, pts: [] }; return; }
      redoStack.current = [];
      cur.current = { tool: L.tool, color: L.color, width: L.tool === 'eraser' ? ERASER_W : L.width, dashed: L.dashed, pressure: L.pressure, pts: [pt(e)] };
      if (L.tool === 'eraser') redrawBase(); else renderOverlay();
    };
    const move = (e: PointerEvent) => {
      if (!cur.current || !accept(e)) return; e.preventDefault();
      const L = live.current;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { const p = pt(e); eraseStrokeAt(p.x, p.y); return; }
      const coalesced = (e.getCoalescedEvents?.() ?? [e]) as PointerEvent[];
      for (const ce of coalesced) cur.current.pts.push(pt(ce));
      if (cur.current.tool === 'eraser') drawStroke(baseCtx.current!, cur.current); // 정밀: base에 즉시(풀 경로 유지)
      else { const pred = cur.current.dashed ? [] : ((e as PE).getPredictedEvents?.() ?? []) as PointerEvent[]; renderOverlay(pred.map(pt)); } // 점선은 예측 끔(끝 dash 리셋 방지)
    };
    const up = (e: PointerEvent) => {
      if (!cur.current) return;
      try { over.releasePointerCapture(e.pointerId); } catch { /* */ }
      const L = live.current;
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') {
        if (removedThisGesture.current.length) { undoStack.current.push({ remove: removedThisGesture.current.slice() }); save(); }
        cur.current = null; return;
      }
      if (cur.current.tool === 'pen') { drawStroke(baseCtx.current!, cur.current); overCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); }
      strokes.current.push(cur.current);
      undoStack.current.push({ add: cur.current });
      cur.current = null; save();
    };

    over.addEventListener('pointerdown', down);
    over.addEventListener('pointermove', move);
    over.addEventListener('pointerup', up);
    over.addEventListener('pointercancel', up);
    const onResize = () => {
      if (cur.current) return;
      const w = wrap.clientWidth, h = wrap.clientHeight;
      if (!w || !h) return;
      if (w === sizeRef.current.w && h === sizeRef.current.h && baseCtx.current) return;
      setup();
    };
    const ro = new ResizeObserver(onResize); ro.observe(wrap);
    return () => {
      over.removeEventListener('pointerdown', down); over.removeEventListener('pointermove', move);
      over.removeEventListener('pointerup', up); over.removeEventListener('pointercancel', up);
      ro.disconnect();
    };
  }, [KEY, redrawBase, renderOverlay, drawStroke, save]);

  const undo = () => {
    const a = undoStack.current.pop(); if (!a) return; redoStack.current.push(a);
    if ('add' in a) { const i = strokes.current.indexOf(a.add); if (i >= 0) strokes.current.splice(i, 1); }
    else strokes.current.push(...a.remove);
    redrawBase(); save();
  };
  const redoFn = () => {
    const a = redoStack.current.pop(); if (!a) return; undoStack.current.push(a);
    if ('add' in a) strokes.current.push(a.add);
    else for (const s of a.remove) { const i = strokes.current.indexOf(s); if (i >= 0) strokes.current.splice(i, 1); }
    redrawBase(); save();
  };
  const clear = () => { if (!strokes.current.length || !confirm('필기를 모두 지울까요?')) return; undoStack.current.push({ remove: strokes.current.slice() }); strokes.current = []; redrawBase(); save(); };

  const RULE = 'color-mix(in oklab, var(--color-border) 55%, transparent)';
  const paperBg = (): string => {
    if (paper === 'blank') return 'none';
    const horiz = `repeating-linear-gradient(to bottom, transparent 0, transparent ${gap - 1}px, ${RULE} ${gap - 1}px, ${RULE} ${gap}px)`;
    const vert = `repeating-linear-gradient(to right, transparent 0, transparent ${gap - 1}px, ${RULE} ${gap - 1}px, ${RULE} ${gap}px)`;
    return paper === 'ruled' ? horiz : `${horiz}, ${vert}`;
  };

  const btn = (active: boolean): CSSProperties => ({
    padding: '4px 9px', borderRadius: 8, fontSize: 13, cursor: 'pointer', lineHeight: 1.4,
    border: `1px solid ${active ? 'var(--color-accent)' : 'var(--color-border)'}`,
    background: active ? 'color-mix(in oklab, var(--color-accent) 16%, transparent)' : 'var(--color-surface)',
    color: active ? 'var(--color-accent)' : 'var(--color-text)',
  });
  const sep = <span style={{ width: 1, height: 18, background: 'var(--color-border)', margin: '0 2px' }} />;

  return (
    <div style={full
      ? { position: 'fixed', inset: 0, zIndex: 1000, background: 'var(--color-bg)', display: 'flex', flexDirection: 'column', padding: 10, gap: 8 }
      : { display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <button style={btn(tool === 'pen')} onClick={() => setTool('pen')}>✏️ 펜</button>
        <button style={btn(tool === 'eraser')} onClick={() => setTool('eraser')}>지우개</button>
        {tool === 'eraser' && (<>
          <button style={btn(eraserMode === 'precise')} onClick={() => setEraserMode('precise')}>정밀</button>
          <button style={btn(eraserMode === 'stroke')} onClick={() => setEraserMode('stroke')}>획</button>
        </>)}
        {sep}
        {COLORS.map((c) => (
          <button key={c} onClick={() => { setColor(c); setTool('pen'); }} title={c}
            style={{ width: 20, height: 20, borderRadius: '50%', background: c, cursor: 'pointer', border: color === c ? '2px solid var(--color-accent)' : '2px solid var(--color-border)' }} />
        ))}
        {WIDTHS.map((w) => (
          <button key={w} onClick={() => setWidth(w)} style={btn(width === w)}>
            <span style={{ display: 'inline-block', width: 16, height: w + 2, borderRadius: 99, background: 'currentColor', verticalAlign: 'middle' }} />
          </button>
        ))}
        <button style={btn(dashed)} onClick={() => setDashed((v) => !v)} title="점선/실선">{dashed ? '┈ 점선' : '─ 실선'}</button>
        <button style={btn(pressure)} onClick={() => setPressure((v) => !v)} title="필압 감지(수학엔 무감지 권장)">{pressure ? '✍️ 필압' : '═ 균일'}</button>
        {sep}
        <select value={paper} onChange={(e) => setPaper(e.target.value as Paper)} style={{ ...btn(false), padding: '4px 6px' }} title="종이">
          <option value="blank">백지</option><option value="ruled">줄</option><option value="grid">격자</option>
        </select>
        {paper !== 'blank' && (
          <input type="range" min={14} max={48} value={gap} onChange={(e) => setGap(+e.target.value)} title={`간격 ${gap}px`} style={{ width: 70 }} />
        )}
        <span style={{ flex: 1 }} />
        <button style={btn(false)} onClick={undo}>↶</button>
        <button style={btn(false)} onClick={redoFn}>↷</button>
        <button style={btn(false)} onClick={clear}>전체지움</button>
        <button style={btn(full)} onClick={() => setFull((v) => !v)}>{full ? '✕ 닫기' : '⛶ 전체화면'}</button>
      </div>
      <div ref={wrapRef} style={{
        position: 'relative', flex: full ? 1 : undefined, height: full ? undefined : height,
        borderRadius: 12, border: '1px solid var(--color-border)', overflow: 'hidden',
        background: 'var(--color-surface)', touchAction: 'none',
        userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none',
        backgroundImage: paperBg(),
      }}>
        <canvas ref={baseRef} style={{ position: 'absolute', inset: 0, touchAction: 'none' }} />
        <canvas ref={overRef} style={{ position: 'absolute', inset: 0, touchAction: 'none' }} />
      </div>
    </div>
  );
}
