import numpy as np
from scipy import integrate

def f(x):
    if x <= 0:
        return 0
    return np.log(1 + x**4)**10

def g_value(x):
    if x <= 0:
        return 0
    result, _ = integrate.quad(lambda t: f(t) * f(1 - t), 0, min(x, 1))
    return result

# ㄱ 검증
assert abs(g_value(-1)) < 1e-10
assert abs(g_value(0)) < 1e-10

# ㄴ 검증
g_half = integrate.quad(lambda t: f(t) * f(1 - t), 0, 0.5)[0]
g_1 = integrate.quad(lambda t: f(t) * f(1 - t), 0, 1)[0]
assert np.isclose(g_1, 2 * g_half)

# ㄷ 검증
assert g_1 < 1

print('VERIFY_PASS')