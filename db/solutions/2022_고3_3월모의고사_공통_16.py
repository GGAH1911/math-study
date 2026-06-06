import math
log2_72 = math.log(72, 2)
log2_sqrt6_over_2 = math.log(math.sqrt(6)/2, 2)
result = log2_72 - 4*log2_sqrt6_over_2
if abs(result - 5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')