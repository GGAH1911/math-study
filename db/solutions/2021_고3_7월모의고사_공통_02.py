from sympy import symbols, integrate
x = symbols('x')
f = 2*x + 3
result = integrate(f, (x, 0, 1))
print('VERIFY_PASS' if result == 4 else 'VERIFY_FAIL')