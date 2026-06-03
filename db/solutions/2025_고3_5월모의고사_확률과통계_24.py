from sympy import symbols, expand, Rational
x = symbols('x')
expr = (x + Rational(1,2))**8
poly = expand(expr)
coeff = poly.coeff(x, 5)
print('VERIFY_PASS' if coeff == 7 else f'VERIFY_FAIL: got {coeff}')