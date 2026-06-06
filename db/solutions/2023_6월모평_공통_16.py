import math
x = 6
result = math.log2(x + 2) + math.log2(x - 2)
if abs(result - 5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')