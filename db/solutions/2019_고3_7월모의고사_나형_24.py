from sympy import symbols, expand, Poly

CANDIDATE = 90

x = symbols('x')
expr = (3*x + 1)**5
expanded = expand(expr)
poly = Poly(expanded, x)
coeff_x2 = poly.nth(2)

if coeff_x2 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')