from sympy import symbols, expand, sqrt, Poly
a = sqrt(2)
x = symbols('x')
expr = (a*x**2 + 1)**6
expanded = expand(expr)
poly = Poly(expanded, x)
coeff_x4 = poly.nth(4)
print(f'Coefficient of x^4: {coeff_x4}')
if coeff_x4 == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')