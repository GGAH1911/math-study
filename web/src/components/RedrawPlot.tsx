import { useEffect, useRef } from 'react';

// 기출 redraw 그래프 전용 렌더러 — 학습노트/튜터와 같은 function-plot 엔진 사용
//   (corrector 의 수동 폴리곤/곡선 대신 진짜 수학 플로팅: 곡선·fill 음영·직선·교점 정확).
//   curves(함수식·fill·범위) · lines(임의 직선/세로선=parametric) · points(라벨·빈원/채운원).
export type RPSpec = {
  range: [number, number];                  // x축 도메인
  yRange: [number, number];                 // y축 도메인
  curves?: Array<{ fn: string; range?: [number, number]; closed?: boolean }>;  // closed=x축까지 음영(∫)
  lines?: Array<{ from: [number, number]; to: [number, number]; dashed?: boolean }>;
  points?: Array<{ x: number; y: number; label?: string; dir?: string; open?: boolean }>;  // open=빈원(불연속)
  regions?: Array<{ pts: Array<[number, number]>; opacity?: number }>;  // 임의 다각형 음영(곡선변은 점샘플로). 곡선/선 뒤에 깔림
  texts?: Array<{ x: number; y: number; text: string; dir?: string }>;  // 곡선식·축눈금 등 자유 라벨
  title?: string;
};

const DIR: Record<string, [number, number]> = {
  '위': [0, -10], '아래': [2, 18], '좌': [-14, 5], '우': [10, 5],
  '좌하': [-15, 17], '우하': [10, 17], '좌상': [-15, -8], '우상': [11, -9],
};

export default function RedrawPlot({ spec, width = 420, height = 360 }: { spec: RPSpec; width?: number; height?: number }) {
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    let cancel = false;
    import('function-plot').then((mod) => {
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
      // 직선/세로선/점근선은 후처리 SVG 로(정확한 끝점 + dashed 지원)
      const closedPts = (spec.points ?? []).filter((p) => !p.open).map((p) => [p.x, p.y]);
      if (closedPts.length) data.push({ points: closedPts, fnType: 'points', graphType: 'scatter', color: '#1a1a1a' });
      let inst;
      try {
        inst = fp({ target: ref.current, width, height, grid: false, xAxis: { domain: spec.range }, yAxis: { domain: spec.yRange }, tip: { xLine: false, yLine: false }, data });
      } catch (e) { if (ref.current) ref.current.textContent = 'plot err: ' + e; return; }
      // 라벨 + 빈원(open)을 투영좌표로 SVG 에 직접 추가
      try {
        const xS = inst.meta.xScale, yS = inst.meta.yScale;
        const svg = ref.current.querySelector('svg');
        const content = (svg?.querySelector('.content') ?? svg) as SVGElement | null;
        const NS = 'http://www.w3.org/2000/svg';
        const clamp = (cx: number, cy: number, txt: string): [number, number] => [Math.max(3, Math.min(cx, width - 6 - txt.length * 7)), Math.max(13, Math.min(cy, height - 5))];  // 라벨 캔버스 안으로
        // 교과서식 정제: 데이터 선 굵게 + function-plot 기본 눈금/축 제거(자체 축으로 대체)
        svg?.querySelectorAll('path').forEach((p) => (p as Element).setAttribute('stroke-width', '1.9'));  // 곡선/선 굵게
        svg?.querySelectorAll('.tick, .domain, .x.axis, .y.axis').forEach((t) => t.remove());  // function-plot 기본 눈금·축 제거(자체 축 사용)
        // 굵은 x·y축 + 화살표(원점 통과, 도형 너머 연장)
        const defs = document.createElementNS(NS, 'defs');
        defs.innerHTML = '<marker id="rax" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker>';
        svg?.insertBefore(defs, svg.firstChild);
        const ax = (x1: number, y1: number, x2: number, y2: number) => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', String(x1)); l.setAttribute('y1', String(y1)); l.setAttribute('x2', String(x2)); l.setAttribute('y2', String(y2)); l.setAttribute('stroke', '#1a1a1a'); l.setAttribute('stroke-width', '1.4'); l.setAttribute('marker-end', 'url(#rax)'); content?.appendChild(l); };
        if (spec.yRange[0] <= 0 && spec.yRange[1] >= 0) ax(xS(spec.range[0]), yS(0), xS(spec.range[1]), yS(0));
        if (spec.range[0] <= 0 && spec.range[1] >= 0) ax(xS(0), yS(spec.yRange[0]), xS(0), yS(spec.yRange[1]));
        for (const ln of spec.lines ?? []) {   // 직선/세로선/점근선 (dashed 지원)
          const l = document.createElementNS(NS, 'line');
          l.setAttribute('x1', String(xS(ln.from[0]))); l.setAttribute('y1', String(yS(ln.from[1])));
          l.setAttribute('x2', String(xS(ln.to[0]))); l.setAttribute('y2', String(yS(ln.to[1])));
          l.setAttribute('stroke', '#1a1a1a'); l.setAttribute('stroke-width', '1.6');
          if (ln.dashed) l.setAttribute('stroke-dasharray', '6,4');
          content?.appendChild(l);
        }
        for (const rg of spec.regions ?? []) {   // 음영 다각형 = 곡선/선 뒤(맨앞 삽입)
          const poly = document.createElementNS(NS, 'polygon');
          poly.setAttribute('points', rg.pts.map(([x, y]) => `${xS(x)},${yS(y)}`).join(' '));
          poly.setAttribute('fill', '#c9c9c9'); poly.setAttribute('fill-opacity', String(rg.opacity ?? 0.5)); poly.setAttribute('stroke', 'none');
          content?.insertBefore(poly, content?.firstChild ?? null);
        }
        for (const tx of spec.texts ?? []) {   // 자유 라벨(곡선식·축눈금)
          const [dx, dy] = DIR[tx.dir ?? '우'] ?? [10, 5];
          const t = document.createElementNS(NS, 'text');
          const [ctx2, cty2] = clamp(xS(tx.x) + dx, yS(tx.y) + dy, tx.text);
          t.setAttribute('x', String(ctx2)); t.setAttribute('y', String(cty2));
          t.setAttribute('font-size', '15'); t.setAttribute('font-family', 'KaTeX_Math, Times, serif'); t.setAttribute('font-style', 'italic'); t.setAttribute('fill', '#111');
          t.textContent = tx.text; content?.appendChild(t);
        }
        for (const p of spec.points ?? []) {
          if (p.open) {
            const c = document.createElementNS(NS, 'circle');
            c.setAttribute('cx', String(xS(p.x))); c.setAttribute('cy', String(yS(p.y))); c.setAttribute('r', '4.5');
            c.setAttribute('fill', '#fff'); c.setAttribute('stroke', '#1a1a1a'); c.setAttribute('stroke-width', '1.6');
            content?.appendChild(c);
          }
          if (p.label) {
            const [dx, dy] = DIR[p.dir ?? '우상'] ?? [11, -9];
            const t = document.createElementNS(NS, 'text');
            const [clx, cly] = clamp(xS(p.x) + dx, yS(p.y) + dy, p.label);
            t.setAttribute('x', String(clx)); t.setAttribute('y', String(cly));
            t.setAttribute('font-size', '16'); t.setAttribute('font-family', 'KaTeX_Math, Times, serif'); t.setAttribute('font-style', 'italic'); t.setAttribute('fill', '#111');
            t.textContent = p.label; content?.appendChild(t);
          }
        }
      } catch { /* 라벨은 best-effort */ }
      (window as unknown as { __figReady?: boolean }).__figReady = true;
    });
    return () => { cancel = true; };
  }, [JSON.stringify(spec), width, height]);
  return <div ref={ref} style={{ background: '#fff', borderRadius: 8, padding: 4 }} />;
}
