import { useEffect, useRef } from 'react';
import { ensureKatex, renderMathSegments } from '../lib/mathish';

// 기출 redraw 그래프 전용 렌더러 — 학습노트/튜터와 같은 function-plot 엔진 +
//   라벨은 KaTeX SSOT(mathish: ensureKatex/renderMathSegments)로 foreignObject 렌더.
//   curves(함수식·fill) · lines(직선/세로선/점근선) · points(라벨·빈원/채운원) · regions(다각형 음영) · texts(자유 라벨).
//   ★라벨 text/label 은 KaTeX TeX (예 "y=\\log_{2}x"·"x=\\frac{\\pi}{2}"). $ 없으면 자동으로 감싼다.
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

// (dx=앵커 가로offset, dy=라벨박스 top offset). H=30 기준.
const DIR: Record<string, [number, number]> = {
  '위': [0, -34], '아래': [0, 3], '좌': [-6, -15], '우': [6, -15],
  '좌하': [-6, 2], '우하': [6, 2], '좌상': [-6, -30], '우상': [6, -30],
};
const XHTML = 'http://www.w3.org/1999/xhtml';

export default function RedrawPlot({ spec, width = 420, height = 360 }: { spec: RPSpec; width?: number; height?: number }) {
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    let cancel = false;
    Promise.all([import('function-plot'), ensureKatex()]).then(([mod, katex]) => {
      const fp = ((mod as unknown as { default?: unknown }).default ?? mod) as (o: unknown) => { meta: { xScale: (n: number) => number; yScale: (n: number) => number } };
      if (cancel || !ref.current) return;
      ref.current.innerHTML = '';
      const data: Array<Record<string, unknown>> = [];
      for (const c of spec.curves ?? []) {
        const d: Record<string, unknown> = { fn: c.fn, color: '#1a1a1a', graphType: 'polyline', nSamples: 900 };
        if (c.range) d.range = c.range;
        if (c.closed) d.closed = true;
        data.push(d);
      }
      const closedPts = (spec.points ?? []).filter((p) => !p.open).map((p) => [p.x, p.y]);
      if (closedPts.length) data.push({ points: closedPts, fnType: 'points', graphType: 'scatter', color: '#1a1a1a' });
      let inst;
      try {
        inst = fp({ target: ref.current, width, height, grid: false, xAxis: { domain: spec.range }, yAxis: { domain: spec.yRange }, tip: { xLine: false, yLine: false }, data });
      } catch (e) { if (ref.current) ref.current.textContent = 'plot err: ' + e; return; }
      try {
        const xS = inst.meta.xScale, yS = inst.meta.yScale;
        const svg = ref.current.querySelector('svg');
        const content = (svg?.querySelector('.content') ?? svg) as SVGElement | null;
        const NS = 'http://www.w3.org/2000/svg';
        // 교과서식 정제: 데이터 선 굵게 + function-plot 기본 눈금/축 제거(자체 축으로 대체)
        svg?.querySelectorAll('path').forEach((p) => (p as Element).setAttribute('stroke-width', '1.9'));
        svg?.querySelectorAll('.tick, .domain, .x.axis, .y.axis').forEach((t) => t.remove());
        svg?.querySelectorAll('[clip-path]').forEach((e) => e.removeAttribute('clip-path'));  // ★플롯영역 클립 제거 — 여백의 라벨(곡선식·축눈금)이 잘리던 원인
        // 굵은 x·y축 + 화살표
        const defs = document.createElementNS(NS, 'defs');
        defs.innerHTML = '<marker id="rax" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker>';
        svg?.insertBefore(defs, svg.firstChild);
        const ax = (x1: number, y1: number, x2: number, y2: number) => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', String(x1)); l.setAttribute('y1', String(y1)); l.setAttribute('x2', String(x2)); l.setAttribute('y2', String(y2)); l.setAttribute('stroke', '#1a1a1a'); l.setAttribute('stroke-width', '1.4'); l.setAttribute('marker-end', 'url(#rax)'); content?.appendChild(l); };
        if (spec.yRange[0] <= 0 && spec.yRange[1] >= 0) ax(xS(spec.range[0]), yS(0), xS(spec.range[1]), yS(0));
        if (spec.range[0] <= 0 && spec.range[1] >= 0) ax(xS(0), yS(spec.yRange[0]), xS(0), yS(spec.yRange[1]));
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
        // KaTeX 라벨 = foreignObject. dir 로 정렬(좌=우측정렬·중앙=가운데). px,py=앵커 투영좌표.
        const H = 30;
        const measEl = document.createElement('div');   // off-screen 실측용(SVG 밖 일반 HTML → 정확한 폭)
        measEl.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap;font-size:15.5px;';
        document.body.appendChild(measEl);
        const addLabel = (tex: string, px: number, py: number, dir?: string) => {
          const wrapped = /\$/.test(tex) ? tex : `$${tex}$`;
          let html = tex;
          try { if (katex) html = renderMathSegments(wrapped, katex); } catch { /* plain */ }
          measEl.innerHTML = html;
          const w2 = Math.max(measEl.getBoundingClientRect().width, measEl.scrollWidth, tex.length * 8) * 1.32 + 8;   // 실측 + 여유(KaTeX 실폭 보정 → 클립/잘림 방지)
          const d = dir ?? '우상';
          const [dx, dy] = DIR[d] ?? [6, -30];
          const ax2 = px + dx;
          let fx = d.includes('좌') ? ax2 - w2 : (d === '위' || d === '아래') ? ax2 - w2 / 2 : ax2;
          fx = Math.max(2, Math.min(fx, width - w2 - 2));   // 캔버스 안 클램프(잘림 방지)
          const fo = document.createElementNS(NS, 'foreignObject');
          fo.setAttribute('x', String(fx)); fo.setAttribute('y', String(Math.max(0, Math.min(py + dy, height - H))));
          fo.setAttribute('width', String(Math.ceil(w2) + 20)); fo.setAttribute('height', String(H)); fo.setAttribute('overflow', 'visible');
          const div = document.createElementNS(XHTML, 'div') as unknown as HTMLDivElement;
          div.setAttribute('style', `font-size:15.5px;color:#111;white-space:nowrap;line-height:${H}px;height:${H}px;`);
          div.innerHTML = html;
          fo.appendChild(div); content?.appendChild(fo);
        };
        for (const p of spec.points ?? []) {   // 빈원(불연속)은 즉시
          if (p.open) {
            const c = document.createElementNS(NS, 'circle');
            c.setAttribute('cx', String(xS(p.x))); c.setAttribute('cy', String(yS(p.y))); c.setAttribute('r', '4.5');
            c.setAttribute('fill', '#fff'); c.setAttribute('stroke', '#1a1a1a'); c.setAttribute('stroke-width', '1.6');
            content?.appendChild(c);
          }
        }
        // ★라벨은 폰트(KaTeX) 로드 후 렌더 — getBoundingClientRect 폭이 정확해야 클램프/정렬이 맞는다(폰트 전엔 0/오측정).
        const doLabels = () => {
          for (const tx of spec.texts ?? []) addLabel(tx.text, xS(tx.x), yS(tx.y), tx.dir);
          for (const p of spec.points ?? []) if (p.label) addLabel(p.label, xS(p.x), yS(p.y), p.dir ?? '우상');
          measEl.remove();
          (window as unknown as { __figReady?: boolean }).__figReady = true;
        };
        const fr = (document as unknown as { fonts?: { ready?: Promise<unknown> } }).fonts?.ready;
        if (fr) fr.then(() => requestAnimationFrame(doLabels)); else doLabels();
      } catch { (window as unknown as { __figReady?: boolean }).__figReady = true; }
    });
    return () => { cancel = true; };
  }, [JSON.stringify(spec), width, height]);
  return <div ref={ref} style={{ background: '#fff', borderRadius: 8, padding: 4 }} />;
}
