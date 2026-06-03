from sympy import symbols, expand
x = symbols('x')
f = -x**2 + 4*x + 3
# vertex x = -b/(2a) = -4/(2*(-1)) = 2
x_v = 2
y_v = f.subs(x, x_v)
print('VERIFY_PASS' if y_v == 7 else f'VERIFY_FAIL: y_v={y_v}')