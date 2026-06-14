from scipy import stats
import numpy as np

CANDIDATE = 0.1587

# X ~ N(m=10, sigma=4)
m = 10
sigma = 4

# 조건 검증
f_8 = stats.norm.pdf(8, m, sigma)
f_14 = stats.norm.pdf(14, m, sigma)
f_2 = stats.norm.pdf(2, m, sigma)
f_16 = stats.norm.pdf(16, m, sigma)

assert f_8 > f_14, f'f(8)={f_8:.6f} not > f(14)={f_14:.6f}'
assert f_2 < f_16, f'f(2)={f_2:.6f} not < f(16)={f_16:.6f}'

# P(X <= 6) 계산
prob_calculated = stats.norm.cdf(6, m, sigma)

# 표준화로 계산
z_value = (6 - m) / sigma  # (6 - 10) / 4 = -1
prob_from_table = 0.5 - 0.3413  # P(Z <= -1) = 0.5 - P(0 <= Z <= 1)

if np.isclose(CANDIDATE, prob_calculated, atol=0.0001):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')