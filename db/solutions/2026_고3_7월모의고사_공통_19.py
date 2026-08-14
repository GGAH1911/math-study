# f(x)=x^3-12x+k, 닫힌구간 [0,3] 에서 최댓값 40 → 최솟값?
# 구조: g(x)=f(x)-k 의 후보값(양 끝점 + 구간 안 임계점)을 구하면
#       max f = k + max g = (주어진 최댓값)  →  k = M - max g
#       min f = k + min g = M - max g + min g
CANDIDATE = 24
import sympy as sp

PARAMS = dict(
    c3=1,          # x^3 의 계수
    c2=0,          # x^2 의 계수
    c1=-12,        # x 의 계수
    lo=0,          # 구간 왼쪽 끝
    hi=3,          # 구간 오른쪽 끝
    max_val=40,    # 닫힌구간에서의 최댓값(조건)
)


def _extreme_offsets(prm):
    """g(x)=c3x^3+c2x^2+c1x 의 [lo,hi] 위 최대·최소 (상수항 k 를 뺀 값)."""
    x = sp.Symbol('x', real=True)
    lo, hi = sp.nsimplify(prm['lo']), sp.nsimplify(prm['hi'])
    g = sp.nsimplify(prm['c3']) * x**3 + sp.nsimplify(prm['c2']) * x**2 + sp.nsimplify(prm['c1']) * x
    pts = [lo, hi]
    for c in sp.solve(sp.Eq(sp.diff(g, x), 0), x):
        if c.is_real and sp.simplify(c - lo) >= 0 and sp.simplify(hi - c) >= 0:
            pts.append(sp.nsimplify(c))
    vals = [sp.simplify(g.subs(x, p)) for p in pts]
    return max(vals), min(vals)


def solve(prm=None):
    """조건(최댓값 max_val) → 최솟값."""
    prm = dict(PARAMS if prm is None else prm)
    hi_off, lo_off = _extreme_offsets(prm)
    k = sp.nsimplify(prm['max_val']) - hi_off      # 최댓값 조건으로 상수항 결정
    return sp.simplify(k + lo_off)                 # 같은 k 에서의 최솟값


def statement(prm=None):
    prm = dict(PARAMS if prm is None else prm)
    x = sp.Symbol('x')
    f = (sp.nsimplify(prm['c3']) * x**3 + sp.nsimplify(prm['c2']) * x**2
         + sp.nsimplify(prm['c1']) * x + sp.Symbol('k'))
    return (f"닫힌구간 [{prm['lo']},{prm['hi']}] 에서 정의된 함수 f(x)={sp.sstr(f)} 의 "
            f"최댓값이 {prm['max_val']} 일 때, 최솟값을 구하시오. (단, k는 상수이다.)")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
