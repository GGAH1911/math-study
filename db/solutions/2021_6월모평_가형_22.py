from sympy import symbols, expand
x = symbols('x')
result = expand((1 + 2*x)**4)
coeff_x2 = result.as_coefficients_dict()[x**2]
if coeff_x2 == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')