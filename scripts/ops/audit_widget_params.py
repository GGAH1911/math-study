#!/usr/bin/env python3
"""위젯 슬라이더가 **실제로 무언가를 움직이는가** 를 결정적으로 검사한다.

★두 종류의 결함이 있다. 둘 다 "슬라이더를 움직여도 아무 일이 없다" 로 보인다.
  L1 완전 미사용 — 파라미터 이름이 스펙 어디에도 안 나온다
  L2 시각 무반응 — 숫자(readout)만 바뀌고 **그림(plot/geometry)이 안 변한다**
     예: 세제곱근 위젯. a → root → readout 은 이어지는데 plot 은 `y=x³` 고정이었다.
     학습자에게는 "고장" 으로 보인다 — 개념을 눈으로 이해하라고 만든 위젯이기 때문이다.

★의존은 **전이적으로** 따라간다. `scope` 가 `root = f(a)` 를 만들고 plot 이 `root` 를 쓰면
  a 는 살아 있는 것이다. 이름 등장 여부만 보면 이 경우를 놓친다.

사용: python3 scripts/ops/audit_widget_params.py [--json out.json]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'web/src/data/concept-widgets'
IDENT = re.compile(r'[A-Za-z_][A-Za-z_0-9]*')


def scope_edges(scope: str) -> list[tuple[str, set[str]]]:
    """`v = expr; w = expr2` → [(v, {expr 안의 식별자}), ...] (선언 순서 유지)."""
    out = []
    for stmt in re.split(r'[;\n]', scope or ''):
        if '=' not in stmt:
            continue
        lhs, rhs = stmt.split('=', 1)
        name = lhs.strip()
        if not name or not IDENT.fullmatch(name):
            continue
        out.append((name, set(IDENT.findall(rhs))))
    return out


def idents_in(obj) -> set[str]:
    """중첩 구조 안의 모든 문자열에서 식별자를 긁는다(`=expr` 형태 포함)."""
    got: set[str] = set()
    if isinstance(obj, str):
        got |= set(IDENT.findall(obj))
    elif isinstance(obj, list):
        for x in obj:
            got |= idents_in(x)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('label', 'title', 'pointsLabel', 'unit', 'name', 'color', 'id'):
                continue                      # 표시용 문자열은 의존이 아니다
            got |= idents_in(v)
    return got


def reaches(seed: str, targets: set[str], scope: str) -> bool:
    """seed 가 (scope 전이 포함) targets 중 하나에 닿는가."""
    live = {seed}
    for _ in range(12):                        # 얕은 고정점 — scope 는 길어야 수 줄이다
        grew = False
        for name, deps in scope_edges(scope):
            if name not in live and (deps & live):
                live.add(name); grew = True
        if not grew:
            break
    return bool(live & targets)


def audit_one(path: Path) -> dict | None:
    try:
        d = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        return {'file': path.name, 'error': str(e)[:80]}
    spec = d.get('spec') or {}
    params = [p.get('name') for p in (spec.get('params') or []) if p.get('name')]
    if not params:
        return None
    scope = spec.get('scope') or ''
    # ★`fns[].fn` 안의 `x` 는 **그래프의 가로축 변수**이지 슬라이더가 아니다.
    #   슬라이더 이름이 x 면 fns 에 x 가 널려 있어 "닿는다" 로 오판한다 —
    #   실제로는 움직여도 아무 일이 없다(2026-08-14 분수식 위젯에서 실측).
    #   그래서 fns 는 축 변수를 뺀 뒤 본다. points·geometry 의 `=식` 은 그대로 센다.
    plot = dict(spec.get('plot') or {})
    axis_free = dict(plot)
    axis_free['fns'] = [{k: v for k, v in (f or {}).items() if k != 'fn'} for f in (plot.get('fns') or [])]
    fn_idents = set()
    for f in (plot.get('fns') or []):
        fn_idents |= set(IDENT.findall(str((f or {}).get('fn', ''))))
    fn_idents.discard('x')                       # 축 변수는 의존이 아니다
    visual = idents_in({k: spec.get(k) for k in ('geometry', 'geometry3d') if spec.get(k)})
    visual |= idents_in(axis_free) | fn_idents
    readout = idents_in(spec.get('readout'))
    anywhere = visual | readout | set(IDENT.findall(scope))

    dead, blind = [], []
    for p in params:
        if p not in anywhere:
            dead.append(p)
        elif not reaches(p, visual, scope):
            blind.append(p)
    if not dead and not blind:
        return None
    return {'file': path.name, 'id': d.get('id'), 'params': params,
            'dead': dead, 'blind': blind,
            'has_plot': bool(spec.get('plot')), 'has_geom': bool(spec.get('geometry') or spec.get('geometry3d'))}


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--json'); a = ap.parse_args()
    files = sorted(DIR.glob('*.json'))
    bad = [r for f in files if (r := audit_one(f))]
    dead_n = sum(len(r.get('dead') or []) for r in bad)
    blind_n = sum(len(r.get('blind') or []) for r in bad)
    print(f'위젯 {len(files)}개 · 결함 {len(bad)}개')
    print(f'  L1 완전 미사용 파라미터 {dead_n}개')
    print(f'  L2 시각 무반응 파라미터 {blind_n}개')
    only_read = [r for r in bad if r.get('blind') and not r.get('dead') and not r.get('has_plot') and not r.get('has_geom')]
    print(f'  (그림 자체가 없는 위젯 {len(only_read)}개 — 숫자만 있는 스펙)')
    if a.json:
        Path(a.json).write_text(json.dumps(bad, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'→ {a.json}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
