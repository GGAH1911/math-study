"""2019 고3 3월모의고사 가형 23번 — 파라미터화 솔버.

원문제: 다항식 (2x + 1/2)^6 의 전개식에서 x^4 의 계수를 구하시오. (답 60)

수학 구조: 이항정리.
    (a*x + b)^n 의 전개식에서 x^power 항의 계수
    = C(n, power) * a^power * b^(n-power)   (일반항 T_{k+1} = C(n,k) (a x)^k b^(n-k), k=power)

파라미터로 뽑은 것: a(=x의 계수), b_num/b_den(=상수항 b, 분수 표현), n(=지수), power(=구하는 항의 차수).
  - a, b, n, power 각각을 바꾸면 계수 값이 달라진다 (아래에서 개별 확인).
"""
import sympy as sp


def value(prm):
    # (a*x + b)^n 의 전개식에서 x^power 의 계수를 sympy로 실제 전개하여 구한다.
    x = sp.symbols('x')
    a = prm['a']
    b = sp.Rational(prm['b_num'], prm['b_den'])
    n = prm['n']
    power = prm['power']
    if not (0 <= power <= n):
        raise ValueError('power는 0 이상 n 이하여야 함')
    expr = sp.expand((a * x + b) ** n)
    return expr.coeff(x, power)


def solve(prm):
    # 이 문제는 단답형(numeric)이므로 값 자체가 답.
    return value(prm)


def statement(prm):
    a = prm['a']
    b_num = prm['b_num']
    b_den = prm['b_den']
    n = prm['n']
    power = prm['power']
    if b_den == 1:
        b_str = f"{b_num}"
    else:
        b_str = f"\\frac{{{b_num}}}{{{b_den}}}"
    return (
        f"다항식 \\left( {a}x + {b_str} \\right)^{n} 의 전개식에서 "
        f"x^{power} 의 계수를 구하시오."
    )


CANDIDATE = 60
PARAMS = dict(a=2, b_num=1, b_den=2, n=6, power=4)

# 원문제 재현 확인
assert value(PARAMS) == CANDIDATE

# 각 파라미터가 실제로 답을 바꾸는지 개별 확인 (장식 파라미터 아님을 검증)
_base = value(PARAMS)
assert value({**PARAMS, 'a': 3}) != _base          # a 변경 → 값 변화
assert value({**PARAMS, 'b_num': 3}) != _base      # b 변경 → 값 변화
assert value({**PARAMS, 'n': 7}) != _base          # n 변경 → 값 변화
assert value({**PARAMS, 'power': 3}) != _base      # power 변경 → 값 변화


def solve_check():
    return solve(PARAMS)


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
