import math

# 주어진 조건을 검증
a = 0.5  # 2^(-1)
b = 16   # 2^4

# 첫 번째 조건: log_sqrt(2) a + log_2 b = 2
log_sqrt2_a = math.log(a) / math.log(2**0.5)
log2_b = math.log(b) / math.log(2)
cond1 = log_sqrt2_a + log2_b

# 두 번째 조건: log_2 a + log_2 b^2 = 7
log2_a = math.log(a) / math.log(2)
log2_b2 = math.log(b**2) / math.log(2)
cond2 = log2_a + log2_b2

# 답 검증
product = a * b

if abs(cond1 - 2) < 1e-9 and abs(cond2 - 7) < 1e-9 and abs(product - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')