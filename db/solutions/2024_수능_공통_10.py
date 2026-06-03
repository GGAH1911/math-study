from sympy import *
t = symbols('t', real=True, positive=True)
v1 = t**2 - 6*t + 5
v2 = 2*t - 7
x1 = integrate(v1, (symbols('s'), 0, t))
x2 = integrate(v2, (symbols('s'), 0, t))
f = Abs(x1 - x2)
f_simplified = t/3 * (t-6)**2
f_prime = diff(f_simplified, t)
crit_pts = solve(f_prime, t)
a, b = 2, 6
dist_Q = integrate(Abs(v2), (t, 2, Rational(7,2))) + integrate(Abs(v2), (t, Rational(7,2), 6))
if dist_Q == Rational(17, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')