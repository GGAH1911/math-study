from sympy import symbols, integrate
x = symbols('x')
f = x**2 - 2
result = integrate(f, (x, 0, 3))
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')