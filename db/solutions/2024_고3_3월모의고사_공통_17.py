from sympy import symbols, integrate
x = symbols('x')
f1 = 3*x**2 - 2*x + 3
f2 = 2*x + 1
int1 = integrate(f1, (x, 0, 2))
int2 = integrate(f2, (x, 2, 0))
result = int1 - int2
if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')