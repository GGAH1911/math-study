from sympy import symbols, integrate
x = symbols('x')
result = integrate(2*x**3 + 3*x**2, (x, 0, 2))
print('VERIFY_PASS' if result == 16 else 'VERIFY_FAIL')