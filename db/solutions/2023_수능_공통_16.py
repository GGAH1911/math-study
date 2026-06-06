import math
x = 10
lhs = math.log2(3*x + 2)
rhs = 2 + math.log2(x - 2)
if abs(lhs - rhs) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')