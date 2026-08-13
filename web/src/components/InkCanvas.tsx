import { useRef, useEffect, useState, useCallback, type CSSProperties } from 'react';
import { recognizeShape, shapeToPoints } from '../lib/shape-recognize'; // 도형 모드: 손그림→깔끔한 도형 스냅
import { normalizeInkDoc, INK_DOC_VERSION } from '../lib/ink-doc.ts';

// 저지연 필기 캔버스 + 레이어 — 애플펜슬/S펜/터치/마우스. 채점·LLM·API 무관.
//   저지연: desynchronized · getCoalescedEvents · getPredictedEvents · 진행 overlay · 압력 · 팜리젝션
//   레이어: ★스택형 per-layer 캔버스 — 가시 토글=display, 지우개 격리=그 레이어에 destination-out(자동).
//   벡터 스트로크 모델(선택·변형 토대). 영속=localStorage(per storageKey, v2 레이어 포맷). 스펙: docs/architecture/handwriting-canvas.md
type PE = PointerEvent & { getPredictedEvents?: () => PointerEvent[] };
type Pt = { x: number; y: number; p: number };
type Stroke = { tool: 'pen' | 'eraser'; color: string; width: number; dashed: boolean; pressure: boolean; pts: Pt[] };
type LayerMeta = { id: string; name: string; visible: boolean };
type Action =
  | { type: 'add'; layerId: string; strokes: Stroke[] }
  | { type: 'remove'; layerId: string; strokes: Stroke[] }
  | { type: 'mutate'; layerId: string; idxs: number[]; before: Stroke[]; after: Stroke[] } // 이동·재색(객체 교체)
  | { type: 'move'; from: string; to: string; strokes: Stroke[] };                          // 레이어 이동
type Paper = 'blank' | 'ruled' | 'grid';
type Tool = 'pen' | 'eraser' | 'select' | 'shape';
type Sel = { layerId: string; idxs: number[] };

const COLORS = ['#2A261E', '#39487D', '#C13D38', '#2E7B4F'];
const WIDTHS = [1.5, 2.5, 4];
const ERASER_SIZES = [12, 24, 44]; // 지우개 지름(px) — 소/중/대
const nid = () => 'L' + Math.random().toString(36).slice(2, 8);
// 갈무리(선택) 기하 헬퍼
const pointInPoly = (x: number, y: number, poly: Pt[]): boolean => {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i].x, yi = poly[i].y, xj = poly[j].x, yj = poly[j].y;
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside;
  }
  return inside;
};
const bboxOf = (arr: Stroke[], idxs: number[]) => {
  let a = Infinity, b = Infinity, c = -Infinity, d = -Infinity;
  for (const i of idxs) for (const p of arr[i]?.pts ?? []) { if (p.x < a) a = p.x; if (p.y < b) b = p.y; if (p.x > c) c = p.x; if (p.y > d) d = p.y; }
  return a === Infinity ? null : { x: a, y: b, w: c - a, h: d - b };
};
const translateStroke = (s: Stroke, dx: number, dy: number): Stroke => ({ ...s, pts: s.pts.map((p) => ({ x: p.x + dx, y: p.y + dy, p: p.p })) });
// 직선 도구: 시작→현재를 45° 격자에 가까우면 스냅(축·대각선 정밀).
const snapAngle = (s: Pt, c: Pt): Pt => {
  const dx = c.x - s.x, dy = c.y - s.y, len = Math.hypot(dx, dy); if (len < 2) return c;
  let ang = Math.atan2(dy, dx); const step = Math.PI / 4, snapped = Math.round(ang / step) * step;
  if (Math.abs(ang - snapped) < 0.12) ang = snapped; // ~7°
  return { x: s.x + Math.cos(ang) * len, y: s.y + Math.sin(ang) * len, p: c.p };
};
const snapGrid = (p: Pt, gap: number): Pt => ({ x: Math.round(p.x / gap) * gap, y: Math.round(p.y / gap) * gap, p: p.p });
// 점→선분 최단거리 (획 지우개가 2점 직선의 중간도 잡도록).
const distToSeg = (px: number, py: number, ax: number, ay: number, bx: number, by: number): number => {
  const dx = bx - ax, dy = by - ay, len2 = dx * dx + dy * dy;
  let t = len2 ? ((px - ax) * dx + (py - ay) * dy) / len2 : 0; t = t < 0 ? 0 : t > 1 ? 1 : t;
  return Math.hypot(px - (ax + t * dx), py - (ay + t * dy));
};

// 펜/종이 설정은 모든 캔버스 공통 — localStorage에 영속(새로고침·페이지이동에도 유지).
const PREFS_KEY = 'ink:prefs';
type Prefs = { color?: string; width?: number; paper?: Paper; gap?: number; pressure?: boolean; dashed?: boolean; eraserSize?: number };
const loadPrefs = (): Prefs => { try { return JSON.parse(localStorage.getItem(PREFS_KEY) || '{}'); } catch { return {}; } };

// ★Android Chrome 에선 그릴 때 desynchronized 캔버스가 불투명 검정 하드웨어 overlay plane 으로 승격돼
//   화면 전체가 까맣게 덮이는 버그(삼성폰 확인). iOS/iPadOS·데스크탑은 정상 → 거기서만 저지연(desync) 유지.
const DESYNC_OK = typeof navigator === 'undefined' || !/android/i.test(navigator.userAgent || '');

export default function InkCanvas({ storageKey, height = 560, bgImage, launchLabel = '손으로 풀기' }: { storageKey: string; height?: number; bgImage?: string; launchLabel?: string }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const overRef = useRef<HTMLCanvasElement>(null);
  const overCtx = useRef<CanvasRenderingContext2D | null>(null);
  const uiRef = useRef<HTMLCanvasElement>(null);   // UI 전용(지우개 커서·올가미·선택박스) — 비desynchronized(iOS 정적표시 안전)
  const uiCtx = useRef<CanvasRenderingContext2D | null>(null);
  const strokesOf = useRef(new Map<string, Stroke[]>());                 // layerId → strokes
  // 지워진 스트로크 묘비. 삭제를 '없앰' 이 아니라 '표시' 로 남겨야 다른 기기의 합류가
  // 지운 획을 되살리지 않는다(v3).
  const deletedRef = useRef<string[]>([]);
  const elOf = useRef(new Map<string, { c: HTMLCanvasElement; ctx: CanvasRenderingContext2D | null }>());
  const cur = useRef<Stroke | null>(null);
  const removed = useRef<Stroke[]>([]);
  const undoStack = useRef<Action[]>([]);
  const redoStack = useRef<Action[]>([]);
  const penSeen = useRef(false);
  const recentPen = useRef(false); // 최근 펜 접촉 윈도우 — 획 사이 빠른 2탭(iOS 더블탭 선택 콜아웃) 차단용
  const sizeRef = useRef({ w: 0, h: 0, dpr: 1 });
  const selRef = useRef<Sel | null>(null);     // 갈무리 선택(활성 레이어 stroke idx 집합)
  const lassoRef = useRef<Pt[] | null>(null);  // 진행 중 올가미 폴리곤
  const dragRef = useRef<{ sx: number; sy: number; before: Stroke[]; idxs: number[] } | null>(null); // 선택 이동(시작점+원본)

  const [layers, setLayers] = useState<LayerMeta[]>([{ id: 'L1', name: '레이어 1', visible: true }]);
  const [activeId, setActiveId] = useState('L1');
  const [panel, setPanel] = useState(false);
  const [rev, setRev] = useState(0); // 썸네일·패널 갱신
  const [tool, setTool] = useState<Tool>('pen');
  const [eraserMode, setEraserMode] = useState<'precise' | 'stroke'>('precise');
  const [eraserSize, setEraserSize] = useState(() => loadPrefs().eraserSize ?? 24);
  const [pressure, setPressure] = useState(() => loadPrefs().pressure ?? false);
  const [dashed, setDashed] = useState(() => loadPrefs().dashed ?? false);
  const [lineMode, setLineMode] = useState(false); // 직선 도구(펜이 직선 + 각도 스냅)
  const [gridSnap, setGridSnap] = useState(false); // 격자 스냅(직선 끝점을 격자에)
  const [color, setColor] = useState(() => loadPrefs().color ?? COLORS[0]);
  const [width, setWidth] = useState(() => loadPrefs().width ?? WIDTHS[1]);
  const [paper, setPaper] = useState<Paper>(() => loadPrefs().paper ?? 'grid');
  const [gap, setGap] = useState(() => loadPrefs().gap ?? 24);
  const [full, setFull] = useState(false);
  const [portrait, setPortrait] = useState(false); // 전체화면 세로 → 가로 유도
  const live = useRef({ tool, eraserMode, eraserSize, pressure, dashed, lineMode, gridSnap, gap, color, width, activeId });
  live.current = { tool, eraserMode, eraserSize, pressure, dashed, lineMode, gridSnap, gap, color, width, activeId };
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
    const ctx = c.getContext('2d', (lowLatency && DESYNC_OK) ? ({ desynchronized: true } as CanvasRenderingContext2DSettings) : undefined);
    ctx?.scale(dpr, dpr); return ctx;
  }, []);

  const dbTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const save = useCallback(() => {
    const strokes: Record<string, Stroke[]> = {};
    for (const l of layersRef.current) strokes[l.id] = strokesOf.current.get(l.id) ?? [];
    // ★쓰기는 v3 로만. 읽기는 v1·v2·v3 전부(ink-doc.ts) — 사장님 필기가 이미 v2 로 있다.
    const doc = { v: INK_DOC_VERSION, layers: layersRef.current, strokes,
                  deletedStrokes: deletedRef.current, activeId: live.current.activeId };
    try { localStorage.setItem(KEY, JSON.stringify(doc)); } catch { /* quota */ }
    // 계정 DB 동기화(디바운스 1.5s — 획마다 POST 방지). 비로그인=401·offline=무시. 4MB 초과 스킵.
    if (dbTimer.current) clearTimeout(dbTimer.current);
    dbTimer.current = setTimeout(() => {
      try {
        const payload = JSON.stringify({ key: storageKey, doc });
        if (payload.length > 4_000_000) return;
        fetch('/api/handwriting', { method: 'POST', headers: { 'content-type': 'application/json' }, body: payload }).catch(() => { /* */ });
      } catch { /* */ }
    }, 1500);
  }, [KEY, storageKey]);

  const hit = (id: string, x: number, y: number, rad: number): number => {
    const arr = strokesOf.current.get(id) ?? [];
    for (let i = arr.length - 1; i >= 0; i--) {
      const s = arr[i]; if (s.tool !== 'pen' || !s.pts.length) continue;
      if (s.pts.length === 1) { if (Math.hypot(s.pts[0].x - x, s.pts[0].y - y) <= rad) return i; continue; }
      for (let k = 1; k < s.pts.length; k++) if (distToSeg(x, y, s.pts[k - 1].x, s.pts[k - 1].y, s.pts[k].x, s.pts[k].y) <= rad) return i; // 세그먼트 거리(직선 중간도)
    }
    return -1;
  };
  // 갈무리: 선택 박스(점선) 그리기 + 올가미 폴리곤 → 포함 stroke idx.
  const drawSelBox = useCallback(() => {
    const ctx = uiCtx.current; if (!ctx) return;
    ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
    const sel = selRef.current; if (!sel) return;
    const bb = bboxOf(strokesOf.current.get(sel.layerId) ?? [], sel.idxs); if (!bb) return;
    const pad = 7; ctx.save();
    ctx.fillStyle = 'rgba(80,120,220,0.09)'; ctx.fillRect(bb.x - pad, bb.y - pad, bb.w + 2 * pad, bb.h + 2 * pad);
    ctx.strokeStyle = 'rgba(70,110,210,0.95)'; ctx.lineWidth = 1.5; ctx.setLineDash([6, 4]);
    ctx.strokeRect(bb.x - pad, bb.y - pad, bb.w + 2 * pad, bb.h + 2 * pad); ctx.restore();
  }, []);
  const computeSel = useCallback((poly: Pt[], layerId: string): number[] => {
    const arr = strokesOf.current.get(layerId) ?? [], idxs: number[] = [];
    for (let i = 0; i < arr.length; i++) {
      const s = arr[i]; if (!s.pts.length) continue;
      let inN = 0; for (const p of s.pts) if (pointInPoly(p.x, p.y, poly)) inN++;
      if (inN / s.pts.length >= 0.5) idxs.push(i); // 과반 포함이면 선택
    }
    return idxs;
  }, []);

  // 마운트 1회: localStorage 데이터 로드(마이그레이션). ★아래 캔버스 setup 과 분리한다 — setup 은
  //   full 토글(작업영역 mount/unmount)마다 재실행되는데, 로드의 setLayers/setActiveId 가 그때마다
  //   리렌더→캔버스 리마운트 레이스를 일으켜 "기존 데이터 있는 일반모드에선 필기가 안 됨"(시크릿=빈
  //   데이터는 멀쩡) 회귀가 났음. 로드는 데이터만이라 캔버스(wrap/over) 불필요 → deps [KEY] 만.
  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        // v1(배열)·v2·v3 를 전부 v3 로 정규화해서 받는다 — 버전 분기를 여기 두면
        // 로드 지점이 늘 때마다 갈라진다(로컬·DB 두 곳이 이미 있다).
        const doc = normalizeInkDoc(JSON.parse(raw));
        if (doc) {
          strokesOf.current.clear();
          for (const l of doc.layers) strokesOf.current.set(l.id, doc.strokes[l.id] ?? []);
          deletedRef.current = doc.deletedStrokes;
          setLayers(doc.layers); setActiveId(doc.activeId ?? doc.layers[0].id);
        }
      }
    } catch { /* */ }
    if (!strokesOf.current.has('L1') && strokesOf.current.size === 0) strokesOf.current.set('L1', []);
  }, [KEY]);

  // DB(계정) hydration: 로컬에 이 페이지 필기가 없을 때만 DB 에서 불러와 그린다(로컬 작업 보존 우선).
  //   로그인 시 기기·시크릿·캐시삭제 무관 유지. 비로그인(401)/실패면 아무것도 안 함(로컬 유지).
  useEffect(() => {
    if (localStorage.getItem(KEY)) return;                 // 로컬 우선 — 덮어쓰기 방지
    let cancelled = false;
    fetch(`/api/handwriting?key=${encodeURIComponent(storageKey)}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        const doc = normalizeInkDoc(d?.doc);
        if (cancelled || !doc) return;
        strokesOf.current.clear();
        for (const l of doc.layers) strokesOf.current.set(l.id, doc.strokes[l.id] ?? []);
        deletedRef.current = doc.deletedStrokes;
        setLayers(doc.layers);
        setActiveId(doc.activeId ?? doc.layers[0]?.id);
        // 로컬에는 **정규화된 v3** 를 넣는다(받은 원문이 아니라) — 다음 로드가 또 변환하지 않게.
        try { localStorage.setItem(KEY, JSON.stringify(doc)); } catch { /* quota */ }
        for (const l of doc.layers) drawLayer(l.id);       // 캔버스 준비됐으면 즉시 그림
      })
      .catch(() => { /* */ });
    return () => { cancelled = true; };
  }, [KEY, storageKey, drawLayer]);

  // 캔버스 setup + 오버레이 핸들러 + 리사이즈. full 토글마다 재실행(접힘=작업영역 unmount→cleanup).
  useEffect(() => {
    const wrap = wrapRef.current, over = overRef.current; if (!wrap || !over) return;

    const setupAll = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      sizeRef.current = { w: wrap.clientWidth, h: wrap.clientHeight, dpr };
      overCtx.current = sizeCanvas(over, true); // 진행 overlay만 저지연
      if (uiRef.current) uiCtx.current = sizeCanvas(uiRef.current, false); // UI(커서·선택)=일반
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
    // 지우개 영역 표시(스탠다드) — overlay에 점선 원 + 옅은 채움. eraserSize=지름.
    const drawEraserCursor = (x: number, y: number) => {
      const ctx = uiCtx.current; if (!ctx) return;
      ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
      ctx.save();
      ctx.beginPath(); ctx.arc(x, y, live.current.eraserSize / 2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(150,150,150,0.14)'; ctx.fill();
      ctx.lineWidth = 1.3; ctx.setLineDash([4, 3]); ctx.strokeStyle = 'rgba(120,120,120,0.9)'; ctx.stroke();
      ctx.restore();
    };
    const clearCursor = () => uiCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h);
    const eraseStrokeAt = (x: number, y: number) => {
      const id = live.current.activeId, idx = hit(id, x, y, live.current.eraserSize / 2);
      if (idx >= 0) { const [s] = (strokesOf.current.get(id) ?? []).splice(idx, 1); removed.current.push(s); drawLayer(id); }
    };
    const drawLasso = () => {
      const ctx = uiCtx.current, poly = lassoRef.current; if (!ctx || !poly || poly.length < 2) return;
      ctx.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); ctx.save();
      ctx.beginPath(); ctx.moveTo(poly[0].x, poly[0].y);
      for (let i = 1; i < poly.length; i++) ctx.lineTo(poly[i].x, poly[i].y); ctx.closePath();
      ctx.fillStyle = 'rgba(80,120,220,0.08)'; ctx.fill();
      ctx.strokeStyle = 'rgba(70,110,210,0.9)'; ctx.lineWidth = 1.3; ctx.setLineDash([5, 4]); ctx.stroke(); ctx.restore();
    };
    // 진행 획을 레이어에 확정+저장. ★iOS가 pointerup을 지연/누락해 다음 pointerdown이 먼저 와도
    //   이전 획을 잃지 않도록 down에서도 호출 → 빠른 연속 획(짝수 획 누락) 방지.
    const finalizeCur = () => {
      if (!cur.current) return;
      const id = live.current.activeId, c = cur.current; cur.current = null;
      if (c.tool === 'eraser' && c.pts.length === 0) { // 획 지우개
        if (removed.current.length) { undoStack.current.push({ type: 'remove', layerId: id, strokes: removed.current.slice() }); removed.current = []; save(); setRev((r) => r + 1); }
        return;
      }
      if (c.tool === 'pen') { drawStroke(activeCtx()!, c); overCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); } // 펜=overlay→레이어(정밀지우개는 이미 레이어에)
      (strokesOf.current.get(id) ?? strokesOf.current.set(id, []).get(id)!).push(c);
      undoStack.current.push({ type: 'add', layerId: id, strokes: [c] });
      save(); setRev((r) => r + 1);
    };

    const down = (e: PointerEvent) => {
      if (e.pointerType === 'pen') penSeen.current = true;
      if (!accept(e)) return; e.preventDefault();
      markPen(); // 펜 접촉 윈도우 갱신(다음 빠른 탭의 선택 콜아웃 차단)
      if (cur.current) finalizeCur(); // ★이전 획 미완(iOS pointerup 지연)이면 먼저 확정 — 클로버 방지
      try { (window.getSelection?.())?.removeAllRanges?.(); } catch { /* iOS 선택 콜아웃 방지 */ }
      over.setPointerCapture(e.pointerId);
      const L = live.current;
      if (L.tool === 'select') { // ── 갈무리: 선택 내부면 이동, 아니면 새 올가미 ──
        const p = pt(e), sel = selRef.current;
        if (sel) { const bb = bboxOf(strokesOf.current.get(sel.layerId) ?? [], sel.idxs);
          if (bb && p.x >= bb.x - 10 && p.x <= bb.x + bb.w + 10 && p.y >= bb.y - 10 && p.y <= bb.y + bb.h + 10) {
            const arr = strokesOf.current.get(sel.layerId) ?? [];
            dragRef.current = { sx: p.x, sy: p.y, before: sel.idxs.map((i) => arr[i]), idxs: sel.idxs.slice() }; return;
          }
        }
        selRef.current = null; lassoRef.current = [p]; drawSelBox(); return;
      }
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { removed.current = []; const p0 = pt(e); eraseStrokeAt(p0.x, p0.y); drawEraserCursor(p0.x, p0.y); cur.current = { tool: 'eraser', color: '', width: 0, dashed: false, pressure: false, pts: [] }; return; }
      redoStack.current = [];
      const start = (L.tool === 'pen' && L.lineMode && L.gridSnap) ? snapGrid(pt(e), L.gap) : pt(e); // 직선+격자스냅이면 시작점 격자에
      cur.current = { tool: L.tool === 'shape' ? 'pen' : L.tool, color: L.color, width: L.tool === 'eraser' ? L.eraserSize : L.width, dashed: L.dashed, pressure: L.tool === 'shape' ? false : L.pressure, pts: [start] };
      if (L.tool === 'eraser') { const p0 = pt(e); drawStroke(activeCtx()!, cur.current); drawEraserCursor(p0.x, p0.y); } else renderOverlay();
    };
    const move = (e: PointerEvent) => {
      if (!accept(e)) return;
      const L = live.current;
      if (L.tool === 'select') { // ── 갈무리: 이동 or 올가미 ──
        if (dragRef.current) { e.preventDefault(); const sel = selRef.current; if (!sel) return;
          const p = pt(e), dx = p.x - dragRef.current.sx, dy = p.y - dragRef.current.sy, arr = strokesOf.current.get(sel.layerId) ?? [];
          dragRef.current.idxs.forEach((idx, k) => { arr[idx] = translateStroke(dragRef.current!.before[k], dx, dy); });
          drawLayer(sel.layerId); drawSelBox(); return;
        }
        if (lassoRef.current) { e.preventDefault(); lassoRef.current.push(pt(e)); drawLasso(); }
        return;
      }
      if (!cur.current) { if (L.tool === 'eraser') { const p = pt(e); drawEraserCursor(p.x, p.y); } return; } // 호버: 지우개 영역 미리보기(애플펜슬 호버 지원시)
      e.preventDefault();
      if (L.tool === 'eraser' && L.eraserMode === 'stroke') { const p = pt(e); eraseStrokeAt(p.x, p.y); drawEraserCursor(p.x, p.y); return; }
      if (cur.current.tool === 'pen' && L.lineMode) { // 직선: 시작→현재(격자 or 각도 스냅)
        const s = cur.current.pts[0], end = L.gridSnap ? snapGrid(pt(e), L.gap) : snapAngle(s, pt(e));
        cur.current.pts = [s, end]; renderOverlay(); return;
      }
      for (const ce of (e.getCoalescedEvents?.() ?? [e]) as PointerEvent[]) cur.current.pts.push(pt(ce));
      if (cur.current.tool === 'eraser') { drawStroke(activeCtx()!, cur.current); const p = pt(e); drawEraserCursor(p.x, p.y); } // 지우개=레이어에 지우고 overlay에 커서
      else { const pred = cur.current.dashed ? [] : ((e as PE).getPredictedEvents?.() ?? []) as PointerEvent[]; renderOverlay(pred.map(pt)); }
    };
    const up = (e: PointerEvent) => {
      markPen(); // 손 뗀 직후 윈도우 갱신(획 직후 빠른 2번째 탭 차단)
      const L = live.current;
      if (L.tool === 'select') { // ── 갈무리 확정 ──
        try { over.releasePointerCapture(e.pointerId); } catch { /* */ }
        if (dragRef.current) {
          const sel = selRef.current;
          if (sel) { const arr = strokesOf.current.get(sel.layerId) ?? [];
            const moved = sel.idxs.some((i, k) => arr[i] !== dragRef.current!.before[k]);
            if (moved) { undoStack.current.push({ type: 'mutate', layerId: sel.layerId, idxs: sel.idxs.slice(), before: dragRef.current.before, after: sel.idxs.map((i) => arr[i]) }); redoStack.current = []; save(); }
          }
          dragRef.current = null; drawSelBox(); setRev((r) => r + 1); return;
        }
        if (lassoRef.current) {
          const poly = lassoRef.current; lassoRef.current = null;
          if (poly.length >= 3) { const lid = L.activeId, idxs = computeSel(poly, lid); selRef.current = idxs.length ? { layerId: lid, idxs } : null; }
          else selRef.current = null;
          drawSelBox(); setRev((r) => r + 1); return;
        }
        return;
      }
      if (!cur.current) return;
      try { over.releasePointerCapture(e.pointerId); } catch { /* */ }
      if (L.tool === 'shape' && cur.current.pts.length >= 4) { // ★도형 모드: 인식되면 깔끔한 도형으로 스냅(아니면 자유필기 유지)
        const rec = recognizeShape(cur.current.pts.map((p) => ({ x: p.x, y: p.y })));
        if (rec) cur.current.pts = shapeToPoints(rec).map((p) => ({ x: p.x, y: p.y, p: 0.5 }));
      }
      finalizeCur();
      if (L.tool === 'eraser') clearCursor(); // 지우개 커서 정리(다음 호버/이동에 다시 그림)
    };
    const onLeave = () => { if (!cur.current && live.current.tool === 'eraser') clearCursor(); }; // 펜이 캔버스 벗어나면 커서 제거

    over.addEventListener('pointerdown', down); over.addEventListener('pointermove', move);
    over.addEventListener('pointerup', up); over.addEventListener('pointercancel', up);
    over.addEventListener('pointerleave', onLeave);
    // ★iOS 더블탭-줌 제스처가 빠른 둘째 탭의 pointerdown을 통째로 삼키는 것 차단.
    //   touch-action:none이 iOS Safari에선 부족 → 터치 기본동작을 직접 preventDefault(passive:false 필수).
    //   포인터 이벤트는 별개로 발생하므로 그리기는 유지됨.
    const killTouch = (ev: TouchEvent) => ev.preventDefault();
    over.addEventListener('touchstart', killTouch, { passive: false });
    over.addEventListener('touchmove', killTouch, { passive: false });
    over.addEventListener('touchend', killTouch, { passive: false });
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
      over.removeEventListener('pointerdown', down); over.removeEventListener('pointermove', move); over.removeEventListener('pointerup', up); over.removeEventListener('pointercancel', up); over.removeEventListener('pointerleave', onLeave);
      over.removeEventListener('touchstart', killTouch); over.removeEventListener('touchmove', killTouch); over.removeEventListener('touchend', killTouch);
      wrap.removeEventListener('selectstart', killSel); wrap.removeEventListener('contextmenu', killSel); over.removeEventListener('contextmenu', killSel);
      document.removeEventListener('selectstart', docSel); document.removeEventListener('dblclick', docSel);
      if (penTimer) clearTimeout(penTimer); document.body.style.removeProperty('-webkit-user-select');
      ro.disconnect();
    };
    // ★full 추가: 전체화면 열림(작업영역 mount)/닫힘(unmount)마다 effect 재실행 → 새 캔버스에 setup·리스너 부착,
    //   닫을 때 cleanup. 접힘 땐 wrap/over ref null 이라 상단 early-return.
  }, [KEY, drawStroke, drawLayer, sizeCanvas, save, drawSelBox, computeSel, full]);

  // 새 레이어 캔버스(나중에 추가된)도 사이즈+그림 보장.
  useEffect(() => {
    if (!sizeRef.current.w) return;
    for (const [id, e] of elOf.current) if (!e.ctx) { e.ctx = sizeCanvas(e.c); drawLayer(id); }
  }, [layers, sizeCanvas, drawLayer]);

  // 도구/지우개 설정이 바뀌면 overlay(지우개 커서·선택 박스 잔상) 정리. select 벗어나면 선택 해제.
  useEffect(() => { if (tool !== 'select') selRef.current = null; uiCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); }, [tool, eraserMode, eraserSize]);

  // 화면 방향(전체화면 세로 → 가로 유도용).
  useEffect(() => {
    const mq = window.matchMedia('(orientation: portrait)');
    const on = () => setPortrait(mq.matches); on();
    mq.addEventListener('change', on); return () => mq.removeEventListener('change', on);
  }, []);

  // 펜/종이 설정 영속(공통 prefs — 새로고침·페이지이동에도 유지).
  useEffect(() => {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify({ color, width, paper, gap, pressure, dashed, eraserSize })); } catch { /* quota */ }
  }, [color, width, paper, gap, pressure, dashed, eraserSize]);

  const layerRef = useCallback((el: HTMLCanvasElement | null) => {
    if (!el) return; const id = el.dataset.lid!; if (!elOf.current.has(id) || elOf.current.get(id)!.c !== el) elOf.current.set(id, { c: el, ctx: sizeRef.current.w ? sizeCanvas(el) : null });
    if (elOf.current.get(id)!.ctx) drawLayer(id);
  }, [sizeCanvas, drawLayer]);

  // ── 레이어/undo 조작 ──
  const addLayer = () => { const id = nid(); strokesOf.current.set(id, []); setLayers((ls) => [...ls, { id, name: `레이어 ${ls.length + 1}`, visible: true }]); setActiveId(id); setRev((r) => r + 1); save(); };
  const delLayer = (id: string) => {
    if (layers.length <= 1) return; if (!confirm('이 레이어를 삭제할까요?')) return;
    strokesOf.current.delete(id); elOf.current.delete(id);
    if (selRef.current?.layerId === id) { selRef.current = null; uiCtx.current?.clearRect(0, 0, sizeRef.current.w, sizeRef.current.h); } // 선택 레이어 삭제 시 선택 해제
    const next = layers.filter((l) => l.id !== id); setLayers(next);
    if (activeId === id) setActiveId(next[0].id); setRev((r) => r + 1); save();
  };
  const toggleVis = (id: string) => { setLayers((ls) => ls.map((l) => l.id === id ? { ...l, visible: !l.visible } : l)); setRev((r) => r + 1); save(); };
  const rename = (id: string) => { const n = prompt('레이어 이름', layers.find((l) => l.id === id)?.name); if (n != null) { setLayers((ls) => ls.map((l) => l.id === id ? { ...l, name: n } : l)); save(); } };
  const moveLayer = (id: string, dir: -1 | 1) => { setLayers((ls) => { const i = ls.findIndex((l) => l.id === id), j = i + dir; if (j < 0 || j >= ls.length) return ls; const n = ls.slice(); [n[i], n[j]] = [n[j], n[i]]; return n; }); setRev((r) => r + 1); save(); };

  const applyAct = (a: Action, forward: boolean) => { // forward=redo방향, !forward=undo
    if (a.type === 'add') { const arr = strokesOf.current.get(a.layerId) ?? []; if (forward) arr.push(...a.strokes); else for (const s of a.strokes) { const i = arr.indexOf(s); if (i >= 0) arr.splice(i, 1); } drawLayer(a.layerId); }
    else if (a.type === 'remove') { const arr = strokesOf.current.get(a.layerId) ?? []; if (forward) for (const s of a.strokes) { const i = arr.indexOf(s); if (i >= 0) arr.splice(i, 1); } else arr.push(...a.strokes); drawLayer(a.layerId); }
    else if (a.type === 'mutate') { const arr = strokesOf.current.get(a.layerId) ?? []; const src = forward ? a.after : a.before; a.idxs.forEach((i, k) => { arr[i] = src[k]; }); drawLayer(a.layerId); }
    else { const from = strokesOf.current.get(a.from) ?? [], to = strokesOf.current.get(a.to) ?? []; const [src, dst] = forward ? [from, to] : [to, from]; for (const s of a.strokes) { const i = src.indexOf(s); if (i >= 0) src.splice(i, 1); } dst.push(...a.strokes); drawLayer(a.from); drawLayer(a.to); }
  };
  const undo = () => { const a = undoStack.current.pop(); if (!a) return; redoStack.current.push(a); applyAct(a, false); selRef.current = null; drawSelBox(); save(); setRev((r) => r + 1); };
  const redoFn = () => { const a = redoStack.current.pop(); if (!a) return; undoStack.current.push(a); applyAct(a, true); selRef.current = null; drawSelBox(); save(); setRev((r) => r + 1); };
  const clearActive = () => { const arr = strokesOf.current.get(activeId) ?? []; if (!arr.length || !confirm('이 레이어 필기를 지울까요?')) return; undoStack.current.push({ type: 'remove', layerId: activeId, strokes: arr.slice() }); redoStack.current = []; arr.length = 0; selRef.current = null; drawLayer(activeId); drawSelBox(); save(); setRev((r) => r + 1); };

  // ── 갈무리(선택) 조작 ──
  const deselect = () => { selRef.current = null; drawSelBox(); setRev((r) => r + 1); };
  const selectAll = () => { const arr = strokesOf.current.get(activeId) ?? []; if (!arr.length) return; selRef.current = { layerId: activeId, idxs: arr.map((_, i) => i) }; drawSelBox(); setRev((r) => r + 1); };
  const deleteSel = () => {
    const sel = selRef.current; if (!sel) return;
    const arr = strokesOf.current.get(sel.layerId) ?? [], removedS = sel.idxs.map((i) => arr[i]).filter(Boolean);
    [...sel.idxs].sort((a, b) => b - a).forEach((i) => arr.splice(i, 1));
    undoStack.current.push({ type: 'remove', layerId: sel.layerId, strokes: removedS }); redoStack.current = [];
    selRef.current = null; drawLayer(sel.layerId); drawSelBox(); save(); setRev((r) => r + 1);
  };
  const dupSel = () => {
    const sel = selRef.current; if (!sel) return;
    const arr = strokesOf.current.get(sel.layerId) ?? [], clones = sel.idxs.map((i) => arr[i]).filter(Boolean).map((s) => translateStroke(s, 18, 18));
    const start = arr.length; arr.push(...clones);
    undoStack.current.push({ type: 'add', layerId: sel.layerId, strokes: clones }); redoStack.current = [];
    selRef.current = { layerId: sel.layerId, idxs: clones.map((_, k) => start + k) };
    drawLayer(sel.layerId); drawSelBox(); save(); setRev((r) => r + 1);
  };
  const recolorSel = (col: string) => {
    const sel = selRef.current; if (!sel) return;
    const arr = strokesOf.current.get(sel.layerId) ?? [], idxs = sel.idxs.filter((i) => arr[i]?.tool === 'pen'); if (!idxs.length) return;
    const before = idxs.map((i) => arr[i]), after = before.map((s) => ({ ...s, color: col }));
    idxs.forEach((i, k) => { arr[i] = after[k]; });
    undoStack.current.push({ type: 'mutate', layerId: sel.layerId, idxs, before, after }); redoStack.current = [];
    drawLayer(sel.layerId); drawSelBox(); save(); setRev((r) => r + 1);
  };
  const moveSelTo = (targetId: string) => {
    const sel = selRef.current; if (!sel || targetId === sel.layerId) return;
    const arr = strokesOf.current.get(sel.layerId) ?? [], moving = sel.idxs.map((i) => arr[i]).filter(Boolean);
    [...sel.idxs].sort((a, b) => b - a).forEach((i) => arr.splice(i, 1));
    const tArr = strokesOf.current.get(targetId) ?? strokesOf.current.set(targetId, []).get(targetId)!;
    tArr.push(...moving);
    undoStack.current.push({ type: 'move', from: sel.layerId, to: targetId, strokes: moving }); redoStack.current = [];
    selRef.current = null; drawLayer(sel.layerId); drawLayer(targetId); drawSelBox(); save(); setRev((r) => r + 1);
  };
  // 내보내기: 선택영역(있으면) 또는 전체를 흰 배경 PNG로. 튜터 이미지 피드백의 토대.
  const exportPng = () => {
    const { w, h, dpr } = sizeRef.current; if (!w) return;
    const sel = selRef.current, bb = sel ? bboxOf(strokesOf.current.get(sel.layerId) ?? [], sel.idxs) : null, pad = 14;
    const rx = bb ? Math.max(0, bb.x - pad) : 0, ry = bb ? Math.max(0, bb.y - pad) : 0;
    const rw = bb ? Math.min(w - rx, bb.w + 2 * pad) : w, rh = bb ? Math.min(h - ry, bb.h + 2 * pad) : h;
    const out = document.createElement('canvas'); out.width = Math.round(rw * dpr); out.height = Math.round(rh * dpr);
    const octx = out.getContext('2d'); if (!octx) return;
    octx.fillStyle = '#ffffff'; octx.fillRect(0, 0, out.width, out.height);
    octx.scale(dpr, dpr); octx.translate(-rx, -ry);
    for (const l of layers) if (l.visible) { const e = elOf.current.get(l.id); if (e?.c) octx.drawImage(e.c, 0, 0, w, h); }
    // toDataURL(동기)로 — 사용자 제스처 안에서 즉시 다운로드(iOS Safari는 toBlob 비동기 콜백 다운로드를 막음).
    const a = document.createElement('a'); a.href = out.toDataURL('image/png'); a.download = `손풀이-${storageKey.replace(/[^a-z0-9가-힣]+/gi, '_')}.png`; a.click();
  };

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
    <div style={full ? { position: 'fixed', inset: 0, zIndex: 1000, background: 'var(--color-bg)', display: 'flex', flexDirection: 'column', padding: 10, gap: 8 } : undefined}>
      {/* 접힘 상태: 좌하단 floating FAB(튜터 우하단 ↔ 손풀이 좌하단). 본문에 묻히지 않고 항상 노출돼
          "손으로 풀 수 있다"를 인지시킨다. 누르면 전체화면. .tutor-fab 와 동일 스타일(좌우만 반전).
          캔버스 DOM 은 아래 작업영역에 display:none 으로 살아있어 init 안전(열 때 ResizeObserver 재size·재draw). */}
      {!full && (
        <button onClick={() => setFull(true)} data-ink-fab aria-label={launchLabel} title={`${launchLabel} — 전체화면 펜·태블릿 (자동 저장)`}
          style={{ position: 'fixed', left: 16, bottom: 'calc(env(safe-area-inset-bottom) + 16px)', zIndex: 48, display: 'inline-flex', alignItems: 'center', gap: 8, height: 48, padding: '0 18px', borderRadius: 999, background: 'var(--color-surface)', border: '1px solid var(--color-border-strong)', color: 'var(--color-text)', boxShadow: 'var(--shadow-card-hover)', fontSize: 14, fontWeight: 600, letterSpacing: '-0.01em', cursor: 'pointer' }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--pen-red)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }} aria-hidden="true">
            <path d="M12 20h9" />
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
          </svg>
          <span style={{ whiteSpace: 'nowrap' }}>{launchLabel}</span>
        </button>
      )}
      {full && portrait && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 1002, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 14, background: 'var(--color-bg)', color: 'var(--color-text)', textAlign: 'center', padding: 24 }}>
          <div style={{ fontSize: 44 }}>📱↻</div>
          <div style={{ fontSize: 17, fontWeight: 700 }}>가로로 돌려주세요</div>
          <div style={{ fontSize: 13, color: 'var(--color-muted)' }}>문제 풀이는 가로 화면에서 가장 편합니다 (왼쪽 문제 · 오른쪽 풀이)</div>
        </div>
      )}
      {/* ★접힘일 땐 작업영역을 display:none 이 아니라 아예 unmount → 열 때 캔버스(특히 desync 오버레이)를
          새 엘리먼트로 mount=깨끗한 실사이즈 init. display:none 재init 이 iPad desync 합성을 깨던 회귀 차단. */}
      {full && (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flex: 1, minHeight: 0 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <button style={btn(tool === 'pen')} onClick={() => setTool('pen')}>✏️ 펜</button>
        <button style={btn(tool === 'eraser')} onClick={() => setTool('eraser')}>지우개</button>
        <button style={btn(tool === 'select')} onClick={() => setTool('select')} title="올가미로 묶어 이동·복제·색변경·레이어이동">⬚ 선택</button>
        <button style={btn(tool === 'shape')} onClick={() => setTool('shape')} title="대충 그리면 깔끔한 도형으로 — 삼각형·사각형·원·타원·직선">⬡ 도형</button>
        {tool === 'eraser' && (<>
          <button style={btn(eraserMode === 'precise')} onClick={() => setEraserMode('precise')}>정밀</button>
          <button style={btn(eraserMode === 'stroke')} onClick={() => setEraserMode('stroke')}>획</button>
          {ERASER_SIZES.map((s) => (<button key={s} style={{ ...btn(eraserSize === s), padding: '4px 7px' }} onClick={() => setEraserSize(s)} title={`지우개 ${s}px`}><span style={{ display: 'inline-block', width: Math.round(s / 3) + 3, height: Math.round(s / 3) + 3, borderRadius: '50%', border: '1.5px solid currentColor', verticalAlign: 'middle' }} /></button>))}
        </>)}
        {tool === 'select' && <button style={btn(false)} onClick={selectAll} title="이 레이어 전체 선택">전체선택</button>}
        {tool === 'select' && selRef.current && (<>
          <button style={btn(false)} onClick={dupSel}>복제</button>
          <button style={btn(false)} onClick={() => recolorSel(color)} title="선택을 현재 색으로">🎨 색</button>
          {layers.length > 1 && (
            <select value="" onChange={(e) => { if (e.target.value) moveSelTo(e.target.value); }} style={{ ...btn(false), padding: '4px 6px' }} title="다른 레이어로 이동">
              <option value="">레이어→</option>
              {layers.filter((l) => l.id !== selRef.current!.layerId).map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}
            </select>
          )}
          <button style={btn(false)} onClick={deleteSel}>삭제</button>
          <button style={btn(false)} onClick={deselect}>해제</button>
        </>)}
        {sep}
        {COLORS.map((c) => (<button key={c} onClick={() => { setColor(c); setTool('pen'); }} title={c} style={{ width: 20, height: 20, borderRadius: '50%', background: c, cursor: 'pointer', border: color === c ? '2px solid var(--color-accent)' : '2px solid var(--color-border)' }} />))}
        {WIDTHS.map((w) => (<button key={w} onClick={() => setWidth(w)} style={btn(width === w)}><span style={{ display: 'inline-block', width: 16, height: w + 2, borderRadius: 99, background: 'currentColor', verticalAlign: 'middle' }} /></button>))}
        <button style={btn(dashed)} onClick={() => setDashed((v) => !v)} title="점선/실선">{dashed ? '┈ 점선' : '─ 실선'}</button>
        <button style={btn(pressure)} onClick={() => setPressure((v) => !v)} title="필압(수학엔 무감지 권장)">{pressure ? '✍️ 필압' : '═ 균일'}</button>
        <button style={btn(lineMode)} onClick={() => setLineMode((v) => !v)} title="직선 도구(끌면 직선 + 0/45/90° 각도 스냅)">📐 직선</button>
        {lineMode && paper === 'grid' && <button style={btn(gridSnap)} onClick={() => setGridSnap((v) => !v)} title="직선 끝점을 격자에 스냅">⊞ 격자스냅</button>}
        {sep}
        <select value={paper} onChange={(e) => setPaper(e.target.value as Paper)} style={{ ...btn(false), padding: '4px 6px' }} title="종이"><option value="blank">백지</option><option value="ruled">줄</option><option value="grid">격자</option></select>
        {paper !== 'blank' && <input type="range" min={14} max={48} value={gap} onChange={(e) => setGap(+e.target.value)} title={`간격 ${gap}px`} style={{ width: 64 }} />}
        <span style={{ flex: 1 }} />
        <button style={btn(panel)} onClick={() => setPanel((v) => !v)} title="레이어">▤ 레이어</button>
        <button style={btn(false)} onClick={undo}>↶</button>
        <button style={btn(false)} onClick={redoFn}>↷</button>
        <button style={btn(false)} onClick={clearActive}>레이어지움</button>
        <button style={btn(false)} onClick={exportPng} title={selRef.current ? '선택 영역을 PNG로 저장' : '전체를 PNG로 저장'}>📷</button>
        <button style={btn(full)} onClick={() => setFull((v) => !v)}>{full ? '✕ 닫기' : '⛶ 전체화면'}</button>
      </div>
      <div style={{ display: 'flex', gap: 8, flex: full ? 1 : undefined, minHeight: 0 }}>
        <div ref={wrapRef} style={{ position: 'relative', flex: 1, height: full ? undefined : height, borderRadius: 12, border: '1px solid var(--color-border)', overflow: 'hidden', background: 'var(--color-surface)', touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none', backgroundImage: paperBg() }}>
          {full && bgImage && <img src={bgImage} alt="문제" draggable={false} style={{ position: 'absolute', left: 0, top: 0, width: '50%', height: '100%', objectFit: 'contain', objectPosition: 'top left', zIndex: 0, opacity: 0.97, pointerEvents: 'none', userSelect: 'none' }} />}
          {layers.map((l, i) => (<canvas key={l.id} data-lid={l.id} ref={layerRef} style={{ position: 'absolute', inset: 0, zIndex: i + 1, display: l.visible ? 'block' : 'none', touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }} />))}
          <canvas ref={overRef} style={{ position: 'absolute', inset: 0, zIndex: 998, touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }} />
          <canvas ref={uiRef} style={{ position: 'absolute', inset: 0, zIndex: 999, pointerEvents: 'none' }} />
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
      </div>)}
    </div>
  );
}
