from sympy import symbols, integrate

x = symbols('x')
f = x**3 + 3*x**2

result = integrate(f, (x, 2, -2))

if result == -16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)