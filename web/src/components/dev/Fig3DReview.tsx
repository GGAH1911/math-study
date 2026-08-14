// 3D 스펙 검수 화면 — 각도와 **회전 중심**을 찾아 스펙에 저장한다. **dev 전용.**
//
// ★왜: 좌표가 sympy 로 완벽해도 카메라가 나쁘면 도형이 안 보인다(2026-08-14: 접은 반원
//   평면의 법선과 시선이 거의 수직이라 반원이 선분 위에 겹쳐 사라졌다).
// ★회전 중심이 따로 필요한 이유: 기본값(바운딩 박스 중심)으로 돌리면 **보고 싶은 부분이
//   화면 밖으로 밀려난다.** 접점 근처만 확대해 보려면 회전축이 거기 있어야 한다.
import { useState } from 'react';
import Geometry3D from '../Geometry3D';
import type { Geom3DSpec } from '../../lib/geometry3d-core';

type V3 = [number, number, number];
type Props = { stem: string; spec: Geom3DSpec; width?: number; height?: number };

const AXES = ['x', 'y', 'z'] as const;

export default function Fig3DReview({ stem, spec, width = 800, height = 620 }: Props) {
  const [pos, setPos] = useState<V3>(spec.cameraPosition ?? [4, -4, 3]);
  const [target, setTarget] = useState<V3>(spec.cameraTarget ?? [0, 0, 0]);
  // 버튼으로 회전 중심을 옮길 때만 spec 을 갈아끼워 리마운트한다(드래그 중엔 안 건드린다).
  const [pinned, setPinned] = useState<V3 | undefined>(spec.cameraTarget);
  const [saved, setSaved] = useState('');
  const [busy, setBusy] = useState(false);

  const nudge = (i: number, d: number) => {
    const next = [...target] as V3;
    next[i] = Math.round((next[i] + d) * 100) / 100;
    setTarget(next); setPinned(next);
  };

  const save = async () => {
    setBusy(true); setSaved('');
    try {
      const r = await fetch('/api/dev/figure3d-camera', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stem, cameraPosition: pos, cameraTarget: pinned ?? target }),
      });
      setSaved(r.ok ? '저장됨' : `실패 ${r.status}: ${await r.text()}`);
    } catch (e) { setSaved(`실패 ${(e as Error).message}`); }
    setBusy(false);
  };

  const box = { padding: '2px 7px', borderRadius: 5, border: '1px solid #3f3f46', color: '#e4e4e7', background: '#27272a', fontSize: 12 };

  return (
    <div>
      <Geometry3D
        key={pinned ? pinned.join(',') : 'auto'}
        spec={pinned ? { ...spec, cameraTarget: pinned } : spec}
        width={width} height={height}
        onCamera={(v) => { setPos(v.position); setTarget(v.target); }}
        hideCaption noBroadcast
      />
      <div style={{ fontSize: 12, color: '#a1a1aa', marginTop: 8, display: 'flex', flexDirection: 'column', gap: 6 }}>
        <div>시점 <code style={{ color: '#e4e4e7' }}>[{pos.join(', ')}]</code></div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <span>회전 중심 <code style={{ color: '#e4e4e7' }}>[{target.join(', ')}]</code></span>
          {AXES.map((ax, i) => (
            <span key={ax} style={{ display: 'inline-flex', gap: 3, alignItems: 'center' }}>
              <b style={{ color: '#71717a' }}>{ax}</b>
              <button type="button" style={box} onClick={() => nudge(i, -0.5)}>−</button>
              <button type="button" style={box} onClick={() => nudge(i, +0.5)}>+</button>
            </span>
          ))}
          <button type="button" style={box} onClick={() => { setPinned(undefined); setTarget([0, 0, 0]); }}>
            자동(도형 중심)으로
          </button>
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <button type="button" onClick={save} disabled={busy} style={{ ...box, padding: '4px 12px' }}>
            {busy ? '저장 중…' : '이 시점·회전 중심을 스펙에 저장'}
          </button>
          {saved && <span style={{ color: saved === '저장됨' ? '#4ade80' : '#f87171' }}>{saved}</span>}
        </div>
        <p style={{ fontSize: 11, color: '#71717a', margin: 0 }}>
          왼쪽 드래그 = 회전 · <b>오른쪽 드래그 = 회전 중심 이동</b> · 휠 = 확대.
          버튼으로도 중심을 0.5씩 옮길 수 있습니다.
          저장은 시점과 회전 중심만 기록하며 좌표·검증 조건은 건드리지 않습니다.
        </p>
      </div>
    </div>
  );
}
