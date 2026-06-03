from sympy import symbols, expand, Poly
x = symbols('x')
expr = (2*x + 5)*(x - 1)**5
expanded = expand(expr)
poly = Poly(expanded, x)
coeff = poly.nth(3)
if coeff == 30:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {coeff}')