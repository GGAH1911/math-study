import math

# 주어진 조건
sigma = 2
n = 256
z_critical = 1.96

# 표본평균의 표준오차
se = sigma / math.sqrt(n)

# 오차한계
margin_of_error = z_critical * se

# 신뢰구간의 폭
width = 2 * margin_of_error

# 검증
if abs(width - 0.49) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')