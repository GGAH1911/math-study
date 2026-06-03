from sympy import symbols, expand, binomial
x = symbols('x')
poly = expand((x**2 + 2)**6)
coeff = poly.coeff(x, 4)
if coeff == 240:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')