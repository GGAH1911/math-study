from fractions import Fraction
import math

# 주어진 조건
r = 4
theta = (2/3) * math.pi

# 부채꼴 넓이 공식 (라디안)
area = (1/2) * r**2 * theta

# 기댓값: 16π/3
expected = (16/3) * math.pi

if abs(area - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')