from math import erf, sqrt

def Phi(x):
    return 0.5*(1+erf(x/sqrt(2)))

def P_ge(a, mu, s):
    return 1 - Phi((a-mu)/s)

def P_le(a, mu, s):
    return Phi((a-mu)/s)

def P_between(a, b, mu, s):
    return Phi((b-mu)/s) - Phi((a-mu)/s)

# 후보: sigma=2, mu는 (가)로부터 결정
# 조건 (가)로 mu 추정: 대칭성 mu=4
mu = 4.0
sigma = 2.0

cond_a = P_ge(1, mu, sigma) + P_ge(7, mu, sigma)
cond_b = P_between(2, 8, mu, sigma) + P_le(0, mu, sigma)
target_b = Phi(1)

if abs(cond_a - 1) < 1e-10 and abs(cond_b - target_b) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
