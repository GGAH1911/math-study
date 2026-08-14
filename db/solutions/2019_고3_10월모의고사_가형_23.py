from sympy import symbols, sin, cos, sqrt, diff, simplify, nsimplify, pi, latex, Rational

# ─────────────────────────────────────────────────────────────
# 문제의 수학 구조
#   f(x) = A*sin(x) + B*cos(x)  →  f'(x0) 를 구하시오.
#
# 원문제: f(x) = sin x - √3 cos x  (A=1, B=-√3), x0 = π/3
#   f'(x) = A cos x - B sin x
#   f'(π/3) = 1*(1/2) - (-√3)*(√3/2) = 1/2 + 3/2 = 2
#
# 파라미터화: A(계수), B(계수), x0(미분값을 구할 지점) 세 값이 모두
# 답을 실제로 바꾼다 (아래 검증 참고).
# ─────────────────────────────────────────────────────────────

CANDIDATE = 2  # ★원문제 정답, 절대 변경 금지

PARAMS = dict(
    A=1,
    B=-sqrt(3),
    x0=pi / 3,
)


def solve(prm):
    """f(x) = A sin x + B cos x 를 미분해 x0에서의 값을 구한다."""
    x = symbols('x')
    A, B, x0 = prm['A'], prm['B'], prm['x0']

    f = A * sin(x) + B * cos(x)
    f_prime = diff(f, x)

    val = simplify(f_prime.subs(x, x0))
    val = nsimplify(val)

    if not val.is_number:
        raise ValueError(f"닫힌 형태의 수치 값을 얻지 못했습니다: {val}")

    return val


def _coeff_term(coeff, trig_latex):
    """계수 coeff 와 삼각함수 latex 문자열을 하나의 항 문자열로 만든다."""
    if coeff == 1:
        return f"{trig_latex}", 1
    if coeff == -1:
        return f"{trig_latex}", -1
    # sympy 값 부호 판별
    is_neg = getattr(coeff, 'is_negative', None)
    if is_neg is None:
        is_neg = coeff < 0
    mag = -coeff if is_neg else coeff
    mag_latex = latex(mag)
    return f"{mag_latex}{trig_latex}", (-1 if is_neg else 1)


def statement(prm):
    A, B, x0 = prm['A'], prm['B'], prm['x0']

    a_str, a_sign = _coeff_term(A, r"\sin x")
    b_str, b_sign = _coeff_term(B, r"\cos x")

    # 첫 항은 부호에 따라 그대로/음수 접두, 두번째 항부터는 + 또는 -
    f_expr = ("-" if a_sign < 0 else "") + a_str
    f_expr += (" - " if b_sign < 0 else " + ") + b_str

    x0_latex = latex(x0)

    return (
        f"함수 $f(x)={f_expr}$에 대하여 "
        f"$f'\\left({x0_latex}\\right)$의 값을 구하시오."
    )


if __name__ == '__main__':
    ans = solve(PARAMS)
    print(statement(PARAMS))
    print('answer =', ans)
    print('VERIFY_PASS' if ans == CANDIDATE else 'VERIFY_FAIL')
