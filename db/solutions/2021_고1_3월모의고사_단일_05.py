import math
from sympy import symbols, pi, solve, simplify

r = 2
h = 15/2

# 원기둥의 겉넓이 계산
surface_area = 2 * math.pi * r**2 + 2 * math.pi * r * h
expected = 38 * math.pi

if abs(surface_area - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')