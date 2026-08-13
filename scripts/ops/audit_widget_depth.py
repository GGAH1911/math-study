#!/usr/bin/env python3
"""**보강이 필요한 위젯**을 가려낸다 — 동작은 하는데 개념을 얕게 보여주는 것들.

★세제곱근 사례에서 나온 문제다. 슬라이더 a 하나로 ∛a 만 보여줬는데, 사장님 지적은
  "근이 3개가 될 수도 있는데 1개만 나온다" 였다. **위젯이 개념의 일부만 담고 있었다.**
  이건 "고장" 이 아니라 "얕음" 이라 기계로 단정할 수 없다 — 후보만 뽑고 사람이 본다.

신호(강한 것부터)
  ① 개념 이름이 **경우 나눔**을 함축하는데(근의 개수·판별식·조건·경우) 파라미터가 1개뿐
  ② 곡선(fns)이 상수식뿐 — 슬라이더가 점만 움직이고 **곡선 모양이 안 변한다**
  ③ 파라미터가 1개뿐인데 readout 이 3개 이상 — 보여줄 건 많은데 조작할 게 없다
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/concept-widgets'
CASE_WORDS = ('근의_개수', '판별식', '경우', '조건', '개수', '분류', '판정', '존재', '해의')


def check(path: Path) -> dict | None:
    d = json.loads(path.read_text(encoding='utf-8'))
    s = d.get('spec') or {}
    params = [p.get('name') for p in (s.get('params') or [])]
    cid = d.get('id') or path.stem
    plot = s.get('plot') or {}
    fns = [f.get('fn', '') for f in (plot.get('fns') or [])]
    pnames = set(params)
    # 곡선 식에 파라미터가 하나도 안 들어가면 = 곡선 모양이 고정
    curve_fixed = bool(fns) and not any(
        any(re.search(rf'\b{re.escape(p)}\b', fn) for p in pnames) for fn in fns)
    signals = []
    if len(params) <= 1 and any(w in cid for w in CASE_WORDS):
        signals.append('경우나눔 개념인데 파라미터 1개')
    if curve_fixed:
        signals.append('곡선 모양이 고정(점만 움직임)')
    if len(params) <= 1 and len(s.get('readout') or []) >= 3:
        signals.append('조작 1개 · 표시 3개+')
    if not signals:
        return None
    return {'id': cid, 'file': path.name, 'params': params,
            'fns': fns[:3], 'signals': signals}


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--json'); a = ap.parse_args()
    rows = [r for f in sorted(DIR.glob('*.json')) if (r := check(f))]
    import collections
    c = collections.Counter(s for r in rows for s in r['signals'])
    print(f'보강 후보 {len(rows)}개')
    for k, n in c.most_common(): print(f'  {n:>4}  {k}')
    if a.json:
        Path(a.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'→ {a.json}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
