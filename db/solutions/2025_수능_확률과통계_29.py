import numpy as np
from scipy import stats

# 구한 값
m1, sigma1 = 20, 5
m2, sigma2 = 10, 5

# 조건 1 검증: P(X ≤ x) = P(X ≥ 40-x)
# x=25일 때 테스트
x_test = 25
X = stats.norm(m1, sigma1)
P_left = X.cdf(x_test)
P_right = 1 - X.cdf(40 - x_test)
print(f'Condition 1 check: P(X ≤ {x_test}) = {P_left:.6f}, P(X ≥ {40-x_test}) = {P_right:.6f}')
assert abs(P_left - P_right) < 1e-10

# 조건 2 검증: P(Y ≤ x) = P(X ≤ x+10)
Y = stats.norm(m2, sigma2)
P_Y = Y.cdf(x_test)
P_X_shifted = X.cdf(x_test + 10)
print(f'Condition 2 check: P(Y ≤ {x_test}) = {P_Y:.6f}, P(X ≤ {x_test+10}) = {P_X_shifted:.6f}')
assert abs(P_Y - P_X_shifted) < 1e-10

# 조건 3 검증: P(15 ≤ X ≤ 20) + P(15 ≤ Y ≤ 20) = 0.4772
P_X_range = X.cdf(20) - X.cdf(15)
P_Y_range = Y.cdf(20) - Y.cdf(15)
total_prob = P_X_range + P_Y_range
print(f'P(15 ≤ X ≤ 20) = {P_X_range:.4f}')
print(f'P(15 ≤ Y ≤ 20) = {P_Y_range:.4f}')
print(f'Total = {total_prob:.4f}')
assert abs(total_prob - 0.4772) < 0.0001

print('VERIFY_PASS')