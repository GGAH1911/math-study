from sympy import symbols, expand, Poly
x = symbols('x')
poly = (x + 4)**6 * (3*x + 2)
expanded = expand(poly)
coeff_x6 = Poly(expanded, x).nth(6)
if coeff_x6 == 74:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')