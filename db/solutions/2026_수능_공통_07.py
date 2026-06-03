from sympy import *
x = symbols('x')
f1 = x**2 + 3
f2 = -Rational(1,5)*x**2 + 3
area = integrate(f1 - f2, (x, 0, 2))
result = Rational(16,5)
print('VERIFY_PASS' if area == result else f'VERIFY_FAIL: got {area}')