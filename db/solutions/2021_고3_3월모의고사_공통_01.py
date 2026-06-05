import math

# 원래 문제: log_8(16)
# log_a(b) = log(b)/log(a)
result = math.log(16) / math.log(8)
expected = 4/3

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')