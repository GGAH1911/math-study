import sympy as sp
from scipy.integrate import quad
import numpy as np

# f(x) 정의
def f(x):
    if x <= 3:
        return x / 12
    elif x <= 5:
        return 1/4
    else:
        return 3/2 - x/4

# k = 1/3 확인
integral_f, _ = quad(f, 0, 6)
k = 1/3
assert abs(integral_f - 1.0) < 1e-10, f'f 적분 오류: {integral_f}'

# g(x) = k - f(x)
def g(x):
    return k - f(x)

# g 적분 확인
integral_g, _ = quad(g, 0, 6)
assert abs(integral_g - 1.0) < 1e-10, f'g 적분 오류: {integral_g}'

# P(6k ≤ Y ≤ 15k) 계산
lower = 6 * k  # = 2
upper = 15 * k  # = 5
prob, _ = quad(g, lower, upper)

# 기약분수로 변환
from fractions import Fraction
frac = Fraction(prob).limit_denominator(1000)
print(f'P(2 ≤ Y ≤ 5) = {prob}')
print(f'분수: {frac}')
print(f'p = {frac.denominator}, q = {frac.numerator}')
print(f'p + q = {frac.denominator + frac.numerator}')

if frac == Fraction(7, 24):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')