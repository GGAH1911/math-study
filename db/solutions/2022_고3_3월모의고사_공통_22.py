import numpy as np
from scipy.optimize import fsolve

# a = 1/2
a = 0.5

# g(x) = x(x - 2a)^2
def g(x):
    return x * (x - 2*a)**2

# f(x) piecewise
def f(x):
    if isinstance(x, np.ndarray):
        result = np.zeros_like(x, dtype=float)
        mask_pos = x >= 0
        mask_neg = x < 0
        result[mask_pos] = -4*x[mask_pos]**2 + 8*a*x[mask_pos]
        result[mask_neg] = 4*x[mask_neg]**2 - 8*a*x[mask_neg]
        return result
    else:
        if x >= 0:
            return -4*x**2 + 8*a*x
        else:
            return 4*x**2 - 8*a*x

# 조건 (가) 검증: x|g(x)| = ∫_{2a}^{x} (a-t)f(t) dt
from scipy.integrate import quad

def integrand(t):
    return (a - t) * f(t)

# 여러 점에서 검증
test_points = [-1, -0.5, 0, 0.5, 1, 1.5]
for x_test in test_points:
    lhs = x_test * abs(g(x_test))
    rhs, _ = quad(integrand, 2*a, x_test)
    if abs(lhs - rhs) < 1e-6:
        pass
    else:
        print(f'VERIFY_FAIL at x={x_test}: LHS={lhs}, RHS={rhs}')
        exit(1)

# 조건 (나) 검증: g(f(x)) = 0의 근이 정확히 4개
roots = []

# f(x) = 0의 근: x = 0, 2a
roots.extend([0, 2*a])

# f(x) = 2a의 근 (x >= 0): -4x^2 + 8ax = 2a -> 2x^2 - 4ax + a = 0
# Δ = 16a^2 - 8a = 0 for a = 1/2
# (2x - 1)^2 = 0 -> x = 1/2
roots.append(1/2)

# f(x) = 2a의 근 (x < 0): 4x^2 - 8ax = 2a -> 2x^2 - 4ax - a = 0
from numpy import sqrt
disc = 16*a**2 + 8*a
x_neg = (4*a - sqrt(disc)) / 4
if x_neg < 0:
    roots.append(x_neg)

if len(roots) != 4:
    print(f'VERIFY_FAIL: Expected 4 roots, got {len(roots)}')
    exit(1)

# 각 근에서 g(f(x)) = 0 확인
for root in roots:
    if abs(g(f(root))) > 1e-6:
        print(f'VERIFY_FAIL at root x={root}: g(f(x))={g(f(root))}')
        exit(1)

# 적분 계산: ∫_{-2a}^{2a} f(x) dx
integral_result, _ = quad(f, -2*a, 2*a)
expected = 4

if abs(integral_result - expected) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: Integral = {integral_result}, expected = {expected}')
