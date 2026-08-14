from sympy import (
    symbols, S, ln, diff, integrate, simplify, Eq, nsimplify,
    solve as sp_solve,
)

# ----------------------------------------------------------------------
# 문제의 수학 구조
#   x f(x) = k*C^x + a + ∫[0,x] t f'(t) dt   (f는 R에서 미분가능, a는 상수)
#
# 풀이의 핵심 구조:
#   1) 양변을 x로 미분하면 좌변 f(x)+x f'(x), 우변 k*C^x*ln(C)+x f'(x) 에서
#      x f'(x) 항이 소거되어 f(x) = k*C^x*ln(C) 로 f 가 완전히 결정된다.
#   2) 이 f 를 원래의 함수방정식(적분 포함)에 다시 대입하면 항등식이 되도록
#      하는 상수 a 가 하나로 정해진다 (x=0 을 대입하면 가장 간단히 나온다).
#   3) 구한 a 를 f 에 대입해 f(a) 를 계산한다.
#
# 파라미터로 뽑은 수학 구조:
#   C : 지수함수의 밑 (원문제는 3)
#   k : 지수항 앞의 계수 (원문제는 1, 즉 "3^x")
#   두 값 모두 a, f(a) 의 값을 실제로 바꾼다 (아래 검증 참고).
# ----------------------------------------------------------------------

PARAMS = dict(
    C=3,   # x f(x) = k*C^x + a + ... 의 밑
    k=1,   # x f(x) = k*C^x + a + ... 의 계수
)
CANDIDATE = 4  # 원문제 정답 보기 번호 (④ ln3/3)


def value(prm):
    """함수방정식을 실제로 풀어 f(a) 의 값(수식)을 sympy 로 구한다."""
    C = S(prm['C'])
    k = S(prm['k'])
    if C <= 1:
        raise ValueError("C 는 1보다 커야 지수함수 조건이 성립한다")

    x, t, a = symbols('x t a', real=True)

    # 1) 양변을 x로 미분해 얻어지는 f(x) (x f'(x) 항이 소거되어 결정됨)
    f_expr = k * C**x * ln(C)
    fprime_expr = diff(f_expr, x)

    # 2) 원래 함수방정식에 f, f' 를 대입해 정말로 항등식을 만드는 a 를 구한다
    integrand = t * fprime_expr.subs(x, t)
    antideriv = integrate(integrand, t)
    integral_val = antideriv.subs(t, x) - antideriv.subs(t, 0)

    lhs = x * f_expr
    rhs = k * C**x + a + integral_val

    a_candidates = sp_solve(Eq(lhs.subs(x, 0), rhs.subs(x, 0)), a)
    if not a_candidates:
        raise ValueError("함수방정식을 만족하는 a 가 존재하지 않는다")
    a_val = a_candidates[0]

    # 모든 x에서 항등식이 성립하는지 실제로 검증(부분적분 결과가 맞는지 포함)
    if simplify(lhs - rhs.subs(a, a_val)) != 0:
        raise ValueError("주어진 조건으로 항등식이 성립하지 않는다")

    return simplify(f_expr.subs(x, a_val))


def choices(prm):
    """value(prm)에서 유도한 5지선다 보기(원문제의 전형적 오답 패턴 포함)."""
    C = S(prm['C'])
    k = S(prm['k'])
    v = value(prm)

    # 흔한 실수: 상수항 k*C^x 를 미분/대입하며 밑을 C 대신 C-1 로 잘못 쓰거나
    # 지수 C^k 대신 (C-1)을 분모로 잘못 쓰는 경우를 모사해 오답을 만든다.
    c_a = ln(C - 1) / (2 * C**k)
    c_b = ln(C - 1) / C**k
    c_c = ln(C - 1) / (C - 1)
    c_d = v
    c_e = ln(C) / (C - 1)

    cands = [c_a, c_b, c_c, c_d, c_e]
    # 실제 시험 보기처럼 값의 오름차순으로 정렬해 ①~⑤ 를 매긴다
    ordered = sorted(cands, key=lambda e: float(e.evalf()))
    return ordered


def solve(prm):
    """f(a)의 값이 정렬된 보기 중 몇 번째(1-based)인지를 답으로 돌려준다."""
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if simplify(c - v) == 0:
            return i
    raise ValueError("계산한 값이 보기 목록 어디에도 없다")


def statement(prm):
    C = prm['C']
    k = prm['k']
    coeff = '' if k == 1 else f'{k} \\cdot '
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{lb} {c}' for lb, c in zip(labels, ch))
    return (
        "실수 전체의 집합에서 미분가능한 함수 f(x)가\n"
        f"  x f(x) = {coeff}{C}^x + a + \\int_{{0}}^{{x}} t f'(t)\\,dt\n"
        "를 만족시킬 때, f(a)의 값은? (단, a는 상수이다.)\n"
        f"{opts}"
    )


# 원문제(C=3, k=1) 기준으로 유도한 보기가 실제 원문제 보기와 일치하는지 고정
_orig_choices = choices(PARAMS)
assert simplify(_orig_choices[0] - ln(2) / 6) == 0
assert simplify(_orig_choices[1] - ln(2) / 3) == 0
assert simplify(_orig_choices[2] - ln(2) / 2) == 0
assert simplify(_orig_choices[3] - ln(3) / 3) == 0
assert simplify(_orig_choices[4] - ln(3) / 2) == 0

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
