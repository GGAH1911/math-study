#!/usr/bin/env python3
"""위젯 스펙이 **렌더러가 모르는 속성**을 쓰는지 검사한다.

★왜 필요한가: `verify_widget_fix.py` 는 "스펙 산출물이 달라지는가" 만 본다. 렌더러가
  무시하는 속성을 바꿔도 통과한다 — 화면에서는 아무 일이 없는데 게이트는 녹색이다.
  (2026-08-14 표본 검토에서 발견. 그때는 `color:'transparent'` 가 마침 지원되는
   관용구라 문제없었지만, 운이었다.)

어휘는 렌더러 코드에서 뽑은 것을 여기 적어 둔다. **렌더러가 바뀌면 여기도 바꾼다.**
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/concept-widgets'

SHAPE_KEYS = {
    'point':   {'type','at','label','color','labelDir'},
    'polygon': {'type','vertices','labels','fill','fillOpacity','stroke','closed','label','color'},
    'line':    {'type','from','to','label','dashed','color'},
    'segment': {'type','from','to','label','dashed','color'},
    'circle':  {'type','center','radius','label','fill','fillOpacity','stroke','color','dashed'},
    'ellipse': {'type','center','rx','ry','rotation','label','fill','fillOpacity','stroke','color'},
    'hyperbola': {'type','center','a','b','label','color'},
    'vector':  {'type','from','to','label','color'},
    'angle':   {'type','at','from','to','label','radius','color'},
    'text':    {'type','at','text','color'},
    'parametric': {'type','x','y','tRange','label','color','dashed','closed','fill'},
}
PLOT_KEYS = {'range','yRange','showAxes','showGrid','grid','title','fns','points','pointsLabel',
             'roots','intersections','annotations','xLabel','yLabel','height'}
FN_KEYS   = {'fn','label','color','dashed','range','closed','fnType','graphType','scope',
             'x','y','points','derivative','nSamples'}
GEOM_KEYS = {'range','yRange','showAxes','showGrid','title','shapes','height','xLabel','yLabel'}
PARAM_KEYS= {'name','label','type','min','max','init','step','unit','options'}
READ_KEYS = {'label','expr','digits','unit'}


def check(path: Path) -> list[str]:
    d = json.loads(path.read_text(encoding='utf-8'))
    s = d.get('spec') or {}
    bad: list[str] = []
    for p in s.get('params') or []:
        for k in p:
            if k not in PARAM_KEYS: bad.append(f"params[{p.get('name')}].{k}")
    for r in s.get('readout') or []:
        for k in r:
            if k not in READ_KEYS: bad.append(f"readout.{k}")
    plot = s.get('plot') or {}
    for k in plot:
        if k not in PLOT_KEYS: bad.append(f'plot.{k}')
    for fn in plot.get('fns') or []:
        for k in fn:
            if k not in FN_KEYS: bad.append(f'plot.fns.{k}')
    for gk in ('geometry', 'geometry3d'):
        g = s.get(gk) or {}
        if gk == 'geometry3d':
            continue                                   # 3D 어휘는 별도 — 여기선 안 본다
        for k in g:
            if k not in GEOM_KEYS: bad.append(f'{gk}.{k}')
        for sh in g.get('shapes') or []:
            t = sh.get('type')
            if t not in SHAPE_KEYS:
                bad.append(f'{gk}.shape[type={t}]'); continue
            for k in sh:
                if k not in SHAPE_KEYS[t]: bad.append(f'{gk}.{t}.{k}')
    return sorted(set(bad))


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--json'); a = ap.parse_args()
    rows = []
    for f in sorted(DIR.glob('*.json')):
        try: b = check(f)
        except Exception as e: b = [f'parse: {e}']
        if b: rows.append({'file': f.name, 'unknown': b})
    import collections
    c = collections.Counter(k for r in rows for k in r['unknown'])
    print(f'위젯 {len(list(DIR.glob("*.json")))}개 · 미지 속성 사용 {len(rows)}개')
    for k, n in c.most_common(15): print(f'  {n:>4}  {k}')
    if a.json:
        Path(a.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'→ {a.json}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
