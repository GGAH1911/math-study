import sympy as sp
import numpy as np

x = sp.Symbol('x', real=True)
d = -9
k = 10
f_expr = -2*x**3 + 6*x + d  # claimed f(x)
fp_expr = sp.diff(f_expr, x)

# (1) f'(0) = 6
assert sp.simplify(fp_expr.subs(x, 0) - 6) == 0

# (2) k + f(1/2) = 15/4
result = k + f_expr.subs(x, sp.Rational(1, 2))
assert result == sp.Rational(15, 4), f'k+f(1/2)={result}'

# (3) Condition (가): continuity at x=1 ensures right-limit is finite
assert sp.simplify(2*f_expr.subs(x, 1) + k) == 0

# Check right derivative <= 0 at sample points
def right_deriv(a):
    if a < -1 or a > 1:
        return -6*a**2 + 6        # = f'(a)
    if a == -1:
        return -(-6*a**2 + 6)     # = -f'(-1)
    if a == 1:
        return -6*a**2 + 6        # right side uses f'(1)
    return -(-6*a**2 + 6)         # interior |a|<1: -f'(a)
for a in [-3.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 3.0]:
    assert right_deriv(a) <= 1e-12, f'right deriv at {a}: {right_deriv(a)}'

# (4) Condition (나): use the ORIGINAL piecewise g and count roots of g(x)=t numerically
def count_roots(t_val, tol=1e-6):
    # Outer pieces (|x|>1): -2x^3 + 6x + d + k - t = 0
    outer = np.roots([-2, 0, 6, d + k - t_val])
    sols = []
    for r in outer:
        if abs(r.imag) < tol:
            xv = r.real
            if xv < -1 - tol or xv > 1 + tol:
                sols.append(xv)
    # Middle piece (|x|<=1): 2x^3 - 6x - d - t = 0
    mid = np.roots([2, 0, -6, -d - t_val])
    for r in mid:
        if abs(r.imag) < tol:
            xv = r.real
            if -1 - tol <= xv <= 1 + tol:
                sols.append(xv)
    sols.sort()
    distinct = []
    for s in sols:
        if not distinct or abs(s - distinct[-1]) > 1e-4:
            distinct.append(s)
    return len(distinct)

assert count_roots(13) == 2, f't=13 -> {count_roots(13)}'
assert count_roots(13.1) == 1, f't=13.1 -> {count_roots(13.1)}'
assert count_roots(12.9) == 2, f't=12.9 -> {count_roots(12.9)}'
assert count_roots(0) == 2, f't=0 -> {count_roots(0)}'
assert count_roots(-12 - d - 0.01) == 1
assert count_roots(-12 - d + 0.01) == 2

print('VERIFY_PASS')
