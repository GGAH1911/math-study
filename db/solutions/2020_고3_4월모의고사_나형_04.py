from sympy import symbols, integrate

x = symbols('x')
result = integrate(3*x**2 + 2, (x, 0, 1))

if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')