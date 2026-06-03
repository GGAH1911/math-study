from sympy import *
x = symbols('x')
# f(x) = 2x^2 - x 는 f(0)=0, f(1)=1, integral=1/6 를 만족하는 대표 예
f_expr = 2*x**2 - x
# -1 < x < 0: g = -f(x+1)+1
g_neg = -f_expr.subs(x, x+1) + 1
# 0 <= x <= 1: g = f(x)
g_mid = f_expr
# 1 < x <= 2: g = g(x-2) = -f(x-1)+1
g_hi = -f_expr.subs(x, x-1) + 1
# 각 조각 검증
I1 = integrate(g_neg, (x, -1, 0))
I2 = integrate(g_mid, (x, 0, 1))
I3 = integrate(g_hi, (x, 1, 2))
assert I1 == Rational(5,6), f'I1={I1}'
assert I2 == Rational(1,6), f'I2={I2}'
assert I3 == Rational(5,6), f'I3={I3}'
# int_{-3}^{2}: [-3,-1] 주기이동 = [-1,1], 그 다음 [-1,1], 마지막 [1,2]
result = (I1+I2) + (I1+I2) + I3
expected = Rational(17, 6)
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)