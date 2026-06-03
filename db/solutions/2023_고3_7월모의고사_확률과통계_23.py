from sympy import symbols, expand, Poly
x = symbols('x')
polynomial = (x**2 + 2)**6
expanded = expand(polynomial)
poly = Poly(expanded, x)
coeff_x8 = poly.nth(8)
result = 'VERIFY_PASS' if coeff_x8 == 60 else f'VERIFY_FAIL: got {coeff_x8}'
print(result)