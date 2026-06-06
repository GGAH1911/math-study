import math
result = math.log(2/3) / math.log(4) + math.log(24) / math.log(4)
expected = 2
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')