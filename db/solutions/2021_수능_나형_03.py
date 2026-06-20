from sympy import symbols, limit, factor
x = symbols('x')
f = (x**2 + 2*x - 8) / (x - 2)
result = limit(f, x, 2)
print('VERIFY_PASS' if result == 6 else f'VERIFY_FAIL: got {result}')