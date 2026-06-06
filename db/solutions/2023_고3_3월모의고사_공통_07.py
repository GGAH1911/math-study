CANDIDATE = 3

from fractions import Fraction
import sympy as sp

x = sp.Symbol('x')

# 원래 문제의 함수: y = |x^2 - 2x| + 1
# 구간 [0, 2]에서 x^2 - 2x = x(x - 2) <= 0이므로
# |x^2 - 2x| = -(x^2 - 2x) = 2x - x^2
# 따라서 y = -x^2 + 2x + 1

f = -x**2 + 2*x + 1

# 구간 [0, 2]에서 적분하여 넓이 계산
integral_result = sp.integrate(f, (x, 0, 2))

# 보기 값 정의
choices = {
    1: Fraction(8, 3),
    2: Fraction(3, 1),
    3: Fraction(10, 3),
    4: Fraction(11, 3),
    5: Fraction(4, 1)
}

# CANDIDATE번 보기의 값이 계산된 적분 결과와 같은지 확인
if integral_result == choices[CANDIDATE]:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")