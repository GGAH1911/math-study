import math

# 문제 원래 조건
X_bar = 67.27
sigma = 0.5
z = 1.96
upper_bound = 67.41

# 내 답
n = 49
a = 67.13

# 검증 1: 상한이 67.41인가?
margin = z * (sigma / math.sqrt(n))
calc_upper = X_bar + margin
calc_lower = X_bar - margin

upper_ok = abs(calc_upper - upper_bound) < 1e-9
lower_ok = abs(calc_lower - a) < 1e-9
result_ok = abs((n + a) - 116.13) < 1e-9

if upper_ok and lower_ok and result_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: upper={calc_upper}, lower={calc_lower}, n+a={n+a}')
