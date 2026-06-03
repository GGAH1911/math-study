import math

def f(n):
    return math.sqrt(n*n + 9*n) - math.sqrt(n*n + 4*n)

vals = [f(10**k) for k in range(3, 8)]
target = 5/2
if all(abs(v - target) < 1e-3 for v in vals[-3:]) and abs(vals[-1] - target) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
