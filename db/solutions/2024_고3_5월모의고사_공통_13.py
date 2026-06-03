import math
import numpy as np

a, b = 1, 8

def f(x):
    if x <= a:
        return 2**(x+3) + b
    else:
        return 2**(-x+5) + 3*b

def solutions(t):
    sols = []
    # piece 1: 2^(x+3)+b = t, x<=a
    if t - b > 0:
        x1 = math.log2(t - b) - 3
        if x1 <= a + 1e-12:
            sols.append(('L', x1))
    # piece 2: 2^(-x+5)+3b = t, x>a
    if t - 3*b > 0:
        x2 = 5 - math.log2(t - 3*b)
        if x2 > a + 1e-12:
            sols.append(('R', x2))
    return sols

k_max_claim = 4*b + 8  # 40

# 1) k_max > b must hold
assert k_max_claim > b

# 2) For all t in (b, k_max), exactly one intersection
ts_in = np.linspace(b + 1e-5, k_max_claim - 1e-5, 5000)
inside_ok = all(len(solutions(t)) == 1 for t in ts_in)

# 3) Confirm solutions actually satisfy f(x)=t (round-trip)
roundtrip_ok = True
for t in ts_in[::200]:
    for _, x in solutions(t):
        if abs(f(x) - t) > 1e-9:
            roundtrip_ok = False

# 4) k_max is supremum: for t slightly above k_max, N(t) != 1
above = [len(solutions(k_max_claim + d)) for d in (1e-6, 1e-3, 0.1, 1.0)]
sup_ok = all(n != 1 for n in above)

# 5) At t = k_max boundary, N != 1 (boundary is excluded by '<' condition anyway)
boundary_n = len(solutions(k_max_claim))
boundary_ok = boundary_n != 1

if inside_ok and roundtrip_ok and sup_ok and boundary_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
