import { useEffect, useRef } from 'react';
import { ensureKatex, renderMathSegments } from '../lib/mathish';

// 기출 redraw 그래프 렌더러 — function-plot 곡선/음영/직선 + 라벨은 KaTeX SSOT(mathish).
//   ★라벨은 SVG 안(foreignObject·클립패스 quirk로 잘림)이 아니라 **wrapper 위 HTML overlay div**로 렌더:
//   일반 HTML이라 폭 실측 정확 + 캔버스 안 클램프 신뢰. text/label 은 KaTeX TeX($ 없으면 자동 감쌈).
export type RPSpec = {
  range: [number, number];
  yRange: [number, number];
  curves?: Array<{ fn: string; range?: [number, number]; closed?: boolean }>;
  lines?: Array<{ from: [number, number]; to: [number, number]; dashed?: boolean }>;
  points?: Array<{ x: number; y: number; label?: string; dir?: string; open?: boolean }>;
  regions?: Array<{ pts: Array<[number, number]>; opacity?: number }>;
  texts?: Array<{ x: number; y: number; text: string; dir?: string }>;
  title?: string;
};

// dx=앵커 가로offset, dy=라벨박스 top offset(라벨 높이 ~18px 기준)
const DIR: Record<string, [number, number]> = {
  '위': [0, -20], '아래': [0, 6], '좌': [-8, -9], '우': [8, -9],
  '좌하': [-8, 3], '우하': [8, 3], '좌상': [-8, -20], '우상': [8, -20],
};

export default function RedrawPlot({ spec, width = 420, height = 360 }: { spec: RPSpec; width?: number; height?: number }) {
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    let cancel = false;
    Promise.all([import('function-plot'), ensureKatex()]).then(([mod, katex]) => {
      const fp = ((mod as unknown as { default?: unknown }).default ?? mod) as (o: unknown) => { meta: { xScale: (n: number) => number; yScale: (n: number) => number } };
      const wrap = ref.current;
      if (cancel || !wrap) return;
      wrap.innerHTML = '';
      const data: Array<Record<string, unknown>> = [];
      for (const c of spec.curves ?? []) {
        const d: Record<string, unknown> = { fn: c.fn, color: '#1a1a1a', graphType: 'polyline', nSamples: 900 };
        if (c.range) d.range = c.range;
        if (c.closed) d.closed = true;
        data.push(d);
      }
      const closedPts = (spec.points ?? []).filter((p) => !p.open).map((p) => [p.x, p.y]);
      if (closedPts.length) data.push({ points: closedPts, fnType: 'points', graphType: 'scatter', color: '#1a1a1a' });
      // ★데이터 도메인을 ~7% 패딩해 가장자리 라벨(곡선끝·x=c 하단)이 캔버스 끝에 잘리지 않게 여백 확보
      const pX = (spec.range[1] - spec.range[0]) * 0.07, pY = (spec.yRange[1] - spec.yRange[0]) * 0.09;
      const dom: [number, number] = [spec.range[0] - pX, spec.range[1] + pX];
      const ydom: [number, number] = [spec.yRange[0] - pY, spec.yRange[1] + pY];
      let inst;
      try {
        inst = fp({ target: wrap, width, height, grid: false, xAxis: { domain: dom }, yAxis: { domain: ydom }, tip: { xLine: false, yLine: false }, data });
      } catch (e) { wrap.textContent = 'plot err: ' + e; return; }
      try {
        const xS = inst.meta.xScale, yS = inst.meta.yScale;
        const svg = wrap.querySelector('svg');
        const content = (svg?.querySelector('.content') ?? svg) as SVGElement | null;
        const NS = 'http://www.w3.org/2000/svg';
        svg?.querySelectorAll('path').forEach((p) => (p as Element).setAttribute('stroke-width', '1.9'));
        svg?.querySelectorAll('.tick, .domain, .x.axis, .y.axis').forEach((t) => t.remove());
        svg?.querySelectorAll('[clip-path]').forEach((e) => e.removeAttribute('clip-path'));
        // 굵은 x·y축 + 화살표
        const defs = document.createElementNS(NS, 'defs');
        defs.innerHTML = '<marker id="rax" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker>';
        svg?.insertBefore(defs, svg.firstChild);
        const ax = (x1: number, y1: number, x2: number, y2: number) => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', String(x1)); l.setAttribute('y1', String(y1)); l.setAttribute('x2', String(x2)); l.setAttribute('y2', String(y2)); l.setAttribute('stroke', '#1a1a1a'); l.setAttribute('stroke-width', '1.4'); l.setAttribute('marker-end', 'url(#rax)'); content?.appendChild(l); };
        if (spec.yRange[0] <= 0 && spec.yRange[1] >= 0) ax(xS(dom[0]), yS(0), xS(dom[1]), yS(0));
        if (spec.range[0] <= 0 && spec.range[1] >= 0) ax(xS(0), yS(ydom[0]), xS(0), yS(ydom[1]));
        for (const ln of spec.lines ?? []) {
          const l = document.createElementNS(NS, 'line');
          l.setAttribute('x1', String(xS(ln.from[0]))); l.setAttribute('y1', String(yS(ln.from[1])));
          l.setAttribute('x2', String(xS(ln.to[0]))); l.setAttribute('y2', String(yS(ln.to[1])));
          l.setAttribute('stroke', '#1a1a1a'); l.setAttribute('stroke-width', '1.6');
          if (ln.dashed) l.setAttribute('stroke-dasharray', '6,4');
          content?.appendChild(l);
        }
        for (const rg of spec.regions ?? []) {
          const poly = document.createElementNS(NS, 'polygon');
          poly.setAttribute('points', rg.pts.map(([x, y]) => `${xS(x)},${yS(y)}`).join(' '));
          poly.setAttribute('fill', '#c9c9c9'); poly.setAttribute('fill-opacity', String(rg.opacity ?? 0.5)); poly.setAttribute('stroke', 'none');
          content?.insertBefore(poly, content?.firstChild ?? null);
        }
        for (const p of spec.points ?? []) {   // 빈원(불연속)
          if (p.open) {
            const c = document.createElementNS(NS, 'circle');
            c.setAttribute('cx', String(xS(p.x))); c.setAttribute('cy', String(yS(p.y))); c.setAttribute('r', '4.5');
            c.setAttribute('fill', '#fff'); c.setAttribute('stroke', '#1a1a1a'); c.setAttribute('stroke-width', '1.6');
            content?.appendChild(c);
          }
        }
        // ★라벨 = wrapper 위 HTML overlay div(SVG 밖). 폰트 로드 후 실측·클램프.
        const addLabel = (tex: string, sx: number, sy: number, dir?: string) => {
          const wrapped = /\$/.test(tex) ? tex : `$${tex}$`;
          let html = tex;
          try { if (katex) html = renderMathSegments(wrapped, katex); } catch { /* plain */ }
          const lab = document.createElement('div');
          lab.style.cssText = 'position:absolute;white-space:nowrap;font-size:15.5px;color:#111;pointer-events:none;line-height:1.1;';
          lab.innerHTML = html;
          wrap.appendChild(lab);
          const r = lab.getBoundingClientRect();
          const w2 = r.width || tex.length * 9, h2 = r.height || 18;
          const d = dir ?? '우상';
          const [dx, dy] = DIR[d] ?? [8, -20];
          const axx = sx + dx;
          let lx = d.includes('좌') ? axx - w2 : (d === '위' || d === '아래') ? axx - w2 / 2 : axx;
          lx = Math.max(1, Math.min(lx, width - w2 - 1));
          const ly = Math.max(1, Math.min(sy + dy, height - h2 - 1));
          lab.style.left = `${lx}px`; lab.style.top = `${ly}px`;
        };
        const doLabels = () => {
          for (const tx of spec.texts ?? []) addLabel(tx.text, xS(tx.x), yS(tx.y), tx.dir);
          for (const p of spec.points ?? []) if (p.label) addLabel(p.label, xS(p.x), yS(p.y), p.dir ?? '우상');
          (window as unknown as { __figReady?: boolean }).__figReady = true;
        };
        const fr = (document as unknown as { fonts?: { ready?: Promise<unknown> } }).fonts?.ready;
        if (fr) fr.then(() => requestAnimationFrame(doLabels)); else doLabels();
      } catch { (window as unknown as { __figReady?: boolean }).__figReady = true; }
    });
    return () => { cancel = true; };
  }, [JSON.stringify(spec), width, height]);
  return <div ref={ref} style={{ position: 'relative', background: '#fff', borderRadius: 8, width, height, overflow: 'hidden' }} />;
}
