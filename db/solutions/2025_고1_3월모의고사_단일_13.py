from sympy import Rational, pi, Eq, solve, symbols
x = symbols('x', positive=True)
R_cyl = 4
r_ball = 3
h_final = 8
V_water = pi * R_cyl**2 * x
V_ball = Rational(4,3) * pi * r_ball**3
V_total = pi * R_cyl**2 * h_final
eq = Eq(V_water + V_ball, V_total)
sol = solve(eq, x)
ans = Rational(23, 4)
if len(sol) == 1 and sol[0] == ans:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
