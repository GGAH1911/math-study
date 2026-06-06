import numpy as np
from scipy import stats

# 구한 값
a = 215
b = 70

# X의 분포
X_mean = 80
X_std = 5

# Y의 분포 (Y = a - 2X)
Y_mean = a - 2 * X_mean
Y_std = 2 * X_std

# 조건 1: P(b <= X <= 75) = 0.1359
cond1 = stats.norm.cdf(75, X_mean, X_std) - stats.norm.cdf(b, X_mean, X_std)
print(f'Condition 1: P({b} <= X <= 75) = {cond1:.4f} (expected 0.1359)')

# 조건 2: P(a-160 <= Y <= b) = 0.4332
cond2 = stats.norm.cdf(b, Y_mean, Y_std) - stats.norm.cdf(a - 160, Y_mean, Y_std)
print(f'Condition 2: P({a-160} <= Y <= {b}) = {cond2:.4f} (expected 0.4332)')

# 검증
if abs(cond1 - 0.1359) < 0.0001 and abs(cond2 - 0.4332) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')