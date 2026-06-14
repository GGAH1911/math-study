CANDIDATE = 6
from sympy import symbols, solve, diff, factor
x = symbols('x')
a_val = 9
b_val = 20
f = x**3 - 6*x**2 + a_val*x + 10
# Check f'(3) = 0 (differentiability condition)
fp = diff(f, x)
assert fp.subs(x, 3) == 0, 'f prime(3) != 0'
# Check continuity at x=3: b - f(3) == f(3)
assert b_val - f.subs(x,3) == f.subs(x,3), 'continuity fail'
# g'(x) for x<3 is -f'(x) = -3(x-1)(x-3)
# g'(x) for x>=3 is f'(x) = 3(x-1)(x-3)
# Critical points of g: x=1 (x<3 region) and x=3
# At x=1: g'<0 left, g'>0 right -> local min
g_at_1 = b_val - f.subs(x, 1)  # x=1 < 3, use b-f(x)
# Verify sign change at x=1
gp_left = -fp.subs(x, 0)   # x=0 < 1
gp_right = -fp.subs(x, 2)  # 1 < x=2 < 3
assert gp_left < 0, 'g should decrease before x=1'
assert gp_right > 0, 'g should increase after x=1'
# No sign change at x=3
gp_before3 = -fp.subs(x, 2.9)  # just before 3
gp_after3 = fp.subs(x, 3.1)    # just after 3
assert gp_before3 > 0 and gp_after3 > 0, 'x=3 should not be extremum'
if g_at_1 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')