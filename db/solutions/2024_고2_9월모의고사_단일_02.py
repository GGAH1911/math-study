from sympy import symbols, limit, oo, expand
x = symbols('x')
expr = ((2*x + 1)**2) / (x**2 + 4*x + 5)
result = limit(expr, x, oo)
if result == 4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')