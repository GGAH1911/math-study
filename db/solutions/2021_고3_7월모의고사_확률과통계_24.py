from sympy import symbols, expand, Poly
x = symbols('x')
expr = (2*x + 1)**7
poly = Poly(expand(expr), x)
coeff = poly.nth(2)
print('VERIFY_PASS' if coeff == 84 else 'VERIFY_FAIL')