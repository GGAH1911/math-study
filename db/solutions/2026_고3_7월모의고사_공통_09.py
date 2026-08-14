# 삼차함수 f(x)=a x^3 + b x^2 + c x + d 의 그래프 위의 점 (t, f(t)) 에서의 접선이
# 점 (px, py) 를 지나도록 하는 양수 t 를 구하고, 그 값을 보기와 대조해 답 번호를 낸다.
#   접선: y - f(t) = f'(t)(x - t)  →  (px, py) 대입:  py - f(t) = f'(t)(px - t)
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
CANDIDATE = 5
import sympy as sp

PARAMS = dict(
    a=2, b=-7, c=0, d=1,        # f(x) = a x^3 + b x^2 + c x + d
    px=0, py=1,                 # 접선이 지나야 하는 점 (px, py)
    choices=[sp.Rational(3, 4), sp.Integer(1), sp.Rational(5, 4),
             sp.Rational(3, 2), sp.Rational(7, 4)],   # 보기 ①~⑤ (정답 번호는 solve 가 정한다)
)


def tangent_point(prm):
    """접선이 (px, py) 를 지나게 하는 양수 t. (조건 → 값, 문제의 수학 구조)"""
    t = sp.symbols('t', real=True)
    f = prm['a']*t**3 + prm['b']*t**2 + prm['c']*t + prm['d']
    cond = sp.expand(prm['py'] - f - sp.diff(f, t)*(prm['px'] - t))   # = 0 이어야 함
    poly = sp.Poly(cond, t)
    pos = [r for r in sp.real_roots(poly) if r.is_positive]
    if not pos:
        raise ValueError('양수 해 없음')
    hit = [r for r in pos if any(sp.simplify(r - sp.nsimplify(v)) == 0 for v in prm['choices'])]
    return sp.nsimplify(hit[0] if hit else min(pos))   # 보기에 있는 해 우선, 없으면 최소 양수해


def solve(prm):
    """구한 t 를 보기와 대조한 답 번호. (보기에 없으면 = 새 보기가 필요한 변형문제 → 값 자체)"""
    t0 = tangent_point(prm)
    for i, v in enumerate(prm['choices'], 1):
        if sp.simplify(t0 - sp.nsimplify(v)) == 0:
            return i
    return t0


def make_variant(**over):
    """유사문제 재생성: 계수를 바꾸면 답 t 를 계산해 그 값이 들어간 보기 5개를 자동 구성한다.
    반환 (새 PARAMS, 정답 번호)."""
    prm = {**PARAMS, **over}
    t0 = tangent_point({**prm, 'choices': []})
    pool = sorted({t0 + sp.Rational(k, 4) for k in (-3, -2, -1, 1, 2, 3) if t0 + sp.Rational(k, 4) > 0})
    ch = sorted(set(pool[:4]) | {t0})
    prm['choices'] = ch
    return prm, ch.index(t0) + 1


def statement(prm):
    x = sp.Symbol('x')
    f = sp.expand(prm['a']*x**3 + prm['b']*x**2 + prm['c']*x + prm['d'])
    ch = ' '.join(f'{"①②③④⑤"[i]}{sp.nsimplify(v)}' for i, v in enumerate(prm['choices']))
    return (f"양수 t 에 대하여 함수 f(x)={f} 의 그래프 위의 점 (t, f(t)) 에서의 접선이 "
            f"점 ({prm['px']}, {prm['py']}) 을 지나도록 하는 t 의 값은?  {ch}")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
