from sympy import symbols, diff, solve, simplify
a = symbols('a', positive=True, real=True)
x, y = symbols('x y', real=True)
ellipse = x**2/8 + y**2/(2*a**2) - 1
dy_dx = -diff(ellipse, x) / diff(ellipse, y)
slope_at_2a = dy_dx.subs([(x, 2), (y, a)])
equation = slope_at_2a + 3
sol = solve(equation, a)
if sol and sol[0] == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')