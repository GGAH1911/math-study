import sympy as sp
x = sp.Symbol('x')
curve = sp.Rational(3,1)/(x-1)
line = -x + 5
area = sp.integrate(line - curve, (x, 2, 4))
expected = 4 - 3*sp.ln(3)
if sp.simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}, expected={expected}')