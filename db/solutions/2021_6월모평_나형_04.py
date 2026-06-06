from sympy import symbols, limit
x = symbols('x')
f = (3*x**2 - 6*x)/(x - 2)
result = limit(f, x, 2)
print('VERIFY_PASS' if result == 6 else 'VERIFY_FAIL')