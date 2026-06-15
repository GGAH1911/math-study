import math

n = 5
a_count = 3
b_count = 2

result = math.factorial(n) // (math.factorial(a_count) * math.factorial(b_count))

if result == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')