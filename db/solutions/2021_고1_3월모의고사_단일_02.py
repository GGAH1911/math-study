from sympy import symbols, expand
x = symbols('x')
original = 2*x*(3*x - 1) - x*(2*x + 3)
simplified = expand(original)
coeff_x2 = simplified.as_coefficients_dict()[x**2]
if coeff_x2 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')