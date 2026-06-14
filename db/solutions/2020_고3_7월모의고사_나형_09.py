from sympy import symbols, expand
x = symbols('x')
expr = (x**2 + 2/x)**6
expanded = expand(expr)
coeff_x6 = expanded.as_coefficients_dict()[x**6]
if coeff_x6 == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')