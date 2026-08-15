from sympy import symbols, ln, Eq, solve as sp_solve, diff, simplify, nsimplify

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 곡선 a*x*y - b*y^n*ln(x) = k 위의 점 (x=1, y0)에서 dy/dx 를 구하는 문제.
#   원문제는 xy - y^3*ln(x) = 2  ↔  a=1, b=1, n=3, k=2  인 특수case.
#
# 구조적으로 x=1 에서는 ln(1)=0 이라 y^n*ln(x) 항이 사라지므로
#   y0 는 항상 선형식 a*y0 = k 의 유일해 y0 = k/a 로 정해진다.
# 음함수 미분 a*(y + x*y') - b*(n*y^(n-1)*y'*ln(x) + y^n/x) = 0 를 x=1 에서 풀면
#   dy/dx = b*y0^n/a - y0
#
# a,b,n,k 는 서로 묶여 있다 — 아무 조합이나 넣으면 dy/dx 가 보기(0,2,4,6,8)
# 범위를 벗어나 "이 보기 구성의 문제"로 성립하지 않는다(지수 n 때문에 값이
# 급격히 커짐). 따라서 규칙 5에 따라 실제로 성립하는 (a,b,n,k) 조합을
# VARIANTS 로 제시한다.

CANDIDATE = 4  # ★원문제 정답 (④ 6)

PARAMS = dict(
    a=1,  # x*y 항의 계수
    b=1,  # y^n*ln(x) 항의 계수
    n=3,  # y 의 지수
    k=2,  # 우변 상수 (= xy - y^3 ln x)
)


def value(prm):
    """곡선 a*x*y - b*y^n*ln(x) = k 위 x=1 점에서 dy/dx 를 sympy 음함수 미분으로 실제 계산."""
    x, y = symbols('x y', real=True)
    a, b, n, k = prm['a'], prm['b'], prm['n'], prm['k']
    curve = a * x * y - b * y**n * ln(x) - k

    # x=1 에서 ln(1)=0 이므로 curve(1, y)=0 은 y 에 대한 선형식 → 유일해
    y0_sols = sp_solve(Eq(curve.subs(x, 1), 0), y)
    if len(y0_sols) != 1:
        raise ValueError(f'x=1 에서 y0 가 유일하게 정해지지 않음: {y0_sols}')
    y0 = y0_sols[0]

    dy_dx = -diff(curve, x) / diff(curve, y)
    val = dy_dx.subs({x: 1, y: y0})
    val = nsimplify(simplify(val))
    if not val.is_real:
        raise ValueError(f'dy/dx 가 실수가 아님: {val}')
    return val


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 0부터 8까지 2씩 증가(값에서 유도된 등간격 창)."""
    return (0, 2, 4, 6, 8)


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # dy/dx 가 보기 범위를 벗어나면 이 보기 구성의 문제로 성립하지 않음
        raise ValueError(f'dy/dx={v} 가 보기 {ch} 범위를 벗어남 — 문제로 성립하지 않음')
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    a, b, n, k = prm['a'], prm['b'], prm['n'], prm['k']
    a_term = 'xy' if a == 1 else f'{a}xy'
    b_term = f'y^{{{n}}}\\ln x' if b == 1 else f'{b}y^{{{n}}}\\ln x'
    return (
        f'곡선 ${a_term} - {b_term} = {k}$에 대하여 $x=1$일 때, '
        f'$\\frac{{dy}}{{dx}}$의 값은?'
    )


# 자연수(정수) 조합이 서로 묶여 있어 하나만 흔들면 보기 범위를 벗어나므로
# 실제로 성립하는 (a,b,n,k) 조합 여러 개를 VARIANTS 로 제시한다.
VARIANTS = [
    dict(a=1, b=1, n=3, k=1),  # y0=1, dy/dx = 1-1 = 0  → ①
    dict(a=1, b=1, n=2, k=2),  # y0=2, dy/dx = 4-2 = 2  → ②
    dict(a=1, b=2, n=1, k=4),  # y0=4, dy/dx = 8-4 = 4  → ③
    dict(a=1, b=3, n=1, k=4),  # y0=4, dy/dx = 12-4 = 8 → ⑤
]

# 원문제 보기가 정확히 ①0 ②2 ③4 ④6 ⑤8 인지 고정 검증
assert choices(PARAMS) == (0, 2, 4, 6, 8)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
