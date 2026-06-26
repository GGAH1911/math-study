import { useRef, useEffect, useState, useCallback, type CSSProperties } from 'react';

// getPredictedEvents는 lib.dom 버전에 따라 없을 수 있어 느슨한 타입으로 받는다.
type PE = PointerEvent & { getPredictedEvents?: () => PointerEvent[] };

// 저지연 필기 캔버스 — 애플펜슬/S펜/터치/마우스. 채점·LLM·API 무관(순수 필기).
//   저지연 기법:
//   ① desynchronized 캔버스 컨텍스트 — 합성 파이프라인 일부 우회(잉크 앱 전용 힌트)
//   ② getCoalescedEvents() — 프레임 사이 고주파(240Hz) 중간점 전부 받아 매끈
//   ③ getPredictedEvents() — 펜 앞 1~2프레임 예측 잉크를 오버레이에 미리 그림(체감 지연↓)
//   ④ 2-레이어 — 확정 획=base 캔버스(커밋 때만 갱신), 진행 획+예측=overlay(매 프레임 클리어·재그림)
//   ⑤ 압력 굵기(e.pressure) + 팜리젝션(펜 감지 시 손바닥 touch 무시)
//   영속: localStorage(per storageKey). DB 저장은 후속.

type Pt = { x: number; y: number; p: number };
type Stroke = { tool: 'pen' | 'eraser'; color: string; width: number; pts: Pt[] };

const COLORS = ['#2A261E', '#39487D', '#C13D38', '#2E7B4F']; // 잉크·파랑·빨강·초록
const WIDTHS = [1.5, 2.5, 4];

export default function InkCanvas({ storageKey, height = 560 }: { storageKey: string; height?: number }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const baseRef = useRef<HTMLCanvasElement>(null);
  const overRef = useRef<HTMLCanvasElement>(null);
  const baseCtx = useRef<CanvasRenderingContext2D | null>(null);
  const overCtx = useRef<CanvasRenderingContext2D | null>(null);
  const strokes = useRef<Stroke[]>([]);
  const redo = useRef<Stroke[]>([]);
  const cur = useRef<Stroke | null>(null);
  const penSeen = useRef(false);
  const sizeRef = useRef({ w: 0, h: 0, dpr: 1 });

  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');
  const [color, setColor] = useState(COLORS[0]);
  const [width, setWidth] = useState(WIDTHS[1]);
  const [full, setFull] = useState(false);
  const toolRef = useRef(tool); toolRef.current = tool;
  const colorRef = useRef(color); colorRef.current = color;
  const widthRef = useRef(width); widthRef.current = width;

  const KEY = `ink:${storageKey}`;

  // 압력 → 굵기 (펜 없으면 pressure 0 → 중간값)
  const pw = (base: number, p: number) => base * (0.45 + 1.3 * (p > 0 ? p : 0.5));

  // 한 획을 ctx에 그림. 세그먼트별 round-cap + 압력 굵기. 지우개는 destination-out.
  const drawStroke = useCallback((ctx: CanvasRenderingContext2D, s: Stroke) => {
    if (s.pts.length === 0) return;
    ctx.save();
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = s.tool === 'eraser' ? 'destination-out' : 'source-over';
    ctx.strokeStyle = s.color;
    if (s.pts.length === 1) {
      const a = s.pts[0];
      ctx.beginPath(); ctx.fillStyle = s.color;
      ctx.arc(a.x, a.y, pw(s.width, a.p) / 2, 0, Math.PI * 2); ctx.fill();
      ctx.restore(); return;
    }
    for (let i = 1; i < s.pts.length; i++) {
      const a = s.pts[i - 1], b = s.pts[i];
      ctx.beginPath();
      ctx.lineWidth = pw(s.width, (a.p + b.p) / 2);
      ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }
    ctx.restore();
  }, []);

  const redrawBase = useCallback(() => {
    const ctx = baseCtx.current; if (!ctx) return;
    const { w, h } = sizeRef.current;
    ctx.clearRect(0, 0, w, h);
    for (const s of strokes.current) drawStroke(ctx, s);
  }, [drawStroke]);

  const renderOverlay = useCallback((predicted?: Pt[]) => {
    const ctx = overCtx.current; if (!ctx || !cur.current) return;
    const { w, h } = sizeRef.current;
    ctx.clearRect(0, 0, w, h);
    drawStroke(ctx, cur.current);
    if (predicted && predicted.length) {
      const last = cur.current.pts[cur.current.pts.length - 1];
      drawStroke(ctx, { ...cur.current, pts: [last, ...predicted] });
    }
  }, [drawStroke]);

  const save = useCallback(() => {
    try { localStorage.setItem(KEY, JSON.stringify(strokes.current)); } catch { /* quota */ }
  }, [KEY]);

  // 캔버스 크기 셋업(retina) + 로드 + 리스너.
  useEffect(() => {
    const wrap = wrapRef.current, base = baseRef.current, over = overRef.current;
    if (!wrap || !base || !over) return;

    const setup = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      const w = wrap.clientWidth, h = wrap.clientHeight;
      sizeRef.current = { w, h, dpr };
      for (const c of [base, over]) {
        c.width = Math.round(w * dpr); c.height = Math.round(h * dpr);
        c.style.width = w + 'px'; c.style.height = h + 'px';
      }
      const opt = { desynchronized: true } as CanvasRenderingContext2DSettings;
      baseCtx.current = base.getContext('2d', opt); overCtx.current = over.getContext('2d', opt);
      for (const ctx of [baseCtx.current, overCtx.current]) ctx?.scale(dpr, dpr);
      redrawBase();
    };

    // 로드
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) strokes.current = JSON.parse(raw);
    } catch { /* ignore */ }
    setup();

    const pt = (e: PointerEvent): Pt => {
      const r = over.getBoundingClientRect();
      return { x: e.clientX - r.left, y: e.clientY - r.top, p: e.pressure };
    };
    const accept = (e: PointerEvent) => !(penSeen.current && e.pointerType === 'touch');

    const down = (e: PointerEvent) => {
      if (e.pointerType === 'pen') penSeen.current = true;
      if (!accept(e)) return;
      e.preventDefault();
      over.setPointerCapture(e.pointerId);
      redo.current = [];
      cur.current = { tool: toolRef.current, color: colorRef.current, width: widthRef.current, pts: [pt(e)] };
      if (toolRef.current === 'eraser') redrawBase(); // 지우개는 base에 직접
      else renderOverlay();
    };
    const move = (e: PointerEvent) => {
      if (!cur.current || !accept(e)) return;
      e.preventDefault();
      const coalesced = (e.getCoalescedEvents?.() ?? [e]) as PointerEvent[];
      for (const ce of coalesced) cur.current.pts.push(pt(ce));
      if (cur.current.tool === 'eraser') {
        // 지우개: base에 즉시 적용(destination-out). ★풀 경로 유지 → 저장/재그림 시 동일하게 지워짐.
        //   (destination-out은 같은 픽셀 반복 지워도 동일 = 매 프레임 풀 재그림 무해. 1점 저장 버그 수정.)
        drawStroke(baseCtx.current!, cur.current);
      } else {
        const pred = ((e as PE).getPredictedEvents?.() ?? []) as PointerEvent[];
        renderOverlay(pred.map(pt));
      }
    };
    const up = (e: PointerEvent) => {
      if (!cur.current) return;
      try { over.releasePointerCapture(e.pointerId); } catch { /* */ }
      if (cur.current.tool === 'pen') {
        drawStroke(baseCtx.current!, cur.current); // 확정 → base
        overCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
      }
      strokes.current.push(cur.current);
      cur.current = null;
      save();
    };

    over.addEventListener('pointerdown', down);
    over.addEventListener('pointermove', move);
    over.addEventListener('pointerup', up);
    over.addEventListener('pointercancel', up);
    const onResize = () => {
      if (cur.current) return;                            // 그리는 중엔 재설정 금지
      const w = wrap.clientWidth, h = wrap.clientHeight;
      if (!w || !h) return;                               // 숨김(details 닫힘·display:none) → 스킵
      if (w === sizeRef.current.w && h === sizeRef.current.h && baseCtx.current) return; // 변화 없음
      setup();                                            // 크기 변할 때만(상태=strokes는 redrawBase로 보존)
    };
    const ro = new ResizeObserver(onResize);
    ro.observe(wrap);
    return () => {
      over.removeEventListener('pointerdown', down);
      over.removeEventListener('pointermove', move);
      over.removeEventListener('pointerup', up);
      over.removeEventListener('pointercancel', up);
      ro.disconnect();
    };
  }, [KEY, redrawBase, renderOverlay, drawStroke, save, full]);

  const undo = () => { const s = strokes.current.pop(); if (s) { redo.current.push(s); redrawBase(); save(); } };
  const redoFn = () => { const s = redo.current.pop(); if (s) { strokes.current.push(s); redrawBase(); save(); } };
  const clear = () => { if (!strokes.current.length || !confirm('필기를 모두 지울까요?')) return; redo.current = strokes.current.slice(); strokes.current = []; redrawBase(); save(); };

  const btn = (active: boolean): CSSProperties => ({
    padding: '4px 9px', borderRadius: 8, fontSize: 13, cursor: 'pointer', lineHeight: 1.4,
    border: `1px solid ${active ? 'var(--color-accent)' : 'var(--color-border)'}`,
    background: active ? 'color-mix(in oklab, var(--color-accent) 16%, transparent)' : 'var(--color-surface)',
    color: active ? 'var(--color-accent)' : 'var(--color-text)',
  });

  return (
    <div style={full
      ? { position: 'fixed', inset: 0, zIndex: 1000, background: 'var(--color-bg)', display: 'flex', flexDirection: 'column', padding: 10 }
      : { display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <button style={btn(tool === 'pen')} onClick={() => setTool('pen')}>✏️ 펜</button>
        <button style={btn(tool === 'eraser')} onClick={() => setTool('eraser')}>지우개</button>
        <span style={{ width: 1, height: 18, background: 'var(--color-border)', margin: '0 2px' }} />
        {COLORS.map((c) => (
          <button key={c} onClick={() => { setColor(c); setTool('pen'); }} title={c}
            style={{ width: 20, height: 20, borderRadius: '50%', background: c, cursor: 'pointer',
              border: color === c ? '2px solid var(--color-accent)' : '2px solid var(--color-border)' }} />
        ))}
        <span style={{ width: 1, height: 18, background: 'var(--color-border)', margin: '0 2px' }} />
        {WIDTHS.map((w) => (
          <button key={w} onClick={() => setWidth(w)} style={btn(width === w)}>
            <span style={{ display: 'inline-block', width: 16, height: w + 2, borderRadius: 99, background: 'currentColor', verticalAlign: 'middle' }} />
          </button>
        ))}
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
        userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none', // 펜 드래그 시 텍스트 선택(파란 하이라이트) 차단
        backgroundImage: 'radial-gradient(color-mix(in oklab, var(--color-border) 60%, transparent) 0.7px, transparent 0.7px)',
        backgroundSize: '22px 22px',
      }}>
        <canvas ref={baseRef} style={{ position: 'absolute', inset: 0, touchAction: 'none' }} />
        <canvas ref={overRef} style={{ position: 'absolute', inset: 0, touchAction: 'none' }} />
      </div>
    </div>
  );
}
