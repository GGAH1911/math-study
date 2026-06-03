from sympy import symbols, expand, Poly
x = symbols('x')
poly = (x - 1)**6 * (2*x + 1)**7
expanded = expand(poly)
p = Poly(expanded, x)
coeff_x2 = p.nth(2)
result = 'VERIFY_PASS' if coeff_x2 == 15 else f'VERIFY_FAIL: got {coeff_x2}'
print(result)