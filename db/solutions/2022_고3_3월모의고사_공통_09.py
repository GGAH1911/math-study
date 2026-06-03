from sympy import symbols, integrate, Abs, solve, Eq, Rational
t, a = symbols('t a', real=True)
v = 3*t**2 + a*t
x = integrate(v, t)  # constant 0
# Condition: x(0) = x(6)
sol = solve(Eq(x.subs(t,0), x.subs(t,6)), a)
assert len(sol)==1
A = sol[0]
v_fixed = v.subs(a, A)
# Total distance from 0 to 6
roots = solve(v_fixed, t)
roots = [r for r in roots if r.is_real and 0 < r < 6]
breaks = sorted([0] + roots + [6])
from sympy import Piecewise, sign
total = 0
for i in range(len(breaks)-1):
    seg = integrate(v_fixed, (t, breaks[i], breaks[i+1]))
    total += Abs(seg)
print('VERIFY_PASS' if total == 64 else 'VERIFY_FAIL')
