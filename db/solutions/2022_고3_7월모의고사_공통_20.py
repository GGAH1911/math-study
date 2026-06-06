import sympy as sp
x = sp.Symbol('x')
f = 3*x**2 - 12*x + 9
integral = sp.integrate(sp.Abs(f), (x, 0, 3))
result = float(integral)
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')