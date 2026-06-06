import sympy as sp
t = sp.Symbol('t', positive=True)
dx_dt = 1/t + 1
dy_dt = -3*t**2 + 3
dy_dx = dy_dt / dx_dt
dy_dx_simplified = sp.simplify(dy_dx)
print('dy/dx =', dy_dx_simplified)
derivative = sp.diff(dy_dx_simplified, t)
print('d(dy/dx)/dt =', derivative)
critical_point = sp.solve(derivative, t)
print('Critical point:', critical_point)
a = sp.Rational(1, 2)
dy_dx_at_a = dy_dx_simplified.subs(t, a)
second_deriv = sp.diff(derivative, t)
second_deriv_at_a = second_deriv.subs(t, a)
print('dy/dx at t=1/2:', dy_dx_at_a)
print('Second derivative at t=1/2:', second_deriv_at_a)
if second_deriv_at_a < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')