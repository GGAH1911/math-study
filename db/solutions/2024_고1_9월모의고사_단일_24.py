import sympy as sp
x, m = sp.symbols('x m')
line = 2*x + 3
parabola = x**2 - 4*x + 12
eq = sp.Eq(line, parabola)
sol = sp.solve(eq, x)
if len(sol) == 1 and sol[0] == 3:
    x_touch = sol[0]
    y_touch_line = 2*x_touch + 3
    y_touch_para = x_touch**2 - 4*x_touch + 12
    if y_touch_line == y_touch_para == 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')