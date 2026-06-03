from sympy import symbols, expand, Poly
x = symbols('x')
f = (x**2 + 1)**4 * (x**3 + 1)**3
expanded = expand(f)
poly = Poly(expanded, x)
coeff_x5 = poly.nth(5)
coeff_x6 = poly.nth(6)
if coeff_x5 == 12 and coeff_x6 == 7:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: x^5 coeff={coeff_x5} (expected 12), x^6 coeff={coeff_x6} (expected 7)')