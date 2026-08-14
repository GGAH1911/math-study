import sympy as sp

# 원문제: y = (2x-7)/(x-3) 의 점근선 x=a, y=b 에 대해 ab 의 값
# 일반화된 수학 구조:
#   y = (m*x + n) / (x - r)   (m, n, r 은 유리수, 분자·분모가 서로 배수로
#   약분되지 않아야 진짜 y=(mx+n)/(x-r) 꼴의 점근선 문제가 된다)
#   - 수직 점근선: 분모 = 0  ->  x = r  =>  a = r
#   - 수평 점근선: x -> ±∞ 극한  ->  y = m (분자·분모 모두 1차이므로 최고차항 계수비)
#   - 구하는 값: a*b = r*m
# m, r 을 바꾸면 a*b 값이 실제로 바뀐다. n 은 함수가 진짜 (mx+n)/(x-r) 형태를
# 유지하도록(=degenerate 하지 않도록) 보장하는 조건에만 관여한다.

CANDIDATE = 6  # ★원문제 정답, 절대 변경 금지

PARAMS = dict(
    m=sp.Rational(2),   # 분자의 x 계수
    n=sp.Rational(-7),  # 분자의 상수항
    r=sp.Rational(3),   # 분모 x - r 의 r (수직 점근선 위치)
)


def solve(prm):
    m, n, r = sp.Rational(prm['m']), sp.Rational(prm['n']), sp.Rational(prm['r'])

    # 분자가 m*(x-r) 의 배수이면(n == -m*r) 함수가 y=m 인 상수함수로 퇴화되어
    # "두 점근선" 문제가 성립하지 않는다 -> 문제 조건 위반으로 예외.
    if sp.simplify(n + m * r) == 0:
        raise ValueError('분자가 분모의 배수가 되어 점근선이 존재하지 않는 퇴화된 함수입니다.')

    x = sp.Symbol('x')
    y = (m * x + n) / (x - r)

    # 수직 점근선: 분모 = 0
    vertical_asymptotes = sp.solve(sp.Eq(x - r, 0), x)
    if len(vertical_asymptotes) != 1:
        raise ValueError('수직 점근선이 유일하게 정해지지 않습니다.')
    a = vertical_asymptotes[0]

    # 수평 점근선: x -> ∞ 극한
    b = sp.limit(y, x, sp.oo)

    return sp.nsimplify(a * b)


def statement(prm):
    x = sp.Symbol('x')
    m, n, r = sp.Rational(prm['m']), sp.Rational(prm['n']), sp.Rational(prm['r'])
    num_str = sp.sstr(m * x + n)
    den_str = sp.sstr(x - r)
    return (
        f"함수 y=({num_str})/({den_str})의 그래프의 점근선은 두 직선 x=a, "
        f"y=b이다. 두 상수 a, b의 곱 ab의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
