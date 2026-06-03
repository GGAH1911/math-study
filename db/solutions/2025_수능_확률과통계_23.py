from sympy import symbols, expand, Poly
x = symbols('x')
poly = (x**3 + 2)**5
expanded = expand(poly)
coeff_x6 = Poly(expanded, x).nth(6)
if coeff_x6 == 80:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 80, got {coeff_x6}')