import math
import numpy as np

def f(x):
    return math.sin((math.pi/4) * x)

def check_inequality(x):
    left = f(2 + x) * f(2 - x)
    return left < 0.25

valid_naturals = []
for x in range(1, 16):
    if check_inequality(x):
        valid_naturals.append(x)

total = sum(valid_naturals)
expected = 32

if total == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}, expected {expected}')