from sympy import sqrt, symbols, solve, simplify, S, Rational

u = symbols('u', positive=True)
eq_u = u**2 - 288*u + 5184
u_solutions = solve(eq_u, u)

c_sq = None
for s in u_solutions:
    val = float(s)
    if 0 < val < 36:
        c_sq = s
        break

assert c_sq is not None, 'No valid c^2 found'

# Verify R is on ellipse
c_val = sqrt(c_sq)
Rx = c_val / 2
Ry = c_val * sqrt(S(3)) / 2
b_sq = 36 - c_sq
ellipse_lhs = Rx**2 / 36 + Ry**2 / b_sq
ellipse_ok = simplify(ellipse_lhs - 1) == 0

# Verify |OR|
OR = sqrt(c_sq)
target = 6*sqrt(S(3)) - 6
or_ok = simplify(OR - target) == 0

if ellipse_ok and or_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('ellipse_ok:', ellipse_ok, 'or_ok:', or_ok)
