import math

# 원래 식: 32 × 2^(-3)
result = 32 * (2 ** (-3))
candidate = 4

if math.isclose(result, candidate):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')