import math
n, r = 6, 2
result = math.factorial(n) // math.factorial(n - r)
if result == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')