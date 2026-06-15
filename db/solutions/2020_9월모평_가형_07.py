from sympy import symbols, expand
x = symbols('x')
poly = (2 + x)**4 * (1 + 3*x)**3
expanded = expand(poly)
coeff_x = expanded.as_coefficients_dict()[x]
if coeff_x == 176:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')