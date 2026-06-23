// 화면에 보일 때만 Geometry3D(R3F WebGL Canvas)를 마운트하는 lazy 래퍼.
// ★WebGL 컨텍스트는 브라우저당 동시 ~8-16개 한계 → 갤러리에 많은 3D를 한 번에 마운트하면
//   초과분이 빈화면이 된다. IntersectionObserver 로 viewport 진입 시 마운트, 멀어지면 언마운트해
//   동시 살아있는 컨텍스트 수를 화면에 보이는 것 + 약간으로 제한한다.
import { useEffect, useRef, useState } from 'react';
import Geometry3D, { type Geom3DSpec } from './Geometry3D.tsx';

export default function Lazy3D({ spec, width = 340, height = 290 }: { spec: Geom3DSpec; width?: number; height?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const [show, setShow] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => { for (const e of entries) setShow(e.isIntersecting); },
      { rootMargin: '200px' },   // 화면 200px 앞에서 미리 마운트(스크롤 매끄럽게)
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div ref={ref} style={{ width, height, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {show
        ? <Geometry3D spec={spec} width={width} height={height} hideCaption noBroadcast />
        : <span style={{ color: '#52525b', fontSize: 12 }}>스크롤하면 3D 로드…</span>}
    </div>
  );
}
