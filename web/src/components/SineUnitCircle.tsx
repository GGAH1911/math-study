import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { ensureKatex } from '../lib/mathish';

// 삼각비 어원 인터랙티브 위젯 — 단위원 + 직각삼각형으로 사인=활시위(현)의 절반(반현)임을 보인다.
//   원본(맥북 사인의 어원.html)의 캔버스 로직을 React로 포팅. KaTeX는 우리 mathish(SSOT) ensureKatex.
//   개념 노드(삼각비의_정의)에 임베드되는 client island. 드래그/슬라이더/자동회전/범례 호버.
const C = {
  arc: '#f59e0b', sine: '#2dd4bf', cos: '#a855f7', tan: '#f43f5e', hyp: '#ef4444',
  chord: '#38bdf8', arrow: '#64748b', grid: '#1e293b', circle: '#334155', text: '#e2e8f0',
};
type Hover = 'bow' | 'chord' | 'sine' | 'cosine' | 'tangent' | null;

export default function SineUnitCircle() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const f1Ref = useRef<HTMLDivElement | null>(null);
  const f2Ref = useRef<HTMLDivElement | null>(null);
  const [angle, setAngle] = useState(45);
  const [animating, setAnimating] = useState(false);
  const [hover, setHover] = useState<Hover>(null);
  const [sizeV, setSizeV] = useState(0);
  const dragRef = useRef(false);
  const dirRef = useRef(1);

  // 캔버스 크기(컨테이너 + DPR) — 마운트·리사이즈 시
  useEffect(() => {
    const cv = canvasRef.current; if (!cv) return;
    const fit = () => {
      const box = cv.parentElement!.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      cv.width = box.width * dpr; cv.height = box.width * dpr;
      cv.style.height = `${box.width}px`;
      setSizeV((v) => v + 1);
    };
    fit();
    window.addEventListener('resize', fit);
    return () => window.removeEventListener('resize', fit);
  }, []);

  // 그리기 — angle/hover/size 변화 시
  useEffect(() => {
    const cv = canvasRef.current; if (!cv) return;
    const ctx = cv.getContext('2d'); if (!ctx) return;
    const dpr = window.devicePixelRatio || 1;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = cv.width / dpr, H = cv.height / dpr;
    ctx.clearRect(0, 0, W, H);
    const cx = W / 2 - W * 0.07, cy = H / 2, R = Math.min(W, H) * 0.35;
    const th = (angle * Math.PI) / 180;
    const px = cx + R * Math.cos(th), pyT = cy - R * Math.sin(th), pyB = cy + R * Math.sin(th);
    const line = (x1: number, y1: number, x2: number, y2: number, col: string, w: number, dash?: number[]) => {
      ctx.strokeStyle = col; ctx.lineWidth = w; ctx.setLineDash(dash || []);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); ctx.setLineDash([]);
    };
    // 축
    line(cx, 0, cx, H, C.grid, 1); line(0, cy, W, cy, C.grid, 1);
    // 단위원
    ctx.strokeStyle = C.circle; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
    // 직각삼각형 채움
    ctx.fillStyle = 'rgba(15,23,42,0.6)';
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(px, cy); ctx.lineTo(px, pyT); ctx.closePath(); ctx.fill();
    // 호(활)
    ctx.strokeStyle = C.arc; ctx.lineWidth = hover === 'bow' ? 6 : 4;
    ctx.beginPath(); ctx.arc(cx, cy, R, -th, th); ctx.stroke();
    ctx.fillStyle = '#b45309';
    ctx.beginPath(); ctx.arc(px, pyT, 5, 0, 7); ctx.arc(px, pyB, 5, 0, 7); ctx.fill();
    // 현 아래절반(흐리게)
    line(px, cy, px, pyB, 'rgba(56,189,248,0.4)', 1.5, [2, 2]);
    // 사인(현 위절반=반현)
    line(px, cy, px, pyT, C.sine, hover === 'sine' || hover === 'chord' ? 6 : 4);
    // 빗변(반지름)
    line(cx, cy, px, pyT, C.hyp, hover === 'sine' ? 2 : 3);
    // 코사인(밑변)
    line(cx, cy, px, cy, C.cos, hover === 'cosine' ? 6 : 3);
    // 탄젠트
    const tx = cx + R, ty = cy - R * Math.tan(th);
    line(px, pyT, tx, ty, 'rgba(255,255,255,0.22)', 1, [3, 3]);
    line(tx, cy, tx, ty, C.tan, hover === 'tangent' ? 6 : 3);
    ctx.fillStyle = C.tan; ctx.beginPath(); ctx.arc(tx, cy, 4, 0, 7); ctx.fill();
    // 화살(sagitta)
    line(cx - 30, cy, px, cy, C.arrow, 2);
    ctx.fillStyle = C.arrow; ctx.beginPath(); ctx.moveTo(px, cy); ctx.lineTo(px - 8, cy - 4); ctx.lineTo(px - 8, cy + 4); ctx.closePath(); ctx.fill();
    line(px, cy, cx + R, cy, C.text, 3);
    // θ호
    ctx.strokeStyle = C.arc; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, 28, -th, 0); ctx.stroke();
    // 라벨
    ctx.font = 'bold 12px "Noto Sans KR",sans-serif';
    ctx.fillStyle = C.arc; ctx.fillText('θ', cx + 34, cy - 9);
    ctx.fillStyle = C.hyp; ctx.fillText('반지름 r', (cx + px) / 2 - 16, (cy + pyT) / 2 - 9);
    ctx.fillStyle = C.sine; ctx.fillText('사인 (활시위 절반)', px + 9, (cy + pyT) / 2);
    ctx.fillStyle = C.cos; ctx.fillText('코사인', (cx + px) / 2 - 14, cy + 17);
    ctx.fillStyle = C.tan; ctx.fillText('탄젠트', tx + 8, (cy + ty) / 2);
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(cx, cy, 4, 0, 7); ctx.fill();
    ctx.fillText('O', cx - 14, cy + 17);
  }, [angle, hover, sizeV]);

  // 자동회전
  useEffect(() => {
    if (!animating) return;
    let raf = 0;
    const tick = () => {
      setAngle((a) => {
        let n = a + 0.5 * dirRef.current;
        if (n >= 80) { n = 80; dirRef.current = -1; } else if (n <= 10) { n = 10; dirRef.current = 1; }
        return n;
      });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [animating]);

  // 라이브 수식 (우리 KaTeX SSOT)
  useEffect(() => {
    ensureKatex().then((katex) => {
      const s = Math.sin((angle * Math.PI) / 180);
      if (f1Ref.current) katex.render(`\\sin(${angle.toFixed(1)}^\\circ)=\\frac{\\text{대변 (활시위의 절반)}}{\\text{빗변 } r}=\\frac{${s.toFixed(4)}}{1}=${s.toFixed(4)}`, f1Ref.current, { displayMode: true, throwOnError: false });
      if (f2Ref.current) katex.render(`\\text{활시위 전체}=2\\times\\sin(${angle.toFixed(1)}^\\circ)=${(s * 2).toFixed(4)}`, f2Ref.current, { displayMode: true, throwOnError: false });
    }).catch(() => {});
  }, [angle]);

  // 드래그로 각도 조절
  useEffect(() => {
    const cv = canvasRef.current; if (!cv) return;
    const at = (e: MouseEvent | TouchEvent) => {
      const r = cv.getBoundingClientRect();
      const t = (e as TouchEvent).touches?.[0];
      const clientX = t ? t.clientX : (e as MouseEvent).clientX;
      const clientY = t ? t.clientY : (e as MouseEvent).clientY;
      const cx = r.width / 2 - r.width * 0.07, cy = r.height / 2;
      let d = (Math.atan2(cy - (clientY - r.top), clientX - r.left - cx) * 180) / Math.PI;
      if (d < 0) d = Math.abs(d);
      if (d >= 2 && d <= 88) { setAnimating(false); setAngle(d); }
    };
    const down = (e: MouseEvent | TouchEvent) => { dragRef.current = true; at(e); };
    const move = (e: MouseEvent | TouchEvent) => { if (dragRef.current) { at(e); if ((e as TouchEvent).touches) e.preventDefault(); } };
    const up = () => { dragRef.current = false; };
    cv.addEventListener('mousedown', down); cv.addEventListener('touchstart', down, { passive: false });
    window.addEventListener('mousemove', move); window.addEventListener('touchmove', move, { passive: false });
    window.addEventListener('mouseup', up); window.addEventListener('touchend', up);
    return () => { cv.removeEventListener('mousedown', down); cv.removeEventListener('touchstart', down); window.removeEventListener('mousemove', move); window.removeEventListener('touchmove', move); window.removeEventListener('mouseup', up); window.removeEventListener('touchend', up); };
  }, []);

  const sinV = Math.sin((angle * Math.PI) / 180).toFixed(3);
  const cosV = Math.cos((angle * Math.PI) / 180).toFixed(3);
  const legends: Array<{ k: Hover; c: string; t: string }> = [
    { k: 'bow', c: C.arc, t: '활 (호)' }, { k: 'chord', c: C.chord, t: '활시위 (현)' },
    { k: 'sine', c: C.sine, t: '사인 (반현)' }, { k: 'cosine', c: C.cos, t: '코사인' }, { k: 'tangent', c: C.tan, t: '탄젠트' },
  ];
  const card: CSSProperties = { background: '#0f172a', border: '1px solid #1e293b', borderRadius: 14, padding: 16 };
  const chip: CSSProperties = { background: '#020617', border: '1px solid #1e293b', borderRadius: 8, padding: '4px 9px', fontSize: 13, fontFamily: 'monospace' };

  return (
    <div style={{ background: '#020617', color: '#e2e8f0', borderRadius: 16, padding: 16, fontFamily: '"Noto Sans KR",sans-serif', maxWidth: 560, margin: '0 auto' }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12, fontSize: 13 }}>
        <span style={chip}>각도 θ <b style={{ color: C.arc }}>{angle.toFixed(1)}°</b></span>
        <span style={chip}>sin <b style={{ color: C.sine }}>{sinV}</b></span>
        <span style={chip}>cos <b style={{ color: C.cos }}>{cosV}</b></span>
      </div>
      <div style={card}>
        <div style={{ position: 'relative', width: '100%', background: '#020617', borderRadius: 10, overflow: 'hidden', cursor: 'crosshair' }}>
          <canvas ref={canvasRef} style={{ width: '100%', display: 'block' }} />
        </div>
        <p style={{ fontSize: 12, color: '#64748b', textAlign: 'center', margin: '10px 0 0' }}>💡 캔버스를 드래그하면 각도 θ를 직접 조절할 수 있습니다.</p>
        <div style={{ marginTop: 14 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#94a3b8', marginBottom: 4 }}><span>각도 θ</span><span style={{ fontFamily: 'monospace' }}>{angle.toFixed(1)}°</span></div>
          <input type="range" min={5} max={85} step={0.5} value={angle} onChange={(e) => { setAnimating(false); setAngle(parseFloat(e.target.value)); }} style={{ width: '100%', accentColor: C.arc }} />
        </div>
        <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
          <button onClick={() => setAnimating((a) => !a)} style={{ flex: 1, padding: '8px', borderRadius: 8, border: 'none', background: C.arc, color: '#020617', fontWeight: 700, cursor: 'pointer' }}>{animating ? '⏸ 일시정지' : '▶ 자동 회전'}</button>
          <button onClick={() => { setAnimating(false); setAngle(45); }} style={{ padding: '8px 16px', borderRadius: 8, border: '1px solid #334155', background: '#1e293b', color: '#e2e8f0', cursor: 'pointer' }}>초기화</button>
        </div>
      </div>
      <div style={{ ...card, marginTop: 12, display: 'flex', flexWrap: 'wrap', gap: 8, fontSize: 12 }}>
        {legends.map((l) => (
          <span key={l.k} onMouseEnter={() => setHover(l.k)} onMouseLeave={() => setHover(null)} style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '3px 7px', borderRadius: 6, cursor: 'pointer', background: hover === l.k ? '#1e293b' : 'transparent' }}>
            <span style={{ width: 12, height: 4, borderRadius: 2, background: l.c, display: 'inline-block' }} />{l.t}
          </span>
        ))}
      </div>
      <div style={{ ...card, marginTop: 12, background: 'linear-gradient(90deg,#0f172a,#1e1b4b)' }}>
        <div ref={f1Ref} style={{ textAlign: 'center', padding: '4px 0', overflowX: 'auto' }} />
        <div style={{ height: 1, background: '#1e293b', margin: '8px 0' }} />
        <div ref={f2Ref} style={{ textAlign: 'center', color: C.arc, padding: '4px 0', overflowX: 'auto' }} />
        <p style={{ fontSize: 11, color: '#94a3b8', marginTop: 8, textAlign: 'center' }}>단위원(r=1)에서 <b style={{ color: C.sine }}>sin θ = 활시위 절반의 실제 길이</b></p>
      </div>
    </div>
  );
}
