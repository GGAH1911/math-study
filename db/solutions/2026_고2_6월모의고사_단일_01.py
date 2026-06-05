import math
result = 2**(2 - math.sqrt(2)) * 2**math.sqrt(2)
answer = 4
if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')