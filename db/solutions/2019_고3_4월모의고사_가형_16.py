import sympy as sp

# ── 수학 구조 ───────────────────────────────────────────────────────────
# 문제: 두 곡선 y=sin(x)ln(x), y=cos(x)/x 와 두 직선 x=a, x=b 로 둘러싸인 넓이.
#   핵심 관찰(부분적분): d/dx[-cos(x)ln(x)] = sin(x)ln(x) - cos(x)/x
#   → 부정적분 F(x) = -cos(x)ln(x) 이며 (도중에 생기는 코사인적분 Ci(x) 항이
#     정확히 상쇄된다 — sympy.integrate 로 실제 계산해 확인한다).
#   → 넓이 = F(b) - F(a) = cos(a)ln(a) - cos(b)ln(b)
# a, b(적분구간의 양 끝점, π의 유리수배)가 문제를 정하는 파라미터다.
# 보기는 "정답의 부호/계수를 착각한 전형적 오답"을 P=cos(a)ln(a), Q=cos(b)ln(b)
# 의 선형결합으로 구성해 유도한다 — a, b 둘 다 정답(보기 번호)을 실제로 바꾼다.

x = sp.symbols('x', positive=True)
_integrand = sp.sin(x) * sp.log(x) - sp.cos(x) / x
_F = sp.integrate(_integrand, x)                     # sympy가 실제로 적분(Ci 상쇄 확인)
assert sp.simplify(sp.diff(_F, x) - _integrand) == 0  # 부정적분 검산

CANDIDATE = 4  # ★원문제 정답(보기 ④) — 절대 바꾸지 않음

PARAMS = dict(
    a=sp.pi / 2,   # 적분구간 왼쪽 끝
    b=sp.pi,       # 적분구간 오른쪽 끝
)


def value(prm):
    """F(b) - F(a) 를 실제로 대입·계산해 넓이(정답 값)를 구한다."""
    a, b = prm['a'], prm['b']
    return sp.simplify(_F.subs(x, b) - _F.subs(x, a))


def choices(prm):
    """전형적 부호/계수 오류 패턴으로부터 보기 5개를 유도한다."""
    a, b = prm['a'], prm['b']
    P = sp.cos(a) * sp.log(a)          # 왼쪽 경계항
    Q = sp.cos(b) * sp.log(b)          # 오른쪽 경계항
    f1 = sp.simplify(-sp.Rational(1, 4) * Q)
    f2 = sp.simplify(-sp.Rational(1, 2) * Q)
    f3 = sp.simplify(-sp.Rational(3, 4) * Q)
    f4 = sp.simplify(2 * P - sp.Rational(5, 4) * Q)   # 경계항 계수를 잘못 안(더 큰 오답)
    f5 = sp.simplify(P - Q)                            # 정답 = F(b)-F(a)
    raw = {f1, f2, f3, f4, f5}
    ch = sorted(raw, key=lambda v: sp.N(v))
    if len(ch) != 5:
        raise ValueError('보기 개수가 5개가 아니다 — 이 파라미터 조합은 문제로 성립하지 않는다')
    return ch


# 원문제 보기와 정확히 일치하는지 고정
_ln_pi = sp.log(sp.pi)
assert choices(PARAMS) == sorted(
    [sp.Rational(1, 4) * _ln_pi, sp.Rational(1, 2) * _ln_pi, sp.Rational(3, 4) * _ln_pi,
     _ln_pi, sp.Rational(5, 4) * _ln_pi],
    key=lambda v: sp.N(v),
)


def solve(prm):
    v = sp.simplify(value(prm))
    ch = choices(prm)
    for i, c in enumerate(ch):
        if sp.simplify(c - v) == 0:
            return i + 1
    raise ValueError('계산된 값이 보기 목록 안에 없다 — 성립하지 않는 문제')


def statement(prm):
    a, b = prm['a'], prm['b']
    return (
        "두 곡선 y = (\\sin x)\\ln x, y = \\frac{\\cos x}{x}와 두 직선 "
        f"x = {sp.latex(a)}, x = {sp.latex(b)}로 둘러싸인 부분의 넓이는?"
    )


if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
