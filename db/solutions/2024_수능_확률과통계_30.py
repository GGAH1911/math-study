from scipy import stats
import numpy as np

# 검증: t=0.2일 때 주어진 조건과 답이 맞는지 확인
t = 0.2
mean = 1
std = t

# 조건 확인: P(X <= 5t) >= 0.5
prob_condition = stats.norm.cdf(5*t, loc=mean, scale=std)
assert prob_condition >= 0.5, f'조건 실패: {prob_condition}'

# 최댓값 확인
lower_bound = t**2 - t + 1
upper_bound = t**2 + t + 1
prob_max = stats.norm.cdf(upper_bound, loc=mean, scale=std) - stats.norm.cdf(lower_bound, loc=mean, scale=std)

# 표준화 검증
z_lower = (lower_bound - mean) / std
z_upper = (upper_bound - mean) / std
print(f'z_lower = {z_lower}, z_upper = {z_upper}')

# 표의 값으로 계산
from scipy.special import ndtr
P_0_08 = ndtr(0.8) - 0.5  # P(0 <= Z <= 0.8)
P_0_12 = ndtr(1.2) - 0.5  # P(0 <= Z <= 1.2)
calculated_k = P_0_08 + P_0_12

print(f'P(0 <= Z <= 0.8) ≈ {P_0_08:.3f}, P(0 <= Z <= 1.2) ≈ {P_0_12:.3f}')
print(f'k = {calculated_k:.3f}, 1000k = {1000*calculated_k:.0f}')
print(f'prob_max = {prob_max:.3f}')

# 답 검증
if abs(calculated_k - 0.673) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')