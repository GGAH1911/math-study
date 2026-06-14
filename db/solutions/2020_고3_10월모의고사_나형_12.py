from scipy import stats
import numpy as np

CANDIDATE = 103

# 모집단 파라미터
mu = 104
sigma = 4
n = 4

# 표본평균의 표준편차
sigma_bar = sigma / np.sqrt(n)

# 표본평균이 a 이상 106 이하일 확률
prob = stats.norm.cdf((106 - mu) / sigma_bar) - stats.norm.cdf((CANDIDATE - mu) / sigma_bar)

# 문제에서 주어진 확률
target_prob = 0.5328

# 검증
if np.isclose(prob, target_prob, atol=0.0001):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')