import sympy as sp
from sympy import Rational, exp, symbols, diff, simplify

CANDIDATE = 4  # 원문제 정답: ④ 8e

# ----------------------------------------------------------------------------
# 문제의 수학 구조
#
#   x > 0 : f(x) = a*x*e^{2x} + b*x^2                       (a, b는 상수)
#   x < 0 : x_1 < x_2 < 0 인 임의의 x_1, x_2 에 대해
#               f(x_2) - f(x_1) = k*(x_2 - x_1)
#           => x < 0에서 f는 기울기가 k인 직선.
#              f가 실수 전체에서 미분가능(따라서 연속)하므로
#              x -> 0- 극한과 x -> 0+ 극한(=f(0)=0)이 같아야 해서
#              x < 0에서 f(x) = k*x.
#   x = 0에서 미분가능 : f'(0+) = a,  f'(0-) = k  =>  a = k
#   f(x0) = v * e^{2*x0} 라는 조건으로 b를 결정
#          (원문제는 x0 = 1/2, v = 2, 즉 f(1/2) = 2e)
#   구하는 값 : f'(x0)
#
#   f'(x0) 는 항상 e^{2*x0}의 정수배(coef)로 정리되고, 원문제의 보기
#   2e, 4e, 6e, 8e, 10e 는 e^{2*x0}(=e^1=e)의 1~5배 등차수열이다.
#   즉 unit = 2 일 때 coef = unit*m 형태이고 정답은 m번째 보기.
#
# 답을 실제로 바꾸는 파라미터(직접 실행하여 확인함):
#   - v  : k=3, x0=1/2, unit=2 고정, v=2 -> coef=8 (④) / v=3/2 -> coef=6 (③)
#   - k  : x0=1(≠1/2일 때는 k가 살아남음), v=1, unit=1 고정,
#          k=1 -> coef=3 (③) / k=3 -> coef=5 (⑤)
#   (참고: x0=1/2인 특수점에서는 (2x0-1)=0이 되어 k의 기여가 상쇄되므로,
#    k의 영향을 보려면 x0 != 1/2 이어야 한다.)
# ----------------------------------------------------------------------------

PARAMS = dict(
    k=3,                 # 조건 (나)의 기울기 상수 (x<0에서 f(x)=k*x)
    x0=Rational(1, 2),   # 값을 묻는 점 (원문제: f(1/2), f'(1/2))
    v=2,                 # f(x0) = v * e^{2*x0}  (원문제: f(1/2)=2e -> v=2)
    unit=2,              # 보기(선택지) 간격의 단위. 보기 = unit*1..5 * e^{2*x0}
)

# 파라미터들이 서로 묶여 있어(전 구간에서 미분가능 + 보기 범위 안에 들어와야
# 함) 자유롭게 흔들 수 없는 경우를 대비해, 실제로 정답이 달라지는 두 개의
# 대안 조합을 함께 제시한다.
VARIANTS = [
    PARAMS,
    dict(k=3, x0=Rational(1, 2), v=Rational(3, 2), unit=2),   # coef=6 -> ③
    dict(k=1, x0=1, v=1, unit=1),                             # coef=3 -> ③
    dict(k=3, x0=1, v=1, unit=1),                             # coef=5 -> ⑤
]


def _core(prm):
    """조건을 세워 b를 풀고 f'(x0)를 계산한다."""
    k = sp.nsimplify(prm['k'])
    x0 = sp.nsimplify(prm['x0'])
    v = sp.nsimplify(prm['v'])
    unit = sp.nsimplify(prm['unit'])

    x = symbols('x', real=True)
    b = symbols('b', real=True)
    a = k  # x=0에서 미분가능 조건: f'(0+) = a = k = f'(0-)

    f_pos = a * x * exp(2 * x) + b * x ** 2
    E0 = exp(2 * x0)

    # f(x0) = v * e^{2*x0} 조건으로 b 결정
    eq = sp.Eq(f_pos.subs(x, x0), v * E0)
    b_sol = sp.solve(eq, b)
    if not b_sol:
        raise ValueError('조건을 만족하는 b가 존재하지 않습니다.')
    b_val = b_sol[0]

    fprime = simplify(diff(f_pos.subs(b, b_val), x).subs(x, x0))
    coef = simplify(fprime / E0)

    if coef.free_symbols or not coef.is_number:
        raise ValueError('f\'(x0)가 e^{2*x0}의 배수로 정리되지 않습니다.')

    return fprime, E0, coef, unit


def value(prm):
    """문제의 수학적 답 f'(x0) (예: 8e)."""
    fprime, _, _, _ = _core(prm)
    return fprime


def choices(prm):
    """값에서 유도한 5개의 보기 (e^{2x0}의 unit*1..5 배 등차수열)."""
    _, E0, _, unit = _core(prm)
    return [unit * i * E0 for i in range(1, 6)]


def solve(prm):
    """정답 보기 번호(1~5)."""
    _, _, coef, unit = _core(prm)
    m = simplify(coef / unit)
    if not m.is_Integer or not (1 <= int(m) <= 5):
        raise ValueError(f'coef({coef})가 보기 범위(unit*1..5)를 벗어났습니다.')
    return int(m)


def _fmt_e_multiple(expr, x0):
    """coef*e^{2*x0} 꼴의 sympy 식을 'coef*e^(2x0)' 문자열로 보기 좋게 표시."""
    E0 = exp(2 * sp.nsimplify(x0))
    coef = simplify(expr / E0)
    return f"{coef}e^({2*sp.nsimplify(x0)})" if 2 * sp.nsimplify(x0) != 1 else f"{coef}e"


def statement(prm):
    k, x0, v = prm['k'], prm['x0'], prm['v']
    opts = ' '.join(
        f"{chr(9312 + i)} {_fmt_e_multiple(c, x0)}" for i, c in enumerate(choices(prm))
    )
    return (
        f"실수 전체의 집합에서 미분가능한 함수 f(x)가 다음 조건을 만족시킨다.\n"
        f"(가) x > 0일 때, f(x) = axe^(2x) + bx^2\n"
        f"(나) x_1 < x_2 < 0인 임의의 두 실수 x_1, x_2에 대하여\n"
        f"     f(x_2) - f(x_1) = {k}x_2 - {k}x_1\n"
        f"f({x0}) = {v}e^({2*sp.nsimplify(x0)})일 때, f'({x0})의 값은? "
        f"(단, a, b는 상수이다.)\n{opts}"
    )


# 원문제 보기(2e, 4e, 6e, 8e, 10e)와 유도된 보기가 같은지 고정
assert choices(PARAMS) == [2 * sp.E, 4 * sp.E, 6 * sp.E, 8 * sp.E, 10 * sp.E]
assert value(PARAMS) == 8 * sp.E

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
