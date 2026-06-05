import math
a = 4
b = 3
c_squared = a**2 + b**2
c = math.sqrt(c_squared)
asymptote_slope = b / a
expected_slope = 3 / 4
if abs(c - 5) < 1e-9 and abs(asymptote_slope - expected_slope) < 1e-9 and c_squared == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')