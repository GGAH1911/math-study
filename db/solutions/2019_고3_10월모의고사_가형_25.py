from sympy import symbols, Rational, Abs, simplify
from sympy import solve as sp_solve

CANDIDATE = 18  # ★원문제 정답 (절대 변경 금지)

# 문제의 수학 구조를 파라미터로 분리:
#  - 타원: x^2/a2 + y^2/b2 = 1  (a2, b2 는 각각 x^2, y^2 의 분모)
#  - 외부 점 A(px, py) 에서 타원에 그은 두 접선의 접점 B, C
# 원문제는 a2=12, b2=16, A=(6,4).
PARAMS = dict(a2=12, b2=16, px=6, py=4)


def _tangent_points(a2, b2, px, py):
    """A(px,py)에서 타원 x^2/a2+y^2/b2=1 에 그은 접선들의 접점 B, C를 구한다.

    접점 (x0,y0) 에서의 접선: x*x0/a2 + y*y0/b2 = 1.
    이 접선이 A를 지나므로: px*x0/a2 + py*y0/b2 = 1  ... (극선, chord of contact)
    (x0,y0) 는 타원 위의 점이므로: x0^2/a2 + y0^2/b2 = 1
    두 식을 연립하면 접점이 정확히 두 개(B, C) 나온다.
    """
    x0, y0 = symbols('x0 y0', real=True)
    eqs = [
        Rational(px) * x0 / a2 + Rational(py) * y0 / b2 - 1,
        x0**2 / a2 + y0**2 / b2 - 1,
    ]
    sols = sp_solve(eqs, [x0, y0], dict=True)
    pts = [(s[x0], s[y0]) for s in sols]
    if len(pts) != 2:
        # 접선이 두 개(즉 서로 다른 접점 두 개) 나오지 않으면
        # 점 A가 타원 외부의 일반위치에 있지 않다는 뜻이므로 문제로 성립하지 않음.
        raise ValueError("접점이 정확히 2개 나오지 않음 (A가 타원 외부의 일반위치가 아님)")
    return pts


def value(prm):
    """삼각형 ABC의 넓이를 sympy로 정확히 계산."""
    a2, b2, px, py = prm['a2'], prm['b2'], prm['px'], prm['py']

    # A가 타원 외부에 있어야 두 개의 실접선이 존재
    if Rational(px)**2 / a2 + Rational(py)**2 / b2 <= 1:
        raise ValueError("점 A가 타원 내부(또는 위)에 있어 접선이 존재하지 않음")

    (bx, by), (cx, cy) = _tangent_points(a2, b2, px, py)

    # 삼각형 넓이 공식 (좌표를 이용한 신발끈 공식)
    area = Abs(px * (by - cy) + bx * (cy - py) + cx * (py - by)) / 2
    return simplify(area)


def solve(prm):
    return value(prm)


def statement(prm):
    a2, b2, px, py = prm['a2'], prm['b2'], prm['px'], prm['py']
    return (
        f"점 A({px}, {py})에서 타원 \\frac{{x^2}}{{{a2}}}+\\frac{{y^2}}{{{b2}}}=1에 그은 "
        f"두 접선의 접점을 각각 B, C라 할 때, 삼각형 ABC의 넓이를 구하시오."
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

    # --- 파라미터를 바꾸면 답이 실제로 달라지는지 확인 (개발 확인용) ---
    # px 를 바꾼 경우
    assert solve(dict(a2=12, b2=16, px=8, py=4)) != CANDIDATE
    # a2 를 바꾼 경우
    assert solve(dict(a2=9, b2=16, px=6, py=4)) != CANDIDATE
