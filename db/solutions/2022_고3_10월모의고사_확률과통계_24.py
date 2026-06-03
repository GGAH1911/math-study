from sympy import symbols, expand, Poly
x = symbols('x')
expr = (x**2 + 1)*(x - 2)**5
poly = Poly(expand(expr), x)
coeff = poly.nth(6)
print('VERIFY_PASS' if coeff == -10 else f'VERIFY_FAIL: got {coeff}')