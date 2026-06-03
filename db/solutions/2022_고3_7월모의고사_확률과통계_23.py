from sympy import symbols, expand, binomial
x = symbols('x')
expr = (4*x + 1)**6
expanded = expand(expr)
coeff_x1 = expanded.coeff(x, 1)
if coeff_x1 == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')