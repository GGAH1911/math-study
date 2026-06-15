import numpy as np
from scipy.integrate import odeint

def f_system(y, x):
    f, F = y
    return [-2*f*F, f]

y0 = [1.0, 0.0]
x = np.linspace(-1, 2, 2000)
solution = odeint(f_system, y0, x)

f_vals = solution[:, 0]
F_vals = solution[:, 1]

# 불변식 검증
invariant_check = np.allclose(f_vals + F_vals**2, 1.0, atol=1e-6)

# ㄱ: x > 0에서 감소
idx_pos = x > 0
f_pos = f_vals[idx_pos]
f_decreasing = np.all(np.diff(f_pos) <= 1e-5)

# ㄴ: 최댓값이 1
f_max_is_one = np.isclose(np.max(f_vals), 1.0, atol=1e-6)

# ㄷ: f(1) + F(1)^2 = 1
idx_1 = np.argmin(np.abs(x - 1.0))
dgamma_check = np.isclose(f_vals[idx_1] + F_vals[idx_1]**2, 1.0, atol=1e-6)

if invariant_check and f_decreasing and f_max_is_one and dgamma_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')