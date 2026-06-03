from math import comb, factorial
result = comb(5, 3) * factorial(3)
if result == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')