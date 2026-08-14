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

import '../styles/geometry3d.css';   // 인라인 <style> 에서 분리 — 위 파일 주석 참조
import { createContext, Suspense, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { OrbitControls, Grid, Html, Line, Edges, GizmoHelper, GizmoViewport } from '@react-three/drei';
import * as THREE from 'three';
import {
  type Geom3DShape, type Geom3DSpec,
  _math, _eval, triangulate, normalizeMathExprStr, coerceCoord, normalizePoint3, vertexKey,
} from '../lib/geometry3d-core';
import { collectPoints, CameraFit, CameraProbe } from './Geometry3DCamera';
// 타입은 여기서 계속 내보낸다 — Graph/Interactive/interactive-samples 의 import 경로를 지키려고.
export type { Geom3DShape, Geom3DSpec };

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


// 사각형 face → 두 삼각형. 5+각형은 fan triangulation.

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
  /** 검수 전용 — 카메라 위치 실시간 통지. 제품 화면에서는 안 넘긴다. */
  onCamera?: (p: [number, number, number]) => void;
  /** sticky 패널 자신은 mirror 안 함 (무한 루프 방지). */
  noBroadcast?: boolean;
};

export default function Geometry3D({ spec, width = 560, height = 380, onOpen, hideCaption, interactive = true, noBroadcast = false, onCamera }: Props) {
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
  // 카메라도 **늘린 뒤의** 점에 맞춰야 한다 — 원래 좌표로 맞추면 늘린 도형이 화면을 벗어난다.
  const dispScale = useMemo<[number, number, number]>(() => {
    const d = spec.displayScale;
    return Array.isArray(d) && d.length === 3 && d.every((v) => Number.isFinite(v) && v > 0)
      ? [d[0], d[1], d[2]] : [1, 1, 1];
  }, [spec.displayScale]);
  const cameraFitPoints = useMemo(
    () => collectPoints(spec.shapes).map((p) => p.clone().multiply(new THREE.Vector3(...dispScale))),
    [spec.shapes, dispScale]);
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
          {/* displayScale 은 **그릴 때만** 축을 늘린다 — 좌표는 검증된 값 그대로다. */}
          <group scale={dispScale}>
            {spec.shapes.map((s, i) => (
              <ShapeRouter key={i} s={s} idx={i} palette={PALETTE}
                           polyhedronVertexKeys={polyhedronVertexKeys} />
            ))}
          </group>
        </Suspense>
        {interactive && <OrbitControls makeDefault enableDamping dampingFactor={0.12} />}
        <CameraFit points={cameraFitPoints} shapeCount={spec.shapes.length} />
        {onCamera && <CameraProbe onChange={onCamera} />}
        </PortalCtx.Provider>
      </Canvas>
      {/* 축을 늘려 그렸으면 반드시 알린다 — 안 그러면 학생이 그림에서 길이를 잰다.
          교과서도 "그림은 실제와 다를 수 있음" 을 적는다. */}
      {dispScale.some((v) => v !== 1) && (
        <div className="absolute bottom-1 left-2 text-[10px] text-zinc-400/80 pointer-events-none">
          비율을 과장한 그림입니다 (길이·각도는 실제와 다름)
        </div>
      )}
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
    </div>
  );
}
