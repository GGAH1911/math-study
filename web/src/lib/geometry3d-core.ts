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
  /**
   * **표시 전용** 축 배율 [sx, sy, sz]. 좌표는 그대로 두고 그릴 때만 늘린다.
   *
   * ★왜: 기출 도판은 실제 비율이 아니다 — 일부러 과장해 그린다. 예로 2020 9월모평 가형 14 는
   *   밑면 폭이 0.59 인데 단면 한 변이 7.69 라, 실제 좌표로는 **어떤 카메라를 잡아도** 세 단면이
   *   겹쳐 바늘처럼 보인다. 원본은 x 를 크게 늘려 그렸다.
   * ★좌표 자체를 늘리지 않는 이유: 그 좌표는 sympy 로 검증된 값이다. 늘리면 검증이 무의미해진다.
   * ⚠️ 축을 따로 늘리면 **각도와 길이가 눈으로는 거짓말을 한다** — 직각이 직각으로 안 보이고
   *   구는 타원체가 된다. 그래서 구·원이 있는 스펙에는 쓰지 않고, 쓴 그림에는 캡션으로 알린다.
   */
  displayScale?: [number, number, number];
  /**
   * 회전 중심(OrbitControls 의 target). 안 주면 도형 바운딩 박스의 중심.
   *
   * ★왜 필요한가: 기본값(중심)으로 돌리면 **보고 싶은 부분이 화면 밖으로 밀려난다.**
   *   예로 접은 반원의 접점 근처만 확대해 보려면 회전축이 거기 있어야 한다.
   */
  cameraTarget?: [number, number, number];
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
