import numpy as np

def f(n):
    value = (n - 3) * (n - 9)
    if n % 2 == 0:  # n is even
        if value > 0:
            return 1
    else:  # n is odd
        if value < 0:
            return 1
    return 0

result = sum(f(n) for n in range(2, 21))
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')