"""2026 고3 7월 미적분 27 — 매개변수 곡선(원의 신개선)의 접선과 직선이 이루는 각.

곡선  x = r(cos t + t sin t),  y = r(sin t - t cos t)   (0 < t < pi/2)
  dx/dt = r t cos t,  dy/dt = r t sin t  →  접선의 기울기 = tan t
  t = k 의 점 P(a, b) 에서 접선과 직선 y = m0 x 가 이루는 예각 theta 가 tan theta = tt.
  구하는 값 = ca*a + cb*b + tan k  (보기와 대조해 번호를 답한다)

파라미터를 바꾸면(직선의 기울기·tan theta·반지름·계수) 같은 유형의 새 문제가 만들어진다.
"""
import sympy as sp

CANDIDATE = 4

PARAMS = dict(
    line_slope=sp.Rational(1, 2),        # 기준 직선 y = (1/2)x 의 기울기
    tan_theta=sp.Rational(1, 2),         # 접선과 기준 직선이 이루는 예각 theta 의 tan
    radius=sp.Integer(1),                # 곡선(신개선) 배율 r : x=r(cos t+t sin t), y=r(sin t-t cos t)
    coef_a=sp.Integer(3),                # 구하는 식 ca*a + cb*b + tan k 의 a 계수
    coef_b=sp.Integer(4),                # 같은 식의 b 계수
    choices=[sp.Rational(10, 3), sp.Rational(13, 3), sp.Rational(16, 3),
             sp.Rational(19, 3), sp.Rational(22, 3)],   # 보기 ①~⑤ (정답 번호는 solve 가 정한다)
)


def tangent_slope(prm):
    """두 직선이 이루는 예각의 tan 조건 |(m-m0)/(1+m*m0)| = tt 에서 접선의 기울기 m 을 구한다.
    0 < k < pi/2 이므로 m = tan k > 0 인 근만 유효(원문제의 다른 근 m=0 은 이 조건에서 탈락)."""
    m0 = sp.nsimplify(prm['line_slope'])
    tt = sp.nsimplify(prm['tan_theta'])
    m = sp.Symbol('m', real=True)
    cands = set()
    for sign in (1, -1):
        for s in sp.solve(sp.Eq(m - m0, sign * tt * (1 + m * m0)), m):
            cands.add(sp.simplify(s))
    pos = [s for s in cands if s.is_real and s.is_positive]
    if not pos:
        return None
    return max(pos, key=lambda s: float(s))               # 근이 둘이면 큰 쪽(원문제는 유일)


def value(prm):
    """ca*a + cb*b + tan k 의 정확한 값."""
    m = tangent_slope(prm)
    if m is None:
        return None
    r = sp.nsimplify(prm['radius'])
    ca, cb = sp.nsimplify(prm['coef_a']), sp.nsimplify(prm['coef_b'])
    k = sp.atan(m)
    sin_k = sp.simplify(m / sp.sqrt(1 + m ** 2))          # 0<k<pi/2
    cos_k = sp.simplify(1 / sp.sqrt(1 + m ** 2))
    a = r * (cos_k + k * sin_k)                            # P 의 x좌표
    b = r * (sin_k - k * cos_k)                            # P 의 y좌표
    return sp.simplify(ca * a + cb * b + m)


def solve(prm):
    """조건 → 답. 보기 안에 값이 있으면 보기 번호(1~5), 없으면 값 자체를 돌려준다."""
    v = value(prm)
    if v is None:
        return None
    for i, c in enumerate(prm['choices'], 1):
        c = sp.nsimplify(c)
        if abs(float(v - c)) < 1e-9 and sp.simplify(v - c) == 0:
            return i
    return v


def statement(prm):
    """새 문제 문장."""
    m0, tt = sp.nsimplify(prm['line_slope']), sp.nsimplify(prm['tan_theta'])
    r, ca, cb = sp.nsimplify(prm['radius']), prm['coef_a'], prm['coef_b']
    ch = ''.join(f'{n}{sp.latex(sp.nsimplify(c))} ' for n, c in zip('①②③④⑤', prm['choices']))
    return (f"매개변수 t(0<t<pi/2)로 나타내어진 곡선 "
            f"x={sp.latex(r*(sp.cos(sp.Symbol('t'))+sp.Symbol('t')*sp.sin(sp.Symbol('t'))))}, "
            f"y={sp.latex(r*(sp.sin(sp.Symbol('t'))-sp.Symbol('t')*sp.cos(sp.Symbol('t'))))} "
            f"에 대하여 t=k일 때 곡선 위의 점을 P(a,b)라 하자. P에서의 접선과 직선 "
            f"y={sp.latex(m0)}x가 이루는 예각의 크기를 theta라 하면 tan theta={sp.latex(tt)}이다. "
            f"{ca}a+{cb}b+tan k의 값은? (단, 0<k<pi/2) {ch}".strip())


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
