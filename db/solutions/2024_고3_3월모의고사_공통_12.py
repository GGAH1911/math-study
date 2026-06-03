import sympy as sp

a = -6
t = sp.Symbol('t')

# Verify f(2) = 0 (local min condition of g at x=2)
assert 3*2 + a == 0

# f for x<0
f_neg = 3*t**2 + 3*t + a

# Critical point of g in x<0 region: solve f_neg = 0
roots_neg = [r for r in sp.solve(f_neg, t) if r < 0]
assert roots_neg == [-2]

# Sign check: f>0 for x<-2, f<0 for -2<x<0 -> local max of g at x=-2
assert f_neg.subs(t, -3) > 0
assert f_neg.subs(t, -1) < 0

# Compute g(-2) = integral from -4 to -2 of f_neg dt
val = sp.integrate(f_neg, (t, -4, -2))

if val == 26:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
