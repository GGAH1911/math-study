from sympy import symbols, integrate
x = symbols('x')
f = 6*x**2 - 2*x + 1
result = integrate(f, (x, 0, 2))
if result == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')