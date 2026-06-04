import math
p = 0.1
sigma = 0.03
n = 100
calculated_sigma = math.sqrt((p * (1 - p)) / n)
if abs(calculated_sigma - sigma) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')