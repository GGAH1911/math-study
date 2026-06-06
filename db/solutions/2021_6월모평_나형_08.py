from sympy import symbols, expand, Poly
x = symbols('x')
expr = (1 + 2*x)**4
expanded = expand(expr)
poly = Poly(expanded, x)
coeff_x2 = poly.nth(2)
print('VERIFY_PASS' if coeff_x2 == 24 else f'VERIFY_FAIL: got {coeff_x2}')