import math
import numpy as np

# 원래 주어진 정의
log_3 = math.log10(3)
log_2 = math.log10(2)
a = log_3**2 - log_2**2

# b = log_6(10) = log(10) / log(6) = 1 / log(6)
b = 1 / math.log10(6)

# ab 계산
ab = a * b

# 10^(ab) 계산
result = 10**ab

# 정답 검증: 3/2 = 1.5
expected = 3/2

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')