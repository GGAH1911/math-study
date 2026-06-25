import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { ensureKatex } from '../lib/mathish';

// 삼각비 어원 인터랙티브 위젯 — 단위원 + 직각삼각형으로 사인=활시위(현)의 절반(반현)임을 보인다.
//   ★색·표면은 전부 사이트 디자인 토큰(global.css CSS 변수) 사용 → 종이/스케치북 톤 + 라이트/다크 토글 자동 적응.
//   캔버스는 CSS변수를 getComputedStyle로 읽어 그린다. KaTeX는 mathish(SSOT) ensureKatex.
type Hover = 'bow' | 'chord' | 'sine' | 'cosine' | 'tangent' | null;
// 도형색 = 사이트 토큰 매핑(네온 아님). 사인=proficient green·코사인=accent·탄젠트=unknown red·활=learning amber.
const V = {
  arc: '--color-mastery-learning', sine: '--color-mastery-proficient', cos: '--color-accent',
  tan: '--color-mastery-unknown', hyp: '--color-accent-strong', chord: '--color-zinc-600',
  arrow: '--color-muted', grid: '--color-border', circle: '--color-zinc-700', bg: '--color-zinc-950', ink: '--color-text',
};
const FB: Record<string, string> = {
  '--color-mastery-learning': '#9F600C', '--color-mastery-proficient': '#2E7B4F', '--color-accent': '#39487D',
  '--color-mastery-unknown': '#C13D38', '--color-accent-strong': '#2D3963', '--color-zinc-600': '#B0A78F',
  '--color-muted': '#6B6350', '--color-border': '#E9E1CF', '--color-zinc-700': '#D7CDB5', '--color-zinc-950': '#FBF8F1', '--color-text': '#2A261E',
};

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

  useEffect(() => {
    const cv = canvasRef.current; if (!cv) return;
    const fit = () => {
      const box = cv.parentElement!.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      cv.width = box.width * dpr; cv.height = box.width * dpr; cv.style.height = `${box.width}px`;
      setSizeV((v) => v + 1);
    };
    fit(); window.addEventListener('resize', fit); return () => window.removeEventListener('resize', fit);
  }, []);

  // 그리기 — 색은 매 그릴 때 CSS변수에서 읽어 테마 적응
  useEffect(() => {
    const cv = canvasRef.current; if (!cv) return;
    const ctx = cv.getContext('2d'); if (!ctx) return;
    const cs = getComputedStyle(document.documentElement);
    const col = (k: keyof typeof V) => { const v = cs.getPropertyValue(V[k]).trim(); return v || FB[V[k]]; };
    const dpr = window.devicePixelRatio || 1;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = cv.width / dpr, H = cv.height / dpr;
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = col('bg'); ctx.fillRect(0, 0, W, H);   // 종이 배경
    const cx = W / 2 - W * 0.07, cy = H / 2, R = Math.min(W, H) * 0.35;
    const th = (angle * Math.PI) / 180;
    const px = cx + R * Math.cos(th), pyT = cy - R * Math.sin(th), pyB = cy + R * Math.sin(th);
    const line = (x1: number, y1: number, x2: number, y2: number, c: string, w: number, dash?: number[]) => {
      ctx.strokeStyle = c; ctx.lineWidth = w; ctx.setLineDash(dash || []);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); ctx.setLineDash([]);
    };
    line(cx, 0, cx, H, col('grid'), 1); line(0, cy, W, cy, col('grid'), 1);
    ctx.strokeStyle = col('circle'); ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(0,0,0,0.04)';
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(px, cy); ctx.lineTo(px, pyT); ctx.closePath(); ctx.fill();
    // 호(활)
    ctx.strokeStyle = col('arc'); ctx.lineWidth = hover === 'bow' ? 6 : 4;
    ctx.beginPath(); ctx.arc(cx, cy, R, -th, th); ctx.stroke();
    ctx.fillStyle = col('arc'); ctx.beginPath(); ctx.arc(px, pyT, 5, 0, 7); ctx.arc(px, pyB, 5, 0, 7); ctx.fill();
    line(px, cy, px, pyB, col('chord'), 1.5, [2, 2]);                          // 현 아래절반
    line(px, cy, px, pyT, col('sine'), hover === 'sine' || hover === 'chord' ? 6 : 4); // 사인(반현)
    line(cx, cy, px, pyT, col('hyp'), hover === 'sine' ? 2 : 3);               // 빗변
    line(cx, cy, px, cy, col('cos'), hover === 'cosine' ? 6 : 3);              // 코사인
    const tx = cx + R, ty = cy - R * Math.tan(th);
    line(px, pyT, tx, ty, col('arrow'), 1, [3, 3]);
    line(tx, cy, tx, ty, col('tan'), hover === 'tangent' ? 6 : 3);            // 탄젠트
    ctx.fillStyle = col('tan'); ctx.beginPath(); ctx.arc(tx, cy, 4, 0, 7); ctx.fill();
    line(cx - 30, cy, px, cy, col('arrow'), 2);                                // 화살
    ctx.fillStyle = col('arrow'); ctx.beginPath(); ctx.moveTo(px, cy); ctx.lineTo(px - 8, cy - 4); ctx.lineTo(px - 8, cy + 4); ctx.closePath(); ctx.fill();
    line(px, cy, cx + R, cy, col('ink'), 3);                                   // sagitta
    ctx.strokeStyle = col('arc'); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, 28, -th, 0); ctx.stroke();
    ctx.font = 'bold 12px system-ui,sans-serif';
    ctx.fillStyle = col('arc'); ctx.fillText('θ', cx + 34, cy - 9);
    ctx.fillStyle = col('hyp'); ctx.fillText('반지름 r', (cx + px) / 2 - 16, (cy + pyT) / 2 - 9);
    ctx.fillStyle = col('sine'); ctx.fillText('사인 (활시위 절반)', px + 9, (cy + pyT) / 2);
    ctx.fillStyle = col('cos'); ctx.fillText('코사인', (cx + px) / 2 - 14, cy + 17);
    ctx.fillStyle = col('tan'); ctx.fillText('탄젠트', tx + 8, (cy + ty) / 2);
    ctx.fillStyle = col('ink'); ctx.beginPath(); ctx.arc(cx, cy, 4, 0, 7); ctx.fill(); ctx.fillText('O', cx - 14, cy + 17);
  }, [angle, hover, sizeV]);

  useEffect(() => {
    if (!animating) return;
    let raf = 0;
    const tick = () => {
      setAngle((a) => { let n = a + 0.5 * dirRef.current; if (n >= 80) { n = 80; dirRef.current = -1; } else if (n <= 10) { n = 10; dirRef.current = 1; } return n; });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick); return () => cancelAnimationFrame(raf);
  }, [animating]);

  useEffect(() => {
    ensureKatex().then((katex) => {
      if (!katex) return;
      const s = Math.sin((angle * Math.PI) / 180);
      if (f1Ref.current) f1Ref.current.innerHTML = katex.renderToString(`\\sin(${angle.toFixed(1)}^\\circ)=\\frac{\\text{대변 (활시위의 절반)}}{\\text{빗변 } r}=\\frac{${s.toFixed(4)}}{1}=${s.toFixed(4)}`, { displayMode: true, throwOnError: false });
      if (f2Ref.current) f2Ref.current.innerHTML = katex.renderToString(`\\text{활시위 전체}=2\\times\\sin(${angle.toFixed(1)}^\\circ)=${(s * 2).toFixed(4)}`, { displayMode: true, throwOnError: false });
    }).catch(() => {});
  }, [angle]);

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
  const legends: Array<{ k: Hover; v: string; t: string }> = [
    { k: 'bow', v: V.arc, t: '활 (호)' }, { k: 'chord', v: V.chord, t: '활시위 (현)' },
    { k: 'sine', v: V.sine, t: '사인 (반현)' }, { k: 'cosine', v: V.cos, t: '코사인' }, { k: 'tangent', v: V.tan, t: '탄젠트' },
  ];
  const card: CSSProperties = { background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 12, padding: 14 };
  const chip: CSSProperties = { background: 'var(--color-surface-2)', border: '1px solid var(--color-border)', borderRadius: 8, padding: '4px 9px', fontSize: 13, fontFamily: 'monospace' };

  return (
    <div style={{ background: 'var(--color-bg)', color: 'var(--color-text)', border: '1px solid var(--color-border)', borderRadius: 14, padding: 14, maxWidth: 560, margin: '0 auto' }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12, fontSize: 13 }}>
        <span style={chip}>각도 θ <b style={{ color: `var(${V.arc})` }}>{angle.toFixed(1)}°</b></span>
        <span style={chip}>sin <b style={{ color: `var(${V.sine})` }}>{sinV}</b></span>
        <span style={chip}>cos <b style={{ color: `var(${V.cos})` }}>{cosV}</b></span>
      </div>
      <div style={card}>
        <div style={{ position: 'relative', width: '100%', borderRadius: 10, overflow: 'hidden', border: '1px solid var(--color-border)', cursor: 'crosshair' }}>
          <canvas ref={canvasRef} style={{ width: '100%', display: 'block' }} />
        </div>
        <p style={{ fontSize: 12, color: 'var(--color-subtle)', textAlign: 'center', margin: '10px 0 0' }}>💡 캔버스를 드래그하면 각도 θ를 직접 조절할 수 있습니다.</p>
        <div style={{ marginTop: 14 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--color-muted)', marginBottom: 4 }}><span>각도 θ</span><span style={{ fontFamily: 'monospace' }}>{angle.toFixed(1)}°</span></div>
          <input type="range" min={5} max={85} step={0.5} value={angle} onChange={(e) => { setAnimating(false); setAngle(parseFloat(e.target.value)); }} style={{ width: '100%', accentColor: 'var(--color-accent)' }} />
        </div>
        <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
          <button onClick={() => setAnimating((a) => !a)} style={{ flex: 1, padding: '8px', borderRadius: 8, border: '1px solid var(--color-accent-strong)', background: 'var(--color-accent)', color: '#FBF8F1', fontWeight: 700, cursor: 'pointer' }}>{animating ? '⏸ 일시정지' : '▶ 자동 회전'}</button>
          <button onClick={() => { setAnimating(false); setAngle(45); }} style={{ padding: '8px 16px', borderRadius: 8, border: '1px solid var(--color-border-strong)', background: 'var(--color-surface-2)', color: 'var(--color-text)', cursor: 'pointer' }}>초기화</button>
        </div>
      </div>
      <div style={{ ...card, marginTop: 12, display: 'flex', flexWrap: 'wrap', gap: 8, fontSize: 12 }}>
        {legends.map((l) => (
          <span key={l.k} onMouseEnter={() => setHover(l.k)} onMouseLeave={() => setHover(null)} style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '3px 7px', borderRadius: 6, cursor: 'pointer', background: hover === l.k ? 'var(--color-surface-2)' : 'transparent' }}>
            <span style={{ width: 12, height: 4, borderRadius: 2, background: `var(${l.v})`, display: 'inline-block' }} />{l.t}
          </span>
        ))}
      </div>
      <div style={{ ...card, marginTop: 12, background: 'var(--color-surface-2)' }}>
        <div ref={f1Ref} style={{ textAlign: 'center', padding: '4px 0', overflowX: 'auto' }} />
        <div style={{ height: 1, background: 'var(--color-border)', margin: '8px 0' }} />
        <div ref={f2Ref} style={{ textAlign: 'center', color: `var(${V.arc})`, padding: '4px 0', overflowX: 'auto' }} />
        <p style={{ fontSize: 11, color: 'var(--color-muted)', marginTop: 8, textAlign: 'center' }}>단위원(r=1)에서 <b style={{ color: `var(${V.sine})` }}>sin θ = 활시위 절반의 실제 길이</b></p>
      </div>
    </div>
  );
}
