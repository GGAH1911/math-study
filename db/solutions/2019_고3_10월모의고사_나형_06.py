from sympy import symbols, integrate
x = symbols('x')
f1 = x**3 + 4*x**2
f2 = x**3 + x**2
result1 = integrate(f1, (x, -3, 3))
result2 = integrate(f2, (x, 3, -3))
total = result1 + result2
if total == 54:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')