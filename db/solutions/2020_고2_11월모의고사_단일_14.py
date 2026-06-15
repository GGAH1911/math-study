from sympy import *
r, arc_len = 4, pi
theta = arc_len / r
S = Rational(1, 2) * r**2 * theta
d = symbols('d', positive=True, real=True)
T = d * sqrt(2)
eq = Eq(S / T, pi)
sol = solve(eq, d)[0]
T_val = sol * sqrt(2)
ratio = S / T_val
if simplify(ratio - pi) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')