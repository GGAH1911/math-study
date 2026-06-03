import numpy as np

p, q = 7, 24

def f(x):
    return 0.5*x**3 - 1.5*x**2 + 5

def g(x):
    if x < 0:
        return 0.5*p*x**2 + 0.5*q*x + 5
    return 5

# Continuity check at x=-2
assert abs(g(-2) - f(-2)) < 1e-9

def h(x):
    fv = f(x)
    if abs(fv) > 5 + 1e-12:
        return fv
    if abs(fv) < 5 - 1e-12:
        return g(x)
    return (np.sign(fv)*5 + g(x)) / 2

# Build h on a grid and count intersections with line
def count_intersections(m):
    # Use sign-change detection of h(x) - (m*x + 5) on fine grid
    # Region-wise exact counting:
    cnt = 0
    disc = 9 + 8*m
    sd = np.sqrt(disc)
    x_neg = (3 - sd)/2
    x_pos = (3 + sd)/2
    # x < -2: h = f, want f(x)=mx+5 => cubic root
    if x_neg < -2 - 1e-15:
        cnt += 1
    # x = -2 boundary
    if abs(-2*m + 5 - (-5)) < 1e-12:
        cnt += 1
    # -2 < x < 0: g(x) - line
    root2 = 2*(m - p - 5)/p
    if -2 + 1e-15 < root2 < -1e-15:
        cnt += 1
    # x = 0 always
    cnt += 1
    # x > 3: h = f
    if x_pos > 3 + 1e-15:
        cnt += 1
    return cnt

# Find k with lim a_n = 4
count_k = 0
ks = []
for k in range(1, 40):
    a_vals = [count_intersections(k - 1/2**n) for n in range(1, 25)]
    # eventually constant 4
    if all(a == 4 for a in a_vals[-15:]):
        count_k += 1
        ks.append(k)

h4 = h(4)
total = p + q + h4

ok = (count_k == 7) and (abs(h4 - 13) < 1e-9) and (total == 44)
if ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL count_k={count_k}, ks={ks}, h4={h4}, total={total}')
