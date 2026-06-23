// 3D geometry renderer — R3F Canvas + drei OrbitControls.
// LLM 이 ```geometry3d``` 블록으로 emit. 어떤 3D 도형이든 일반화된 primitive
// (polyhedron / parametricSurface / parametricCurve3d / plane) 로 표현.
//
// 사용:
//
//   ```geometry3d
//   { "shapes": [
//       {"type":"polyhedron",
//        "vertices":[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]],
//        "faces":[[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]],
//        "labels":["A","B","C","D","E","F","G","H"]}
//   ]}
//   ```

import { createContext, Suspense, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { OrbitControls, Grid, Html, Line, Edges, GizmoHelper, GizmoViewport } from '@react-three/drei';
import * as THREE from 'three';
import { create, all } from 'mathjs';
import katex from 'katex';
import { broadcastLatestGraph } from './Graph';

// 3D 라벨 — KaTeX 수식 렌더. 라벨에 \vec{a}·\alpha·^·_·\frac 등이 흔해(31/84 도식) plain text 면 깨진다.
//   3가지 경우: ① 전체가 $...$ 또는 순수 LaTeX(\vec·첨자·그리스) → 통째 KaTeX
//   ② 한글+중간 $수식$ 혼합('거리 $d(P,\pi)$') → $...$ 부분만 KaTeX, 나머지는 텍스트(HTML escape)
//   ③ 순수 텍스트(A·B·평면) → 그대로
const _MATHY = /\\[a-zA-Z]+|[_^{}]|[Ͱ-Ͽ]/;
function _esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function _kx(s: string): string {
  try { return katex.renderToString(s, { throwOnError: false, displayMode: false }); }
  catch { return _esc(s); }
}
function mathHtml(raw: string): { __html: string } | null {
  if (!raw) return null;
  const s = raw.trim();
  // ② 중간에 $...$ 가 낀 혼합 — 토큰별로 분리(escape 텍스트 + KaTeX)
  if (/\$[^$]+\$/.test(s)) {
    const parts = s.split(/(\$[^$]+\$)/);
    const html = parts.map((p) => {
      const m = /^\$([^$]+)\$$/.exec(p);
      return m ? _kx(m[1]) : _esc(p);
    }).join('');
    return { __html: html };
  }
  // ① 전체가 LaTeX (델리미터 없이 \vec·첨자·그리스문자)
  if (_MATHY.test(s)) return { __html: _kx(s) };
  // ③ 순수 텍스트
  return null;
}
// geom3d-label 내용 — 수식/혼합이면 KaTeX HTML, 순수텍스트면 그대로.
function Label3D({ text, color }: { text: string; color?: string }) {
  const html = mathHtml(text);
  return html
    ? <div className="geom3d-label" style={color ? { color } : undefined} dangerouslySetInnerHTML={html} />
    : <div className="geom3d-label" style={color ? { color } : undefined}>{text}</div>;
}

const _math = create(all);
function _eval(s: string | number): number {
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

// 사각형 face → 두 삼각형. 5+각형은 fan triangulation.
function triangulate(faceIndices: number[]): number[] {
  if (faceIndices.length === 3) return faceIndices;
  const out: number[] = [];
  for (let i = 1; i < faceIndices.length - 1; i++) {
    out.push(faceIndices[0], faceIndices[i], faceIndices[i + 1]);
  }
  return out;
}

// 좌표 좌표 정규화 — LLM 이 '3*sqrt(3)' 같은 raw 수학식 string 박은 경우
// 자동 mathjs evaluate. number, evaluable string 모두 number 로. invalid 면 null.
function normalizeMathExprStr(s: string): string {
  return s.replace(/√/g, 'sqrt').replace(/π/g, 'pi').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
}
function coerceCoord(v: unknown): number | null {
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
function normalizePoint3(p: unknown): [number, number, number] | null {
  if (!Array.isArray(p) || p.length < 3) return null;
  const x = coerceCoord(p[0]);
  const y = coerceCoord(p[1]);
  const z = coerceCoord(p[2]);
  if (x === null || y === null || z === null) return null;
  return [x, y, z];
}
function vertexKey(p: [number, number, number]): string {
  return `${p[0].toFixed(4)},${p[1].toFixed(4)},${p[2].toFixed(4)}`;
}

// Html 라벨이 박힐 DOM portal target — Geometry3D wrapper 안으로 강제.
// overflow:hidden 으로 자기 박스 밖 안 흘러나감 (sticky 영역 침범 차단).
const PortalCtx = createContext<{ current: HTMLDivElement | null } | null>(null);
function useHtmlPortal(): HTMLElement | undefined {
  const ref = useContext(PortalCtx);
  return ref?.current ?? undefined;
}

function PolyhedronShape({ s, defaultColor }: { s: Extract<Geom3DShape, { type: 'polyhedron' }>; defaultColor: string }) {
  const portal = useHtmlPortal();
  const normalizedVertices = useMemo(() => {
    return s.vertices.map((v) => normalizePoint3(v)).filter((v): v is [number, number, number] => v !== null);
  }, [s.vertices]);
  const geometry = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const positions: number[] = [];
    const indices: number[] = [];
    for (const v of normalizedVertices) positions.push(...v);
    for (const face of s.faces) {
      const tri = triangulate(face);
      for (const idx of tri) indices.push(idx);
    }
    g.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [normalizedVertices, s.faces]);
  const fill = s.fill ?? defaultColor;
  const stroke = s.stroke ?? '#fafafa';
  const opacity = s.fillOpacity ?? 0.28;
  return (
    <>
      <mesh geometry={geometry}>
        <meshStandardMaterial
          color={fill}
          transparent
          opacity={opacity}
          side={THREE.DoubleSide}
        />
        <Edges color={stroke} threshold={1} />
      </mesh>
      {s.labels?.map((label, i) => {
        if (!label || !normalizedVertices[i]) return null;
        const [x, y, z] = normalizedVertices[i];
        return (
          <Html key={`pl${i}`} position={[x, y, z]} center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}>
            <Label3D text={label} />
          </Html>
        );
      })}
    </>
  );
}

function ParametricSurfaceShape({ s, defaultColor }: { s: Extract<Geom3DShape, { type: 'parametricSurface' }>; defaultColor: string }) {
  const geometry = useMemo(() => {
    const u0 = _eval(s.uRange[0]), u1 = _eval(s.uRange[1]);
    const v0 = _eval(s.vRange[0]), v1 = _eval(s.vRange[1]);
    if (!Number.isFinite(u0) || !Number.isFinite(u1) || !Number.isFinite(v0) || !Number.isFinite(v1)) {
      return new THREE.BufferGeometry();
    }
    const nu = Math.max(4, Math.min(s.uSamples ?? 32, 128));
    const nv = Math.max(4, Math.min(s.vSamples ?? 32, 128));
    let xN, yN, zN;
    try {
      xN = _math.parse(s.x).compile();
      yN = _math.parse(s.y).compile();
      zN = _math.parse(s.z).compile();
    } catch {
      return new THREE.BufferGeometry();
    }
    const positions: number[] = [];
    for (let i = 0; i <= nu; i++) {
      for (let j = 0; j <= nv; j++) {
        const u = u0 + ((u1 - u0) * i) / nu;
        const v = v0 + ((v1 - v0) * j) / nv;
        try {
          const xv = xN.evaluate({ u, v });
          const yv = yN.evaluate({ u, v });
          const zv = zN.evaluate({ u, v });
          positions.push(
            Number.isFinite(xv) ? xv : 0,
            Number.isFinite(yv) ? yv : 0,
            Number.isFinite(zv) ? zv : 0,
          );
        } catch {
          positions.push(0, 0, 0);
        }
      }
    }
    const indices: number[] = [];
    for (let i = 0; i < nu; i++) {
      for (let j = 0; j < nv; j++) {
        const a = i * (nv + 1) + j;
        const b = a + 1;
        const c = a + (nv + 1);
        const d = c + 1;
        indices.push(a, c, b, b, c, d);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [s.x, s.y, s.z, s.uRange, s.vRange, s.uSamples, s.vSamples]);
  const color = s.color ?? defaultColor;
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial
        color={color}
        transparent
        opacity={s.opacity ?? 0.15}
        side={THREE.DoubleSide}
        wireframe={s.wireframe ?? false}
        depthWrite={false}
      />
    </mesh>
  );
}

function ParametricCurveShape({ s, defaultColor }: { s: Extract<Geom3DShape, { type: 'parametricCurve3d' }>; defaultColor: string }) {
  const points = useMemo(() => {
    const t0 = _eval(s.tRange[0]), t1 = _eval(s.tRange[1]);
    if (!Number.isFinite(t0) || !Number.isFinite(t1) || t1 <= t0) return [];
    const n = Math.max(8, Math.min(s.samples ?? 200, 2000));
    let xN, yN, zN;
    try {
      xN = _math.parse(s.x).compile();
      yN = _math.parse(s.y).compile();
      zN = _math.parse(s.z).compile();
    } catch { return []; }
    const out: Array<[number, number, number]> = [];
    for (let i = 0; i <= n; i++) {
      const t = t0 + ((t1 - t0) * i) / n;
      try {
        const xv = xN.evaluate({ t });
        const yv = yN.evaluate({ t });
        const zv = zN.evaluate({ t });
        if (Number.isFinite(xv) && Number.isFinite(yv) && Number.isFinite(zv)) {
          out.push([xv, yv, zv]);
        }
      } catch { /* skip */ }
    }
    return out;
  }, [s.x, s.y, s.z, s.tRange, s.samples]);
  if (points.length < 2) return null;
  return <Line points={points} color={s.color ?? defaultColor} lineWidth={s.strokeWidth ?? 2} />;
}

function PlaneShape({ s, defaultColor, portal }: {
  s: Extract<Geom3DShape, { type: 'plane' }>;
  defaultColor: string;
  portal?: HTMLElement | null;
}) {
  const origin = normalizePoint3(s.origin);
  const normal = normalizePoint3(s.normal);
  const sz = coerceCoord(s.size) ?? 4;
  // size cap — 너무 큰 plane 이 다른 도형 가리는 거 방지. max 10.
  const size = Math.min(Math.max(sz, 0.5), 10);
  const { quat } = useMemo(() => {
    if (!normal) return { quat: new THREE.Quaternion() };
    const n = new THREE.Vector3(...normal).normalize();
    const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), n);
    return { quat: q };
  }, [normal]);
  if (!origin || !normal) {
    if (typeof window !== 'undefined') console.warn('[Geometry3D] plane origin/normal invalid — ignored');
    return null;
  }
  return (
    <>
      <mesh position={origin} quaternion={quat}>
        <planeGeometry args={[size, size]} />
        <meshStandardMaterial
          color={s.color ?? defaultColor}
          transparent
          opacity={s.opacity ?? 0.12}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
      {s.label && (
        <Html position={origin} center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}>
          <Label3D text={s.label} />
        </Html>
      )}
    </>
  );
}

function ShapeRouter({ s, idx, palette, polyhedronVertexKeys }: {
  s: Geom3DShape; idx: number; palette: string[];
  polyhedronVertexKeys: Set<string>;
}) {
  const dc = palette[idx % palette.length];
  const portal = useHtmlPortal();
  // polyhedron vertex 와 좌표가 같은 point3d 는 자동 무시 — labels 중복 방지.
  if (s.type === 'point3d') {
    const at = normalizePoint3(s.at);
    if (!at) {
      if (typeof window !== 'undefined') {
        console.warn(`[Geometry3D] point3d "at" invalid (expected [x,y,z]) — ignored`, s.at);
      }
      return null;
    }
    const key = vertexKey(at);
    if (polyhedronVertexKeys.has(key)) {
      if (typeof window !== 'undefined') {
        console.warn(`[Geometry3D] duplicate point3d at polyhedron vertex ignored (label="${s.label ?? ''}")`);
      }
      return null;
    }
  }
  switch (s.type) {
    case 'point3d': {
      const at = normalizePoint3(s.at);
      if (!at) return null;
      const [x, y, z] = at;
      // size 옵션 무시 — 항상 0.06 (정육면체 한 변 2 기준 3%). LLM 이 박은 값 무시.
      const radius = 0.06;
      return (
        <>
          <mesh position={[x, y, z]}>
            <sphereGeometry args={[radius, 16, 16]} />
            <meshStandardMaterial color={s.color ?? '#f472b6'} />
          </mesh>
          {s.label && (
            <Html position={[x, y, z]} center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}>
              <Label3D text={s.label} />
            </Html>
          )}
        </>
      );
    }
    case 'segment3d': {
      const from = normalizePoint3(s.from);
      const to = normalizePoint3(s.to);
      if (!from || !to) {
        if (typeof window !== 'undefined') console.warn('[Geometry3D] segment3d from/to invalid — ignored', s.from, s.to);
        return null;
      }
      return (
        <>
          <Line
            points={[from, to]}
            color={s.color ?? dc}
            lineWidth={2}
            dashed={s.dashed ?? false}
            dashSize={s.dashed ? 0.2 : undefined}
            gapSize={s.dashed ? 0.1 : undefined}
          />
          {s.label && (
            <Html
              position={[(from[0] + to[0]) / 2, (from[1] + to[1]) / 2, (from[2] + to[2]) / 2]}
              center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}
            >
              <Label3D text={s.label} />
            </Html>
          )}
        </>
      );
    }
    case 'polyhedron':
      // vertices 가 비정상적으로 많으면 (sphere 격자 우회) 거부.
      // 정육면체 8, 정사면체 4, 정팔면체 6, 정이십면체 12, 정십이면체 20.
      // 24 초과는 sphere 흉내 의심.
      if (s.vertices.length > 24) {
        if (typeof window !== 'undefined') {
          console.warn(`[Geometry3D] polyhedron ${s.vertices.length} verts rejected (sphere mimic)`);
        }
        return null;
      }
      if (!s.vertices.every((v) => normalizePoint3(v) !== null)) {
        if (typeof window !== 'undefined') {
          console.warn('[Geometry3D] polyhedron has invalid vertex — ignored');
        }
        return null;
      }
      return <PolyhedronShape s={s} defaultColor={dc} />;
    case 'parametricSurface':
      return <ParametricSurfaceShape s={s} defaultColor={dc} />;
    case 'parametricCurve3d':
      return <ParametricCurveShape s={s} defaultColor={dc} />;
    case 'sphere': {
      const center = normalizePoint3(s.center);
      const radius = coerceCoord(s.radius);
      if (!center || radius === null || radius <= 0) {
        if (typeof window !== 'undefined') console.warn('[Geometry3D] sphere invalid center/radius — ignored', s.center, s.radius);
        return null;
      }
      const segs = 32;
      return (
        <>
          <mesh position={center}>
            <sphereGeometry args={[radius, segs, Math.round(segs * 0.7)]} />
            <meshStandardMaterial color={s.color ?? dc} transparent
              opacity={s.opacity ?? 0.18} wireframe={s.wireframe ?? false}
              side={THREE.DoubleSide} depthWrite={false} />
          </mesh>
          {s.label && (
            <Html position={center} center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}>
              <Label3D text={s.label} />
            </Html>
          )}
        </>
      );
    }
    case 'plane':
      return <PlaneShape s={s} defaultColor={dc} portal={portal} />;
    case 'text3d': {
      const at = normalizePoint3(s.at);
      if (!at) return null;
      return (
        <Html position={at} center portal={portal ? { current: portal } : undefined} style={{ pointerEvents: 'none' }}>
          <Label3D text={s.text} color={s.color} />
        </Html>
      );
    }
  }
}

// 도형 vertex 들을 카메라 projection 으로 NDC 변환 → 화면 bbox 가
// viewport 의 TARGET 분율 채우도록 distance iterate 조정. drei Bounds 의
// axis-aligned bbox 한계 (isometric viewing 부정확) 우회.
function collectPoints(shapes: Geom3DShape[]): THREE.Vector3[] {
  const out: THREE.Vector3[] = [];
  const pushIfValid = (p: unknown) => {
    const n = normalizePoint3(p);
    if (n) out.push(new THREE.Vector3(...n));
  };
  for (const s of shapes) {
    switch (s.type) {
      case 'point3d': pushIfValid(s.at); break;
      case 'segment3d':
        pushIfValid(s.from);
        pushIfValid(s.to);
        break;
      case 'polyhedron':
        for (const v of s.vertices) pushIfValid(v);
        break;
      case 'text3d': pushIfValid(s.at); break;
      case 'sphere': {
        const center = normalizePoint3(s.center);
        const r = coerceCoord(s.radius);
        if (!center || r === null || r <= 0) break;
        const [cx, cy, cz] = center;
        // sphere bbox 6 점
        out.push(new THREE.Vector3(cx + r, cy, cz));
        out.push(new THREE.Vector3(cx - r, cy, cz));
        out.push(new THREE.Vector3(cx, cy + r, cz));
        out.push(new THREE.Vector3(cx, cy - r, cz));
        out.push(new THREE.Vector3(cx, cy, cz + r));
        out.push(new THREE.Vector3(cx, cy, cz - r));
        break;
      }
      case 'parametricCurve3d': {
        const t0 = _eval(s.tRange[0]), t1 = _eval(s.tRange[1]);
        if (!Number.isFinite(t0) || !Number.isFinite(t1)) break;
        try {
          const xN = _math.parse(s.x).compile();
          const yN = _math.parse(s.y).compile();
          const zN = _math.parse(s.z).compile();
          const n = Math.min(s.samples ?? 60, 200);
          for (let i = 0; i <= n; i++) {
            const t = t0 + ((t1 - t0) * i) / n;
            const xv = xN.evaluate({ t }) as number;
            const yv = yN.evaluate({ t }) as number;
            const zv = zN.evaluate({ t }) as number;
            if (Number.isFinite(xv) && Number.isFinite(yv) && Number.isFinite(zv)) {
              out.push(new THREE.Vector3(xv, yv, zv));
            }
          }
        } catch { /* skip */ }
        break;
      }
      case 'plane': {
        const origin = normalizePoint3(s.origin);
        const sz = Math.min(Math.max(coerceCoord(s.size) ?? 4, 0.5), 10);
        if (!origin) break;
        const half = sz / 2;
        // plane 의 4 corner 대략값 — normal 따라 회전하지만 bbox 추정엔 origin±half 6 방향 충분
        out.push(new THREE.Vector3(origin[0] + half, origin[1] + half, origin[2]));
        out.push(new THREE.Vector3(origin[0] - half, origin[1] - half, origin[2]));
        out.push(new THREE.Vector3(origin[0] + half, origin[1] - half, origin[2]));
        out.push(new THREE.Vector3(origin[0] - half, origin[1] + half, origin[2]));
        break;
      }
      case 'parametricSurface': {
        // 성긴 격자(5×5) 로 surface 위 점 일부를 bbox 에 포함 — surface 하나만
        // 있는 spec 도 CameraFit 이 동작하도록(원점에서 멀거나 큰 곡면 대응).
        const u0 = _eval(s.uRange[0]), u1 = _eval(s.uRange[1]);
        const v0 = _eval(s.vRange[0]), v1 = _eval(s.vRange[1]);
        if (!Number.isFinite(u0) || !Number.isFinite(u1) || !Number.isFinite(v0) || !Number.isFinite(v1)) break;
        try {
          const xN = _math.parse(s.x).compile();
          const yN = _math.parse(s.y).compile();
          const zN = _math.parse(s.z).compile();
          const m = 4; // 4 구간 → 5×5 = 25 점
          for (let i = 0; i <= m; i++) {
            for (let j = 0; j <= m; j++) {
              const u = u0 + ((u1 - u0) * i) / m;
              const v = v0 + ((v1 - v0) * j) / m;
              const xv = xN.evaluate({ u, v }) as number;
              const yv = yN.evaluate({ u, v }) as number;
              const zv = zN.evaluate({ u, v }) as number;
              if (Number.isFinite(xv) && Number.isFinite(yv) && Number.isFinite(zv)) {
                out.push(new THREE.Vector3(xv, yv, zv));
              }
            }
          }
        } catch { /* skip */ }
        break;
      }
    }
  }
  return out;
}

function CameraFit({ points, shapeCount }: { points: THREE.Vector3[]; shapeCount: number }) {
  const { camera, controls } = useThree();
  const lastFitCount = useRef(-1);
  useEffect(() => {
    if (points.length === 0) return;
    // slider 변경 (shape 개수 동일) 은 fit 스킵 — 사용자 회전 유지.
    // 첫 mount + 도형 추가/삭제 시만 fit.
    if (lastFitCount.current === shapeCount) return;
    lastFitCount.current = shapeCount;
    const cam = camera as THREE.PerspectiveCamera;
    cam.up.set(0, 0, 1); // Z-up 강제
    const box = new THREE.Box3();
    for (const p of points) box.expandByPoint(p);
    const center = new THREE.Vector3();
    box.getCenter(center);
    // 카메라 viewing direction 유지 (현재 position - center). 첫 mount 시
    // 카메라가 (4,-4,3) 근처라 isometric direction.
    const dir = cam.position.clone().sub(center);
    if (dir.length() < 0.01) dir.set(1, -1, 0.7);
    dir.normalize();

    const TARGET = 0.85; // NDC max abs — 85% 채움 (15% 여백)
    let d = Math.max(box.getSize(new THREE.Vector3()).length() * 1.5, 2);
    for (let iter = 0; iter < 5; iter++) {
      cam.position.copy(center).addScaledVector(dir, d);
      cam.lookAt(center);
      cam.updateMatrixWorld();
      cam.updateProjectionMatrix();
      let maxAbs = 0;
      for (const p of points) {
        const v = p.clone().project(cam);
        maxAbs = Math.max(maxAbs, Math.abs(v.x), Math.abs(v.y));
      }
      if (maxAbs < 1e-6) break;
      const scale = maxAbs / TARGET;
      if (Math.abs(scale - 1) < 0.02) break;
      d *= scale;
    }
    cam.position.copy(center).addScaledVector(dir, d);
    cam.lookAt(center);
    cam.updateProjectionMatrix();
    // OrbitControls 의 회전축도 center 로
    const c = controls as unknown as { target?: THREE.Vector3; update?: () => void } | null;
    if (c?.target) { c.target.copy(center); c.update?.(); }
  }, [points, shapeCount, camera, controls]);
  return null;
}

const PALETTE = ['#60a5fa', '#a3e635', '#f472b6', '#fbbf24', '#34d399', '#c084fc'];

type Props = {
  spec: Geom3DSpec;
  width?: number;
  /** number(px) 또는 CSS string ('70vh' 같이). */
  height?: number | string;
  onOpen?: () => void;
  hideCaption?: boolean;
  /** 회전·줌 인터랙션 허용. 채팅 inline 미리보기는 false (정적), 모달은 true. */
  interactive?: boolean;
  /** sticky 패널 자신은 mirror 안 함 (무한 루프 방지). */
  noBroadcast?: boolean;
};

export default function Geometry3D({ spec, width = 560, height = 380, onOpen, hideCaption, interactive = true, noBroadcast = false }: Props) {
  // R3F Canvas 는 SSR 호환 X — SSR pass 에선 placeholder 만 render, hydration 후 실제 mount.
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);
  const [hoverOpen, setHoverOpen] = useState(false);
  const portalRef = useRef<HTMLDivElement | null>(null);

  // mirror to sticky panel
  useEffect(() => {
    if (noBroadcast) return;
    if (spec.shapes.length === 0) return;
    broadcastLatestGraph({ kind: 'geom3d', geom3dSpec: spec });
  }, [spec, noBroadcast]);
  const cameraFitPoints = useMemo(() => collectPoints(spec.shapes), [spec.shapes]);
  const polyhedronVertexKeys = useMemo(() => {
    const keys = new Set<string>();
    for (const s of spec.shapes) {
      if (s.type === 'polyhedron') {
        for (const v of s.vertices) {
          const n = normalizePoint3(v);
          if (n) keys.add(vertexKey(n));
        }
      }
    }
    return keys;
  }, [spec.shapes]);
  // Z-up: 카메라 기본 위치를 +Y forward / +Z up 로
  const camPos = spec.cameraPosition ?? [4, -4, 3];
  const showAxes = spec.axes !== false;

  if (!mounted) {
    return (
      <div className="geom3d-wrap" style={{
        position: 'relative', width: '100%', height,
        overflow: 'hidden', borderRadius: 8, background: '#0c0c0e',
      }} />
    );
  }

  return (
    <div className="geom3d-wrap" style={{
      position: 'relative',
      width: '100%',
      height,
      overflow: 'hidden',
      borderRadius: 8,
    }}>
      {/* drei Html 라벨이 박힐 portal target — wrapper 안에 묶어 overflow:hidden 으로 잘림 */}
      <div ref={portalRef} style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        overflow: 'hidden', zIndex: 2,
      }} />
      <Canvas
        camera={{ position: camPos, up: [0, 0, 1], fov: 50, near: 0.1, far: 1000 }}
        style={{ background: spec.bgColor ?? '#0c0c0e', borderRadius: 8 }}
        gl={{ antialias: true, alpha: false, preserveDrawingBuffer: true }}
      >
        <PortalCtx.Provider value={portalRef}>
        <ambientLight intensity={0.55} />
        <directionalLight position={[5, -5, 8]} intensity={0.9} />
        <directionalLight position={[-5, 5, -5]} intensity={0.25} />
        {showAxes && (
          <>
            {/* Z-up: drei Grid 기본은 XZ 평면이므로 XY 평면이 되게 X 축 회전 */}
            <Grid
              args={[spec.gridSize ?? 10, spec.gridSize ?? 10]}
              cellColor="#3f3f46"
              sectionColor="#52525b"
              fadeDistance={20}
              fadeStrength={1}
              infiniteGrid
              rotation={[Math.PI / 2, 0, 0]}
            />
            {/* 축 표시는 화면 우측 하단 코너 gizmo 로 — 도형과 분리되어 vertex 라벨과 안 겹침 */}
            <GizmoHelper alignment="bottom-right" margin={[60, 60]}>
              <GizmoViewport
                axisColors={['#f87171', '#4ade80', '#60a5fa']}
                labelColor="#fafafa"
              />
            </GizmoHelper>
          </>
        )}
        <Suspense fallback={null}>
          {spec.shapes.map((s, i) => (
            <ShapeRouter key={i} s={s} idx={i} palette={PALETTE}
                         polyhedronVertexKeys={polyhedronVertexKeys} />
          ))}
        </Suspense>
        {interactive && <OrbitControls makeDefault enableDamping dampingFactor={0.12} />}
        <CameraFit points={cameraFitPoints} shapeCount={spec.shapes.length} />
        </PortalCtx.Provider>
      </Canvas>
      {onOpen && (
        <button
          type="button"
          onClick={onOpen}
          onMouseEnter={() => setHoverOpen(true)}
          onMouseLeave={() => setHoverOpen(false)}
          className="absolute top-2 right-2 px-2 py-1 text-[10px] rounded bg-zinc-900/70 border border-zinc-700 text-zinc-300 hover:bg-zinc-800"
        >
          {hoverOpen ? '확대' : '⛶'}
        </button>
      )}
      {!hideCaption && spec.title && (
        <div className="text-[11px] text-zinc-400 mt-1 px-1">{spec.title}</div>
      )}
      <style>{`
        .geom3d-axis-label {
          font-size: 13px;
          font-weight: 600;
          font-family: var(--font-mono, monospace);
          user-select: none;
          text-shadow: 0 0 4px rgba(0,0,0,0.8);
        }
        .geom3d-label {
          color: #fafafa;
          background: rgba(20, 20, 23, 0.78);
          border: 1px solid #3f3f46;
          padding: 1px 5px;
          border-radius: 3px;
          font-size: 13px;
          line-height: 16px;
          font-family: var(--font-mono, monospace);
          white-space: nowrap;
          user-select: none;
        }
        /* KaTeX 수식 라벨 — 색 상속(흰색) + 크기 보장(작은 박스에 안 뭉개지게) */
        .geom3d-label .katex { font-size: 1em; color: inherit; }
      `}</style>
    </div>
  );
}
