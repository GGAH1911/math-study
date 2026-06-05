import sympy as sp

x = sp.symbols('x', real=True)
a = -3
assert a < 3
# f(x) quadratic, leading coeff 1
f = (x + 3) * (x - 3)
assert sp.Poly(sp.expand(f), x).LC() == 1
assert sp.degree(sp.expand(f), x) == 2

# f(4) check
assert int(f.subs(x, 4)) == 7

# Build g(x) = |(x-a) f(x)| numerically
def gn(t):
    return abs((t - a) * (t + 3) * (t - 3))

# 1) Local max value = 32 at critical point x = 2 + a/3 = 1
crit = 2 + a/3.0
assert abs(gn(crit) - 32) < 1e-12

# Verify it's a strict local max
for d in [1e-4, 1e-3, 1e-2, 1e-1]:
    assert gn(crit) > gn(crit - d)
    assert gn(crit) > gn(crit + d)

# 2) Non-differentiable AT x = 3
eps = 1e-7
left  = (gn(3) - gn(3 - eps)) / eps
right = (gn(3 + eps) - gn(3)) / eps
assert abs(left - right) > 1.0  # kink: derivatives differ

# 3) Differentiable at x = -3 (the other zero of (x-a)f(x))
left2  = (gn(-3) - gn(-3 - eps)) / eps
right2 = (gn(-3 + eps) - gn(-3)) / eps
assert abs(left2 - right2) < 1e-3

# 4) Differentiable at all other zeros / sample points (no other kinks)
# Sweep and find points where left/right derivatives diverge
import math
found_kinks = []
for k in range(-100, 101):
    t = k * 0.1
    if abs(t - 3) < 1e-9: continue
    L = (gn(t) - gn(t - eps)) / eps
    R = (gn(t + eps) - gn(t)) / eps
    if abs(L - R) > 1e-2 and abs(L) < 1e6 and abs(R) < 1e6:
        found_kinks.append(t)
assert len(found_kinks) == 0, f'unexpected kinks: {found_kinks}'

print('VERIFY_PASS')
