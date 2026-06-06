import numpy as np
from scipy.optimize import fsolve

# a = 3, b = 5
a, b = 3, 5

def f(x):
    if abs(x) > 1:
        return a + b/x
    elif -1 < x < 1:
        return x/2
    elif x == 1:
        return (a + b + 1)/3
    elif x == -1:
        return (a - b - 1)/3

# k = 3일 때 검증
m = 3
rhs = lambda x: 2*x - 2 + m

# 구간별 근 찾기
roots = []

# x > 1
coeffs = [2, m-5, -5]
roots_quad = np.roots(coeffs)
for r in roots_quad:
    if r.imag == 0 and r.real > 1:
        roots.append(float(r.real))

# x = 1
if abs(f(1) - rhs(1)) < 1e-10:
    roots.append(1.0)

# -1 < x < 1
x_int = 2*(2-m)/3
if -1 < x_int < 1 and abs(f(x_int) - rhs(x_int)) < 1e-10:
    roots.append(x_int)

# x = -1
if abs(f(-1) - rhs(-1)) < 1e-10:
    roots.append(-1.0)

# x < -1
for r in roots_quad:
    if r.imag == 0 and r.real < -1:
        roots.append(float(r.real))

c_k = len(roots)
if c_k == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')