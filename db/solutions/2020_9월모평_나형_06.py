from sympy import symbols, integrate
x = symbols('x')
f = 3*x**2 + 6*x
result = integrate(f, (x, 0, 2))
print('VERIFY_PASS' if result == 20 else f'VERIFY_FAIL: {result}')