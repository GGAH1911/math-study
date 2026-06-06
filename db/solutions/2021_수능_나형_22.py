from sympy import symbols, expand, binomial
x = symbols('x')
poly = (3*x + 1)**8
expanded = expand(poly)
coeff_x1 = expanded.coeff(x, 1)
print('VERIFY_PASS' if coeff_x1 == 24 else f'VERIFY_FAIL: got {coeff_x1}')