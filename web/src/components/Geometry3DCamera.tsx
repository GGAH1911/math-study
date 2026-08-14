// 3D 도형의 **바운딩 박스 수집 + 카메라 맞춤** — Geometry3D.tsx 에서 갈라져 나왔다(2026-08-14).
//
// ★왜 따로: "무엇을 그리는가" 와 "어디서 보는가" 는 다른 문제다. 카메라가 잘못 잡히면
//   좌표가 완벽해도 도형이 안 보인다(2026-08-14: 접은 반원 평면의 법선과 시선이 거의
//   수직이라 반원이 선분 위에 겹쳐 사라졌다). 이 판정은 여기 모아 둔다.
import { useEffect, useRef } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { type Geom3DShape, _eval, _math, coerceCoord, normalizePoint3 } from '../lib/geometry3d-core';

export function collectPoints(shapes: Geom3DShape[]): THREE.Vector3[] {
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

export function CameraFit({ points, shapeCount }: { points: THREE.Vector3[]; shapeCount: number }) {
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
