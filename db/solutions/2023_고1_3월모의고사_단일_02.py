from sympy import symbols, expand
x = symbols('x')
expr = (2*x + 1)**2 - (2*x**2 + x - 1)
result = expand(expr)
linear_coeff = result.coeff(x, 1)
if linear_coeff == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')