import math
sqrt_2 = math.sqrt(2)
inner = 3 ** sqrt_2
sqrt_inner = inner ** 0.5
result = sqrt_inner ** sqrt_2
if abs(result - 3.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')