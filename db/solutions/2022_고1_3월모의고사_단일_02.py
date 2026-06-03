from sympy import symbols, expand
x = symbols('x')
result = expand((2*x - 1)*(x + 3))
coeff = result.as_coefficients_dict()[x]
if coeff == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')