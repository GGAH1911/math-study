import math

# 원래 식: log_2(100) - 2*log_2(5)
value1 = math.log2(100)
value2 = 2 * math.log2(5)
result = value1 - value2

expected_answer = 2

if abs(result - expected_answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')