from fractions import Fraction
import math

x = Fraction(3, 4)
a1 = x
a2 = 1 / (1 - x)

a = {1: float(a1)}

def compute(n, memo=a):
    if n in memo:
        return memo[n]
    if n % 2 == 0:
        result = float(a2) * compute(n // 2, memo) + 1
    else:
        result = float(a2) * compute((n - 1) // 2, memo) - 2
    memo[n] = result
    return result

for i in range(1, 16):
    compute(i)

a8 = compute(8)
a15 = compute(15)
diff = a8 - a15

if abs(diff - 63) < 1e-9:
    ratio = a8 / float(a1)
    if abs(ratio - 92) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')