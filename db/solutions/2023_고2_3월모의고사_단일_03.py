import math
n, r = 5, 3
result = math.factorial(n) // math.factorial(n - r)
print('VERIFY_PASS' if result == 60 else 'VERIFY_FAIL')