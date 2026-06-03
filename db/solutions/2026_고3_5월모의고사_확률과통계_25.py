from sympy import symbols, expand
x = symbols('x')
expr = (2*x**2 + 1)**4 * (x - 1/(2*x))
expanded = expand(expr)
coeff_x5 = expanded.as_coefficients_dict()[x**5]
if coeff_x5 == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')