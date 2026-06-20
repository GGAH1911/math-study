from sympy import symbols, limit
x = symbols('x')
expr = (3*x**2 - 6*x) / (x - 2)
result = limit(expr, x, 2)
if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')