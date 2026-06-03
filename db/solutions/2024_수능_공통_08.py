from sympy import *
x = symbols('x')
f = 3*x**3 + 3*x**2 + 3*x
# 원래 방정식 검증: x*f(x) - f(x) == 3x^4 - 3x
lhs = x*f - f
rhs = 3*x**4 - 3*x
assert expand(lhs - rhs) == 0, 'equation check FAIL'
# 적분 계산
result = integrate(f, (x, -2, 2))
if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
