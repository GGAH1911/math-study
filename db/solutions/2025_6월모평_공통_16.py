import math
x = 7
lhs = math.log2(x+1) - 5
rhs = math.log(x-3) / math.log(0.5)
if abs(lhs - rhs) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')