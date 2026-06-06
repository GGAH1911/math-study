import sympy as sp
x = sp.Symbol('x')
y = x**3 - 6*x**2 + 6
y_prime = sp.diff(y, x)
slope_at_1 = y_prime.subs(x, 1)
y_at_1 = y.subs(x, 1)
tangent_line = y_at_1 + slope_at_1 * (x - 1)
a_value = tangent_line.subs(x, 0)
if a_value == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')