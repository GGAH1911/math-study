import math
x = 7
term1 = math.log(x + 2, 3)
term2 = math.log(x - 4, 1/3)
result = term1 - term2
if abs(result - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')