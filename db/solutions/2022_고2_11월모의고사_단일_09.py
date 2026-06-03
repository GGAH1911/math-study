import sympy as sp
from sympy import sqrt, limit, symbols, oo

x = symbols('x')
a = -2

# 검증: x=1 근처에서 극한 계산
expr = (sqrt(x**2 + 3) + a) / (x - 1)
f_at_1 = limit(expr, x, 1)

# 원래 조건 확인: (x-1)f(x) = sqrt(x^2+3) - 2
f_x = expr
original_eqn = (x - 1) * f_x - (sqrt(x**2 + 3) + a)
original_simplified = sp.simplify(original_eqn)

if f_at_1 == sp.Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')