from sympy import *
x = symbols('x')
f = Rational(1,3)*x**2 + 1
area = integrate(f, (x, 0, 3))
print('VERIFY_PASS' if area == 6 else f'VERIFY_FAIL got {area}')