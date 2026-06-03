import math
x = 2 + 2*math.sqrt(3)
side1, side2, side3 = x, x+1, x+3
result = side1**2 + side2**2
result_expected = side3**2
if abs(result - result_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')