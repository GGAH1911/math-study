import math
from scipy.stats import binom, norm

# 파라미터
n = 16200
p = 2/3
required_position = 5700

# X ≤ X_max라는 조건에서 2X - 16200 ≤ 5700
# 2X ≤ 21900, X ≤ 10950
X_max = 10950

# 이항분포 파라미터
mu = n * p
sigma_sq = n * p * (1 - p)
sigma = math.sqrt(sigma_sq)

# 정규분포 근사
Z = (X_max - mu) / sigma

# 표준정규분포에서 확률 계산 (표의 값 이용)
# P(Z ≤ 2.5) = 0.5 + P(0 ≤ Z ≤ 2.5) = 0.5 + 0.494
prob_z_pos = 0.494
k = 0.5 + prob_z_pos

# 1000 × k
result = 1000 * k

# 검증
if abs(Z - 2.5) < 1e-10 and abs(k - 0.994) < 1e-10 and abs(result - 994) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')