from sympy import symbols, expand, Poly
x = symbols('x')
result = expand((2*x + 1)**5)
poly = Poly(result, x)
coeff = poly.nth(2)
if coeff == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')