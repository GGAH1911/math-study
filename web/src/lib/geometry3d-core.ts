// 3D 도형 스펙의 **타입과 순수 헬퍼** — Geometry3D.tsx 에서 갈라져 나왔다(2026-08-14).
//
// ★가른 자리: 여기 있는 것은 React 도 three.js 도 모르는 순수 계산이다(수식 평가·좌표 정규화·
//   면 삼각분할). 렌더링 컴포넌트와 수명이 다르고, 카메라 모듈도 이걸 써야 해서
//   양쪽이 서로를 import 하면 순환이 된다. 그래서 아래층으로 내렸다.
import { create, all } from 'mathjs';

export const _math = create(all);
export function _eval(s: string | number): number {
  if (typeof s === 'number') return s;
  try { return _math.evaluate(s); } catch { return NaN; }
}

export type Geom3DShape =
  | { type: 'point3d'; at: [number, number, number]; label?: string; color?: string; size?: number; labelDir?: string }
  | { type: 'segment3d'; from: [number, number, number]; to: [number, number, number]; color?: string; dashed?: boolean; label?: string }
  | { type: 'polyhedron';
      vertices: Array<[number, number, number]>;
      faces: number[][];
      labels?: string[];
      fill?: string; fillOpacity?: number; stroke?: string; strokeWidth?: number }
  | { type: 'parametricSurface';
      x: string; y: string; z: string;
      uRange: [number | string, number | string]; vRange: [number | string, number | string];
      uSamples?: number; vSamples?: number;
      color?: string; opacity?: number; wireframe?: boolean; label?: string }
  | { type: 'parametricCurve3d';
      x: string; y: string; z: string;
      tRange: [number | string, number | string]; samples?: number;
      color?: string; strokeWidth?: number; label?: string }
  | { type: 'sphere';
      center: [number, number, number]; radius: number;
      color?: string; opacity?: number; wireframe?: boolean; label?: string }
  | { type: 'plane';
      origin: [number, number, number];
      normal: [number, number, number];
      size?: number; color?: string; opacity?: number; label?: string }
  | { type: 'text3d'; at: [number, number, number]; text: string; color?: string };

export type Geom3DSpec = {
  shapes: Geom3DShape[];
  cameraPosition?: [number, number, number];
  axes?: boolean;
  gridSize?: number;
  bgColor?: string;
  title?: string;
};

export function triangulate(faceIndices: number[]): number[] {
  if (faceIndices.length === 3) return faceIndices;
  const out: number[] = [];
  for (let i = 1; i < faceIndices.length - 1; i++) {
    out.push(faceIndices[0], faceIndices[i], faceIndices[i + 1]);
  }
  return out;
}

// 좌표 좌표 정규화 — LLM 이 '3*sqrt(3)' 같은 raw 수학식 string 박은 경우
// 자동 mathjs evaluate. number, evaluable string 모두 number 로. invalid 면 null.
export function normalizeMathExprStr(s: string): string {
  return s.replace(/√/g, 'sqrt').replace(/π/g, 'pi').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
}
export function coerceCoord(v: unknown): number | null {
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  if (typeof v === 'string') {
    const expr = normalizeMathExprStr(v.startsWith('=') ? v.slice(1) : v);
    try {
      const r = _math.evaluate(expr);
      if (typeof r === 'number' && Number.isFinite(r)) return r;
    } catch { /* fall through */ }
    return null;
  }
  return null;
}
export function normalizePoint3(p: unknown): [number, number, number] | null {
  if (!Array.isArray(p) || p.length < 3) return null;
  const x = coerceCoord(p[0]);
  const y = coerceCoord(p[1]);
  const z = coerceCoord(p[2]);
  if (x === null || y === null || z === null) return null;
  return [x, y, z];
}
export function vertexKey(p: [number, number, number]): string {
  return `${p[0].toFixed(4)},${p[1].toFixed(4)},${p[2].toFixed(4)}`;
}
