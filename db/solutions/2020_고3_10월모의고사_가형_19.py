from fractions import Fraction
import math

def f(m):
    return Fraction((-1)**m, m+1)

def g(m):
    return math.factorial(m)

def h(m):
    return m + 1

result = (g(3) + h(3)) / f(4)
expected = 50

if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')