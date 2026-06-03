import numpy as np

def tan_theta(t):
    m1 = np.cos(t)
    m2 = -1.0
    denom = 1.0 + m1 * m2
    if abs(denom) < 1e-15:
        return float('inf')
    return abs((m1 - m2) / denom)

def ratio(t):
    return tan_theta(t) / (np.pi - t)**2

# Numerical convergence check
test_s = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
ratios = [ratio(np.pi - s) for s in test_s]

limit_candidate = 1.0 / 4.0

# All ratios must converge to 1/4
all_close = all(abs(r - limit_candidate) < 1e-4 for r in ratios)

# Also verify the formula: tan(theta) = (1+cos t)/(1-cos t) matches direct formula
t_test = np.pi - 0.001
formula_val = (1 + np.cos(t_test)) / (1 - np.cos(t_test))
direct_val = tan_theta(t_test)
formula_ok = abs(formula_val - direct_val) < 1e-10

if all_close and formula_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('ratios:', ratios)
    print('expected:', limit_candidate)
