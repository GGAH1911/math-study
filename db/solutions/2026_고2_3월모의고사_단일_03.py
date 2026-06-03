import math
n, r = 6, 2
result = math.factorial(n) // math.factorial(n - r)
answer = 30
if result == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')