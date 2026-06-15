from sympy import symbols, diff, Rational

x, y = symbols('x y', real=True)
F = x**2 - 3*x*y + y**2 - x

dF_dx = diff(F, x)
dF_dy = diff(F, y)

slope = -dF_dx / dF_dy
slope_at_point = slope.subs([(x, 1), (y, 0)])

if slope_at_point == Rational(1, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')