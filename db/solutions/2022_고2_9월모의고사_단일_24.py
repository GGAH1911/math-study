import math
a = math.log(2) / math.log(5)
b = math.log(2) / math.log(7)
ab_ratio = a / b
result = 25 ** ab_ratio
if abs(result - 49) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')