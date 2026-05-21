// Interactive 탐구 그래픽 — 슬라이더 값을 mathjs scope로 받아 도형/숫자를
// 실시간 갱신. 정적 Geometry/Plot에 동적 layer를 얹은 wrapper.
//
// 사용: chat fence ```interactive ... ```  (LLM이 spec emit)
//
// Spec 형식: web/src/data/interactive-samples.ts 참고. 좌표/숫자 자리에
// `"=expr"` 문자열이 오면 mathjs로 평가 (scope 변수 사용 가능).

import { useEffect, useMemo, useState, useRef } from 'react';
import Geometry, { type GeomSpec, type GeomShape } from './Geometry';
import Geometry3D, { type Geom3DSpec } from './Geometry3D';
import Graph, { type PlotSpec } from './Graph';
import { MathishText } from '../lib/mathish';
import type { InteractiveSpec } from '../data/interactive-samples';

// mathjs는 function-plot 의존성으로 이미 번들에 포함됨.
import { create, all } from 'mathjs';

const math = create(all);

// `"=expr"` 형식 문자열을 mathjs로 평가. 일반 값은 그대로 반환.
// LLM 이 박을 수 있는 유니코드 수학 기호 → mathjs ASCII 매핑.
// √2/2 → sqrt(2)/2, π → pi 등. mathjs 가 이걸 그대로 못 받음.
function normalizeMathExpr(s: string): string {
  return s
    .replace(/√/g, 'sqrt')
    .replace(/π/g, 'pi')
    .replace(/×/g, '*')
    .replace(/÷/g, '/')
    .replace(/−/g, '-')   // unicode minus
    .replace(/⋅/g, '*')
    .replace(/·/g, '*');
}

// 배열/객체는 재귀적으로 walk.
function resolveValue(value: unknown, scope: Record<string, unknown>): unknown {
  if (typeof value === 'string' && value.startsWith('=')) {
    try { return math.evaluate(normalizeMathExpr(value.slice(1)), scope); }
    catch { return NaN; }
  }
  if (Array.isArray(value)) return value.map((v) => resolveValue(v, scope));
  if (value && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value)) out[k] = resolveValue(v, scope);
    return out;
  }
  return value;
}

type InteractiveProps = {
  spec: InteractiveSpec;
  width?: number;
  height?: number;
  onOpen?: () => void;
  interactive?: boolean;
  hideCaption?: boolean;
  noBroadcast?: boolean;
};

export default function Interactive({
  spec, width = 380, height, onOpen, interactive, hideCaption, noBroadcast,
}: InteractiveProps) {
  // 슬라이더 값 state — 초기값은 spec.params[].init.
  const [values, setValues] = useState<Record<string, number>>(() => {
    const init: Record<string, number> = {};
    for (const p of spec.params ?? []) init[p.name] = p.init;
    return init;
  });

  // spec.scope 를 statement 단위로 분리 + 각각 컴파일. 한 statement broken 이라도
  // 나머지는 정상 평가되도록 (LLM 이 한 식만 잘못 박은 경우 전체 fail 안 함).
  const compiledStatements = useMemo(() => {
    if (!spec.scope) return [] as Array<{ src: string; node: { evaluate: (s: Record<string, unknown>) => unknown } | null }>;
    const raw = normalizeMathExpr(spec.scope);
    const stmts = raw.split(/[;\n]/).map((s) => s.trim()).filter(Boolean);
    return stmts.map((stmt) => {
      try {
        const node = math.parse(stmt).compile() as { evaluate: (s: Record<string, unknown>) => unknown };
        return { src: stmt, node };
      } catch {
        return { src: stmt, node: null as { evaluate: (s: Record<string, unknown>) => unknown } | null };
      }
    });
  }, [spec.scope]);

  // 매 슬라이더 변경마다 scope 평가 → 도형/리드아웃 리졸브.
  const { resolvedGeom, resolvedGeom3d, resolvedPlot, readoutValues, evalError } = useMemo(() => {
    const scope: Record<string, unknown> = { ...values };
    for (const { node } of compiledStatements) {
      if (!node) continue;
      try { node.evaluate(scope); }
      catch { /* skip broken statement — 다른 정상 statement 는 계속 평가 */ }
    }
    const geom = spec.geometry
      ? (resolveValue(spec.geometry, scope) as GeomSpec)
      : undefined;
    if (geom?.shapes) {
      geom.shapes = geom.shapes.filter((s) => isFinite(s)) as GeomShape[];
    }
    const geom3d = spec.geometry3d
      ? (resolveValue(spec.geometry3d, scope) as Geom3DSpec)
      : undefined;
    // Plot: 함수 문자열은 그대로 둔다 (function-plot이 자체 mathjs로 평가).
    // 슬라이더 + scope 변수를 fns[].scope에 주입.
    let plot: PlotSpec | undefined;
    if (spec.plot) {
      // function-plot의 expression scope는 builtin pi/e 를 자동 포함하지
      // 않는 경우가 있어, scope에 직접 주입해서 LLM이 pi/e 를 안심하고
      // 식에 쓸 수 있게 한다.
      const liveScope: Record<string, number> = { pi: Math.PI, e: Math.E };
      for (const [k, v] of Object.entries(scope)) {
        if (typeof v === 'number' && Number.isFinite(v)) liveScope[k] = v;
      }
      plot = {
        ...spec.plot,
        // fn 문자열은 그대로 (function-plot이 자체 평가). 다만 `range`/`scope`
        // 등 슬라이더 반응이 필요한 구조적 필드는 resolveValue로 처리.
        fns: spec.plot.fns?.map((f) => ({
          ...f,
          scope: { ...(f.scope ?? {}), ...liveScope },
          range: f.range
            ? (resolveValue(f.range, scope) as [number, number])
            : f.range,
        })),
        points: spec.plot.points
          ? (resolveValue(spec.plot.points, scope) as PlotSpec['points'])
          : spec.plot.points,
      };
    }
    const readouts = (spec.readout ?? []).map((r) => {
      try {
        const v = math.evaluate(normalizeMathExpr(r.expr), scope) as number;
        return { ...r, value: typeof v === 'number' ? v : NaN };
      } catch {
        // readout 한 식 broken 이라도 다른 readout / 도형은 정상 — 그 슬롯만 NaN.
        return { ...r, value: NaN };
      }
    });
    return { resolvedGeom: geom, resolvedGeom3d: geom3d, resolvedPlot: plot, readoutValues: readouts, evalError: null as string | null };
  }, [values, compiledStatements, spec.geometry, spec.geometry3d, spec.plot, spec.readout]);

  // 현재 슬라이더 값 + readout을 한 줄 텍스트로 직렬화. LLM이 채팅 메시지에서
  // 이 메타 라인을 보고 학생의 실제 상태를 인지하도록.
  const serializeState = (): string => {
    const paramParts = (spec.params ?? []).map((p) => {
      const v = values[p.name] ?? p.init;
      return `${p.label ?? p.name}=${fmtNum(v)}${p.unit ?? ''}`;
    });
    const readParts = readoutValues
      .filter((r) => Number.isFinite(r.value))
      .map((r) => `${r.label}=${fmtNum(r.value, r.digits ?? 3)}${r.unit ?? ''}`);
    return `[현재 상태] ${[...paramParts, ...readParts].join(', ')}`;
  };
  const onShareState = () => {
    if (typeof window === 'undefined') return;
    window.dispatchEvent(new CustomEvent('math-study:chat-insert', {
      detail: { text: serializeState() },
    }));
  };

  // 슬라이더 UI — Plot의 기존 마크업과 동일한 스타일.
  const controls = (
    <div className="mt-3 pt-3 border-t border-zinc-800 space-y-2">
      {(spec.params ?? []).map((p) => (
        <label key={p.name} className="flex items-center gap-3 text-xs">
          <span className="font-mono text-zinc-300 w-12 shrink-0 text-right">
            {p.label ?? p.name}
          </span>
          <input
            type="range"
            min={p.min}
            max={p.max}
            step={p.step ?? (p.max - p.min) / 100}
            value={values[p.name] ?? p.init}
            onChange={(e) => setValues((v) => ({ ...v, [p.name]: parseFloat(e.target.value) }))}
            className="flex-1 accent-indigo-400"
          />
          <span className="font-mono text-zinc-100 w-20 text-right tabular-nums">
            {fmtNum(values[p.name] ?? p.init)}{p.unit ? ` ${p.unit}` : ''}
          </span>
        </label>
      ))}
      {(spec.params?.length ?? 0) > 0 && (
        <div className="flex justify-end pt-1">
          <button
            type="button"
            onClick={onShareState}
            title="현재 슬라이더 값을 채팅 입력창에 첨부 — LLM이 이 상태를 알도록"
            className="text-[10px] uppercase tracking-wider px-2 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100 transition"
          >
            📋 현재 상태 채팅에 첨부
          </button>
        </div>
      )}
    </div>
  );

  const readoutPanel = readoutValues.length > 0 ? (
    <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
      {readoutValues.map((r, i) => (
        <div key={i} className="bg-zinc-900/70 border border-zinc-800 rounded px-2 py-1">
          <div className="text-[10px] text-zinc-500 tracking-wider">
            <MathishText text={r.label} />
          </div>
          <div className="font-mono text-zinc-100 tabular-nums">
            {fmtNum(r.value, r.digits ?? 3)}{r.unit ? ` ${r.unit}` : ''}
          </div>
        </div>
      ))}
    </div>
  ) : null;

  // sticky panel rendering: skip broadcast through Interactive itself; the
  // wrapping wrapper handles broadcast at the parent (Graph.tsx) level.
  const wrapRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (interactive || noBroadcast) return;
    import('./Graph').then((m) => m.broadcastLatestGraph({
      kind: 'interactive', interactiveSpec: spec,
    }));
  }, [spec, interactive, noBroadcast]);

  // 외부 wrapper를 button으로 두면 내부의 슬라이더/공유 버튼이 nested button
  // HTML 위반을 만들고, 슬라이더 드래그가 모달 열기로 hijack됨. 그래서 외부는
  // 일반 div로 두고, 확대 버튼만 별도로 노출.
  return (
    <div ref={wrapRef}
         className="graph-host bg-zinc-950 border border-zinc-700/80 rounded-lg shadow-inner max-w-full relative"
         style={{ padding: '10px 12px' }}>
      {!hideCaption && spec.title && (
        <div className="text-zinc-300 mb-1 px-1 break-keep text-sm font-semibold pr-8">
          <MathishText text={spec.title} />
        </div>
      )}
      {!interactive && onOpen && (
        <button type="button" onClick={onOpen} title="확대"
                className="absolute top-1.5 right-1.5 w-6 h-6 inline-flex items-center justify-center rounded text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 text-sm">
          ⤢
        </button>
      )}
      {evalError && (
        <pre className="text-xs text-rose-300 bg-rose-500/10 border border-rose-500/30 p-2 rounded mb-2">
          {`expression error: ${evalError}`}
        </pre>
      )}
      {resolvedGeom && (
        <Geometry spec={resolvedGeom} width={width} height={height} hideCaption noBroadcast />
      )}
      {resolvedGeom3d && (
        <Geometry3D spec={resolvedGeom3d} width={width} height={height} hideCaption noBroadcast />
      )}
      {resolvedPlot && (
        <Graph kind="plot" spec={resolvedPlot} width={width} height={height ?? 260} hideCaption noBroadcast />
      )}
      {readoutPanel}
      {controls}
    </div>
  );
}

// 도형이 평가 후 NaN 좌표를 갖는지 검사 — 잘못된 표현식 또는 정의역 벗어남.
function isFinite(s: GeomShape): boolean {
  const check = (pt: [number, number] | unknown): boolean => {
    if (!Array.isArray(pt)) return true;
    return pt.every((v) => typeof v === 'number' && Number.isFinite(v));
  };
  switch (s.type) {
    case 'point': return check(s.at);
    case 'polygon': return s.vertices.every(check);
    case 'line': case 'segment': case 'vector': return check(s.from) && check(s.to);
    case 'circle': return check(s.center) && Number.isFinite(s.radius);
    case 'angle': return check(s.at) && check(s.from) && check(s.to);
    case 'text': return check(s.at);
  }
  return true;
}

function fmtNum(n: number, digits = 2): string {
  if (!Number.isFinite(n)) return '—';
  // Floating-point blow-up near asymptotes (e.g. tan 90°) → show ∞ symbol
  // instead of an unhelpful 17-digit integer.
  if (Math.abs(n) > 1e9) return n > 0 ? '∞' : '−∞';
  const s = Math.abs(n) >= 100 ? n.toFixed(0) : n.toFixed(digits);
  return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
}
