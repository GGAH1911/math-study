# 삼차곡선 y=f(x) 와 직선 y=mx+d (Q 는 y축 위 교점).
#   A = 곡선·x축·선분 RQ 로 둘러싸인 부분,  B = 곡선과 선분 QP 로 둘러싸인 부분,  답 = A-B 가 몇 번 보기인가.
# 구조: f(0)=d 이고 Q 가 y축 위 교점이므로 직선의 y절편도 d 다(문제의 "y=4x+2" 의 2 = f(0)).
#   교점: f-g = a x^3 + b x^2 + (c-m) x  → x=0 과 나머지 두 근. 제1사분면 교점이 P.
#   R = 직선의 x절편 = -d/m,  A 의 왼쪽 끝 = 곡선의 x절편.
import sympy as sp

CANDIDATE = 2   # 정답 = 보기 ② (문제의 정답표 값, 건드리지 않는다)

PARAMS = dict(
    a=1, b=2, c=1, d=2,          # f(x) = a x^3 + b x^2 + c x + d  (문제: x^3+2x^2+x+2)
    m=4,                          # 직선 y = m x + d               (문제: y = 4x+2)
    choices=['2', '9/4', '5/2', '11/4', '3'],   # 보기 ①~⑤ (정답 번호는 solve 가 정한다)
)

x = sp.Symbol('x', real=True)


def _num(v):
    return sp.nsimplify(sp.sympify(v))


def _real_roots(poly_expr):
    """실근을 작은 것부터. CRootOf 로 받아 무리근도 정확히 다룬다."""
    p = sp.Poly(sp.expand(poly_expr), x)
    if p.degree() < 1:
        return []
    return sorted(sp.real_roots(p), key=lambda r: float(r.evalf()))


def _area_diff(prm):
    """조건 → A-B 의 값. 그림의 배치가 성립하지 않으면 ValueError."""
    a, b, c, d, m = (_num(prm[k]) for k in ('a', 'b', 'c', 'd', 'm'))
    if a <= 0 or d <= 0 or m <= 0:
        raise ValueError('a, d, m 은 양수여야 그림의 배치가 성립한다')
    f = a * x**3 + b * x**2 + c * x + d
    g = m * x + d                                  # Q(0,d) 를 지나는 직선

    inter = _real_roots(f - g)                     # 곡선과 직선의 교점 x좌표 (0 포함)
    pos = [r for r in inter if float(r.evalf()) > 0]
    if not any(r == 0 for r in inter) or not pos:
        raise ValueError('제1사분면 교점 P 가 없다')
    Px = min(pos, key=lambda r: float(r.evalf()))   # 제1사분면 교점

    Rx = sp.Rational(-1, 1) * d / m                 # 직선의 x절편 R
    zeros = _real_roots(f)                          # 곡선의 x절편
    left = [r for r in zeros if float(r.evalf()) < float(Rx.evalf())]
    if not left:
        raise ValueError('곡선의 x절편이 R 보다 왼쪽에 없다 — A 영역이 닫히지 않는다')
    x0 = max(left, key=lambda r: float(r.evalf()))  # A 영역의 왼쪽 끝
    if any(float(x0.evalf()) < float(r.evalf()) < 0 for r in zeros):
        raise ValueError('곡선이 (x0,0) 안에서 x축을 또 만난다')
    neg = [r for r in inter if float(r.evalf()) < 0]
    if neg and float(max(neg, key=lambda r: float(r.evalf())).evalf()) > float(x0.evalf()):
        raise ValueError('세 번째 교점이 A 영역 안에 있다')

    F = sp.integrate(f, x)
    G = sp.integrate(g, x)
    A = (F.subs(x, 0) - F.subs(x, x0)) - (G.subs(x, 0) - G.subs(x, Rx))
    B = (G.subs(x, Px) - G.subs(x, 0)) - (F.subs(x, Px) - F.subs(x, 0))
    if sp.simplify(A) <= 0 or sp.simplify(B) <= 0:
        raise ValueError('넓이가 양수가 아니다 — 배치가 틀렸다')
    return sp.nsimplify(sp.simplify(A - B))


def solve(prm):
    """답: 보기 번호. (보기에 없는 값이면 값 자체를 돌려준다 — 변형문제는 make_choices 로 보기를 새로 만든다)"""
    val = _area_diff(prm)
    for i, ch in enumerate(prm.get('choices') or [], 1):
        if sp.simplify(val - _num(ch)) == 0:
            return sp.Integer(i)
    return val


def make_choices(val, pos=2):
    """변형문제용 보기 5개 — val 을 pos 번째에 둔 등차 보기."""
    val = _num(val)
    q = sp.denom(val)
    step = sp.Rational(1, q) if q > 1 else sp.Integer(1)
    return [sp.nsimplify(val + (i - pos) * step) for i in range(1, 6)]


def statement(prm):
    a, b, c, d, m = (_num(prm[k]) for k in ('a', 'b', 'c', 'd', 'm'))
    f = sp.latex(a * x**3 + b * x**2 + c * x + d)
    g = sp.latex(m * x + d)
    ch = prm.get('choices') or make_choices(_area_diff(prm))
    opts = '  '.join(f'{n} {sp.latex(_num(v))}' for n, v in zip('①②③④⑤', ch))
    return (f'함수 f(x)={f} 에 대하여 곡선 y=f(x) 와 직선 y={g} 가 제1사분면에서 만나는 점을 P,\n'
            f'y축 위에서 만나는 점을 Q라 하자. 직선 y={g} 가 x축과 만나는 점을 R이라 할 때,\n'
            '곡선 y=f(x)와 x축 및 선분 RQ로 둘러싸인 부분의 넓이를 A, 곡선 y=f(x)와 선분 QP로\n'
            f'둘러싸인 부분의 넓이를 B라 하자. A-B의 값은?\n{opts}')


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
