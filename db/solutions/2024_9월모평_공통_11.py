from sympy import symbols, integrate, solve, Abs, Rational
t = symbols('t', real=True)
v1 = 3*t**2 + 4*t - 7
xP = 1 + t**3 + 2*t**2 - 7*t
xQ = 8 + t**2 + 4*t
f = xP - xQ  # t^3+t^2-11t-7
# Check t=3 gives distance 4
dist_at_3 = abs(int(f.subs(t, 3)))
assert dist_at_3 == 4, f'distance at t=3 is {dist_at_3}, not 4'
# Check no earlier solution in (0,3): solve |f|=4
sol_neg = [s for s in solve(f + 4, t) if s >= 0]  # f=-4
sol_pos = [s for s in solve(f - 4, t) if s >= 0]  # f=+4
first_time = min(sol_neg + sol_pos)
assert first_time == 3, f'first time is {first_time}, not 3'
# Compute distance traveled by P: direction change at t=1
v1_sign_check = int(v1.subs(t, Rational(1,2)))  # should be < 0
assert v1_sign_check < 0
d1 = int(integrate(-v1, (t, 0, 1)))
d2 = int(integrate(v1, (t, 1, 3)))
total = d1 + d2
if total == 32:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: total={total}')