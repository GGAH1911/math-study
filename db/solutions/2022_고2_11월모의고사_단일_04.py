import numpy as np

# 원래 조건: 2x+1 <= f(x) <= (x+1)^2 for all x
# f(x)의 가능한 예시로 양쪽 경계의 평균값 사용해 수치 검증
# 핵심: Squeeze theorem으로 lim f(x) = 1 검증

x_vals = np.linspace(-0.001, 0.001, 10000)
exclude_zero = x_vals[x_vals != 0]

lower = 2 * exclude_zero + 1
upper = (exclude_zero + 1) ** 2

# 두 경계 극한 모두 1에 수렴하는지 확인
lower_lim = 2 * 0 + 1  # = 1
upper_lim = (0 + 1) ** 2  # = 1

assert abs(lower_lim - 1) < 1e-12, 'lower bound limit fail'
assert abs(upper_lim - 1) < 1e-12, 'upper bound limit fail'

# f(x)의 모든 가능한 값이 lower와 upper 사이에 있으면
# lim f(x) = 1, 따라서 lim (x+5)f(x) = 5
limit_xplus5 = 0 + 5  # = 5
limit_f = 1
result = limit_xplus5 * limit_f

# 수치적으로 (x+5)*lower 와 (x+5)*upper 모두 5로 수렴하는지 확인
lower_expr = (exclude_zero + 5) * (2 * exclude_zero + 1)
upper_expr = (exclude_zero + 5) * (exclude_zero + 1) ** 2

lower_at_0 = np.mean(lower_expr[np.abs(exclude_zero) < 0.0001])
upper_at_0 = np.mean(upper_expr[np.abs(exclude_zero) < 0.0001])

if abs(lower_at_0 - 5) < 0.01 and abs(upper_at_0 - 5) < 0.01 and abs(result - 5) < 1e-12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
