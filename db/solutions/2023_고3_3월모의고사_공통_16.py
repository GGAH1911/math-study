import math
log2_96 = math.log2(96)
log6_2 = math.log(2) / math.log(6)
result = log2_96 - (1 / log6_2)
if abs(result - 4) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')