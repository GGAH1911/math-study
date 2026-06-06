import math
log2_sqrt2 = math.log2(math.sqrt(2))
log2_2sqrt2 = math.log2(2 * math.sqrt(2))
result = log2_sqrt2 + log2_2sqrt2
if abs(result - 2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')