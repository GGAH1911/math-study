import math
from scipy import stats

# 매개변수
a = 4
n_trials = 19200
p = (3*a + 12) / 96

# E(X) 검증
expected_value = n_trials * p
print(f'E(X) = {expected_value}')
assert abs(expected_value - 4800) < 0.01, 'E(X) check failed'

# 분산 및 표준편차
variance = n_trials * p * (1 - p)
std_dev = math.sqrt(variance)
print(f'Var(X) = {variance}, σ = {std_dev}')

# P(X ≤ 4800 + 30*4) 계산
threshold = 4800 + 30*a
z_score = (threshold - expected_value) / std_dev
print(f'Z = {z_score}')

# 표준정규분포에서 누적확률
prob = stats.norm.cdf(z_score)
print(f'P(X ≤ {threshold}) = {prob}')

# 답
b = prob
ans = int(round(1000 * b))
print(f'b = {b}, 1000b = {ans}')

if ans == 977:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')