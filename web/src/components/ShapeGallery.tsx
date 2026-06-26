import { useEffect, useRef, useState } from 'react';
import { recognizeShape, shapeToPoints, type P } from '../lib/shape-recognize';

// 도형 인식기 시각 검증 — 합성 손그림(회색) → 인식 결과(파랑) 나란히. /dev/shape-gallery.
const noise = (i: number) => ((i * 9301 + 49297) % 233280) / 233280 * 6 - 3;
const edge = (a: P, b: P, n: number, o: number): P[] => { const r: P[] = []; for (let i = 0; i <= n; i++) { const t = i / n; r.push({ x: a.x + (b.x - a.x) * t + noise(i + o), y: a.y + (b.y - a.y) * t + noise(i + o + 50) }); } return r; };
const poly = (vs: P[], per: number): P[] => { const r: P[] = []; for (let i = 0; i < vs.length; i++) r.push(...edge(vs[i], vs[(i + 1) % vs.length], per, i * 100)); return r; };
const ngon = (cx: number, cy: number, R: number, n: number, rot = 0): P[] => { const v: P[] = []; for (let i = 0; i < n; i++) { const t = rot + i / n * 2 * Math.PI; v.push({ x: cx + R * Math.cos(t), y: cy + R * Math.sin(t) }); } return v; };
const ring = (cx: number, cy: number, rx: number, ry: number): P[] => { const r: P[] = []; for (let i = 0; i <= 60; i++) { const t = i / 60 * 2 * Math.PI; r.push({ x: cx + rx * Math.cos(t) + noise(i), y: cy + ry * Math.sin(t) + noise(i + 30) }); } return r; };

const SAMPLES: { label: string; pts: P[] }[] = [
  { label: '직선', pts: edge({ x: 30, y: 120 }, { x: 230, y: 128 }, 40, 0) },
  { label: '정삼각형', pts: poly(ngon(130, 120, 80, 3, -Math.PI / 2), 22) },
  { label: '직각삼각형', pts: poly([{ x: 45, y: 45 }, { x: 45, y: 195 }, { x: 215, y: 195 }], 22) },
  { label: '사각형', pts: poly([{ x: 45, y: 50 }, { x: 215, y: 50 }, { x: 215, y: 190 }, { x: 45, y: 190 }], 22) },
  { label: '마름모(회전사각)', pts: poly(ngon(130, 120, 90, 4, 0), 22) },
  { label: '오각형', pts: poly(ngon(130, 120, 85, 5, -Math.PI / 2), 18) },
  { label: '원', pts: ring(130, 120, 80, 80) },
  { label: '타원', pts: ring(130, 120, 100, 55) },
];

function Card({ label, pts }: { label: string; pts: P[] }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const [kind, setKind] = useState('');
  useEffect(() => {
    const c = ref.current; if (!c) return; const ctx = c.getContext('2d'); if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2); c.width = 260 * dpr; c.height = 240 * dpr; ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, 260, 240); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.strokeStyle = 'rgba(140,140,140,0.5)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y); for (const p of pts) ctx.lineTo(p.x, p.y); ctx.stroke();
    const rec = recognizeShape(pts); setKind(rec?.kind ?? 'null');
    if (rec) { const cp = shapeToPoints(rec); ctx.strokeStyle = '#39487D'; ctx.lineWidth = 2.8; ctx.beginPath(); ctx.moveTo(cp[0].x, cp[0].y); for (const p of cp) ctx.lineTo(p.x, p.y); ctx.stroke(); }
  }, []);
  return (
    <div style={{ border: '1px solid var(--color-border)', borderRadius: 10, padding: 8, background: 'var(--color-surface)' }}>
      <canvas ref={ref} style={{ width: 260, height: 240, display: 'block' }} />
      <div style={{ fontSize: 13, marginTop: 4, color: 'var(--color-text)' }}>{label} → <b style={{ color: 'var(--color-accent)' }}>{kind}</b></div>
    </div>
  );
}

export default function ShapeGallery() {
  return <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14 }}>{SAMPLES.map((s, i) => <Card key={i} {...s} />)}</div>;
}
