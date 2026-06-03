from math import erf, sqrt

# 원 문제: X ~ N(mu=68, sigma=10), P(55 <= X <= 78)
mu, sigma = 68.0, 10.0

def Phi(x):
    # 표준정규분포 CDF
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def P_interval(a, b):
    za = (a - mu) / sigma
    zb = (b - mu) / sigma
    return Phi(zb) - Phi(za)

# 문제에서 제공된 표 값 (z=1.0,1.1,1.2,1.3)을 이용한 정답
table = {1.0: 0.3413, 1.1: 0.3643, 1.2: 0.3849, 1.3: 0.4032}
expected = table[1.3] + table[1.0]  # P(0<=Z<=1.3)+P(0<=Z<=1.0)

# 정밀 계산과 표 기반 계산이 일치(반올림 오차 내)하고
# 후보 ② 0.7445 와 일치하는지 확인
ans = 0.7445
prob_exact = P_interval(55, 78)

if abs(expected - ans) < 1e-9 and abs(prob_exact - ans) < 5e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
