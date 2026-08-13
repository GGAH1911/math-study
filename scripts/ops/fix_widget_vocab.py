#!/usr/bin/env python3
"""위젯 스펙의 **속성 이름 오기**를 렌더러 어휘로 정규화한다.

★왜: 렌더러는 `polygon.vertices` 를 기대하는데 257개 위젯이 `points` 를 쓴다.
  `Geometry.tsx:87` 이 vertices 없는 polygon 을 **조용히 버린다**(크래시 방지).
  즉 그 도형들은 화면에 아예 안 나온다 — 슬라이더는 멀쩡히 움직이는데 그림이 비어 있다.
  자동 생성기가 만든 오기이고, 뜻은 같으므로 기계적으로 고칠 수 있다.

★쓰기 전에 검사한다(2026-08-14 교훈: 정규식 하나로 파일을 날린 적이 있다).
사용: python3 scripts/ops/fix_widget_vocab.py [--apply]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/concept-widgets'

# 도형타입 → {오기: 정식이름}. 두 점을 받는 도형은 from/to 가 정식이다.
RENAME = {
    'polygon': {'points': 'vertices', 'opacity': 'fillOpacity'},
    'segment': {'start': 'from', 'end': 'to', 'p1': 'from', 'p2': 'to',
                'stroke': 'color', 'dash': 'dashed', 'style': None, 'strokeWidth': None},
    'line':    {'start': 'from', 'end': 'to', 'point1': 'from', 'point2': 'to'},
}
# 배열 하나로 두 점을 주는 형태 → from/to 로 편다
PAIR_KEYS = ('points', 'endpoints', 'coords', 'through')


def fix_shape(sh: dict) -> tuple[dict, list[str]]:
    t, log = sh.get('type'), []
    out = dict(sh)
    for old, new in (RENAME.get(t) or {}).items():
        if old in out:
            if new is None:
                out.pop(old); log.append(f'{t}.{old} 제거(렌더러 미지원)')
            elif new not in out:
                out[new] = out.pop(old); log.append(f'{t}.{old}→{new}')
            else:
                out.pop(old); log.append(f'{t}.{old} 중복 제거')
    if t in ('segment', 'line'):
        for k in PAIR_KEYS:
            v = out.get(k)
            if isinstance(v, list) and len(v) == 2 and all(isinstance(x, list) for x in v):
                out.pop(k); out.setdefault('from', v[0]); out.setdefault('to', v[1])
                log.append(f'{t}.{k}→from/to')
        if 'x' in out and 'from' not in out:           # 세로선 관용구
            x = out.pop('x'); out['from'] = [x, '=yRange0']; out['to'] = [x, '=yRange1']
            log.append('line.x→from/to(세로선)')
    return out, log


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--apply', action='store_true'); a = ap.parse_args()
    changed = fixed = 0
    for f in sorted(DIR.glob('*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        g = (d.get('spec') or {}).get('geometry') or {}
        shapes = g.get('shapes')
        if not isinstance(shapes, list):
            continue
        logs, new_shapes = [], []
        for sh in shapes:
            if not isinstance(sh, dict): new_shapes.append(sh); continue
            ns, lg = fix_shape(sh); new_shapes.append(ns); logs += lg
        if not logs:
            continue
        changed += 1; fixed += len(logs)
        if a.apply:
            g['shapes'] = new_shapes
            txt = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
            # ★쓰기 전 검사 — 핵심 구조가 살아 있는지
            chk = json.loads(txt)
            assert chk.get('id') == d.get('id') and (chk['spec'].get('params') is not None), '구조 손상 — 쓰지 않음'
            assert len(chk['spec']['geometry']['shapes']) == len(shapes), '도형 수 변화 — 쓰지 않음'
            f.write_text(txt, encoding='utf-8')
        if changed <= 3:
            print(f'  {f.name}: {", ".join(logs[:4])}{" …" if len(logs) > 4 else ""}')
    print(f"{'[적용]' if a.apply else '[dry-run]'} 위젯 {changed}개 · 속성 {fixed}건")
    return 0


if __name__ == '__main__':
    sys.exit(main())
