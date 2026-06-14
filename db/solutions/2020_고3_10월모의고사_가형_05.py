from sympy import *

CANDIDATE = Rational(1, 4)

# 검증: (2x + a/x)^7의 x^3 계수가 42인지 확인
x, a = symbols('x a')
expr = expand((2*x + a/x)**7)

# x^3의 계수 추출
coeff_x3 = expr.coeff(x, 3)

# a = CANDIDATE를 대입
coeff_value = coeff_x3.subs(a, CANDIDATE)

if coeff_value == 42:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')