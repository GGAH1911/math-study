// 3D 스펙 검수 화면 — 드래그로 각도를 찾고 그 값을 스펙에 저장한다. **dev 전용.**
//
// ★왜: 좌표가 sympy 로 완벽해도 카메라가 나쁘면 도형이 안 보인다(2026-08-14: 접은 반원
//   평면의 법선과 시선이 거의 수직이라 반원이 선분 위에 겹쳐 사라졌다). 좋은 각도는 눈으로
//   돌려 찾는 게 제일 빠른데, 지금까지 찾은 값을 스펙에 옮겨 적을 길이 없었다.
import { useState } from 'react';
import Geometry3D from '../Geometry3D';
import type { Geom3DSpec } from '../../lib/geometry3d-core';

type Props = { stem: string; spec: Geom3DSpec; width?: number; height?: number };

export default function Fig3DReview({ stem, spec, width = 800, height = 620 }: Props) {
  const [cam, setCam] = useState<[number, number, number]>(spec.cameraPosition ?? [4, -4, 3]);
  const [saved, setSaved] = useState('');
  const [busy, setBusy] = useState(false);

  const save = async () => {
    setBusy(true); setSaved('');
    try {
      const r = await fetch('/api/dev/figure3d-camera', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stem, cameraPosition: cam }),
      });
      setSaved(r.ok ? `저장됨 [${cam.join(', ')}]` : `실패 ${r.status}: ${await r.text()}`);
    } catch (e) { setSaved(`실패 ${(e as Error).message}`); }
    setBusy(false);
  };

  return (
    <div>
      <Geometry3D spec={spec} width={width} height={height} onCamera={setCam} hideCaption noBroadcast />
      <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 8, fontSize: 12, color: '#a1a1aa' }}>
        <span>카메라 <code style={{ color: '#e4e4e7' }}>[{cam.join(', ')}]</code></span>
        <button type="button" onClick={save} disabled={busy}
          style={{ padding: '3px 10px', borderRadius: 6, border: '1px solid #3f3f46', color: '#e4e4e7', background: '#27272a' }}>
          {busy ? '저장 중…' : '이 각도를 스펙에 저장'}
        </button>
        {saved && <span style={{ color: saved.startsWith('저장됨') ? '#4ade80' : '#f87171' }}>{saved}</span>}
      </div>
      <p style={{ fontSize: 11, color: '#71717a', marginTop: 4 }}>
        드래그로 돌리면 값이 실시간으로 바뀝니다. 마음에 드는 각도에서 저장하세요 —
        좌표·검증 조건은 건드리지 않고 cameraPosition 만 기록합니다.
      </p>
    </div>
  );
}
