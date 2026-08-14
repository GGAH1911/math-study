#!/usr/bin/env python3
"""3D 스펙의 **가독성 하한**을 적용한다.

★왜: 좌표가 정확해도 안 보이면 학생에겐 틀린 그림이다. 2026-08-14 검수에서 곡면·구·평면의
  opacity 중앙값이 0.14 였고(96개 중 54개가 0.2 미만), 검은 배경에서 면이 사실상 사라져
  "접어 올린 반원"이 호만 그린 것처럼 보였다 — 실제로 나도 그렇게 오독했다.

하한만 올린다. 이미 진한 것은 건드리지 않는다(구 안쪽이 보여야 하는 경우가 있다).
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/figures-3d'

FLOOR_FILL = 0.18     # polyhedron 면
FLOOR_OPACITY = 0.22  # parametricSurface / plane
FLOOR_SPHERE = 0.15   # 구는 안이 비쳐야 해서 조금 낮게
FLOOR_STROKE = 2      # 검은 배경의 1px 선은 거의 안 보인다


def main() -> int:
    apply = '--apply' in sys.argv
    n_files = n_edits = 0
    for f in sorted(DIR.glob('*.json')):
        e = json.loads(f.read_text(encoding='utf-8'))
        edits = []
        for s in e['spec']['shapes']:
            t = s['type']
            if t == 'polyhedron':
                if s.get('fillOpacity', 1.0) < FLOOR_FILL:
                    edits.append((t, 'fillOpacity', s.get('fillOpacity'), FLOOR_FILL))
                    if apply: s['fillOpacity'] = FLOOR_FILL
                if s.get('strokeWidth', 1) < FLOOR_STROKE:
                    edits.append((t, 'strokeWidth', s.get('strokeWidth'), FLOOR_STROKE))
                    if apply: s['strokeWidth'] = FLOOR_STROKE
            elif t == 'sphere':
                if s.get('opacity', 1.0) < FLOOR_SPHERE:
                    edits.append((t, 'opacity', s.get('opacity'), FLOOR_SPHERE))
                    if apply: s['opacity'] = FLOOR_SPHERE
            elif t in ('parametricSurface', 'plane'):
                if s.get('opacity', 1.0) < FLOOR_OPACITY:
                    edits.append((t, 'opacity', s.get('opacity'), FLOOR_OPACITY))
                    if apply: s['opacity'] = FLOOR_OPACITY
        if not edits:
            continue
        n_files += 1; n_edits += len(edits)
        print(f'■ {f.stem}  {len(edits)}건')
        for t, k, old, new in edits[:4]:
            print(f'    {t}.{k}: {old} → {new}')
        if apply:
            assert e.get('conditions') and e.get('verify'), f'{f.stem}: 필수 필드 유실 — 쓰지 않음'
            f.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n{n_files}개 파일 · {n_edits}건 {"적용" if apply else "대상 (--apply 로 실행)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
