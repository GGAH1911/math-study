import math

# 원래 식: (sqrt(2))^(1 + log_2(3))
log2_3 = math.log(3) / math.log(2)
exponent = 1 + log2_3

# 계산
result = (math.sqrt(2)) ** exponent

# 검증: sqrt(6)
expected = math.sqrt(6)

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')