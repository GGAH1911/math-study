import numpy as np
import sympy as sp

def f(x):
    return 2*x**3 - 8*x

def gpiece(x, m):
    if x < 0:
        return (-47.0/m)*x + 4.0/m**3
    else:
        return 2.0*m*x + 4.0/m**3

def h(x, m):
    return min(f(x), gpiece(x, m))

def candidates(m):
    c = {0.0}
    D1 = [2.0, 0.0, 47.0/m - 8.0, -4.0/m**3]   # region x<0 (f-g)
    D2 = [2.0, 0.0, -(8.0 + 2.0*m), -4.0/m**3]  # region x>=0 (f-g)
    for r in np.roots(D1):
        if abs(r.imag) < 1e-7 and r.real < -1e-9:
            c.add(float(r.real))
    for r in np.roots(D2):
        if abs(r.imag) < 1e-7 and r.real > 1e-9:
            c.add(float(r.real))
    return c

def count_nondiff(m, dx=1e-6, tol=1e-2):
    n = 0
    for x0 in candidates(m):
        dL = (h(x0, m) - h(x0 - dx, m)) / dx
        dR = (h(x0 + dx, m) - h(x0, m)) / dx
        if abs(dL - dR) > tol:
            n += 1
    return n

# statement g: m=-1, h(1/2) = -5
g_true = abs(h(0.5, -1.0) - (-5.0)) < 1e-9

# statement n: m=-1, number of non-diff points = 2
n_true = (count_nondiff(-1.0) == 2)

# statement d: max positive m with exactly 1 non-diff point is 6
m, x = sp.symbols('m x', real=True)
D1s = 2*x**3 + (sp.Integer(47)/m - 8)*x - 4/m**3
sols = sp.solve([D1s, sp.diff(D1s, x)], [x, m], dict=True)
pos_m = [s[m] for s in sols if s[m].is_real and s[m] > 0]
c_max = max(pos_m) if pos_m else None
d_true = (c_max == 6) and (count_nondiff(6.0) == 1) and (count_nondiff(6.2) == 3) and (count_nondiff(5.5) == 1)

if (g_true, n_true, d_true) == (True, True, True):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
