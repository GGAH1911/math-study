import math
from sympy import sqrt, symbols, simplify

# 주어진 조건
a = -4
b = 16
r = 8

# 검증 1: 점 (a, 4√3)이 원 x² + y² = r² 위에 있는가?
point_check = a**2 + (4*sqrt(3))**2
expected_r_squared = r**2
assert simplify(point_check - expected_r_squared) == 0, f'Point not on circle: {point_check} != {expected_r_squared}'

# 검증 2: 점 (a, 4√3)에서의 접선 ax + 4√3·y = r²이 x - √3·y + b = 0과 같은가?
# 접선: -4x + 4√3·y = 64
# 정리: -4x + 4√3·y - 64 = 0
# -4로 나누면: x - √3·y + 16 = 0
# 따라서 b = 16이 맞음

# 점에서 접선까지 거리 확인 (접선은 원에 접해야 함)
# 직선 ax + 4√3·y - r² = 0에서 원점까지의 거리 = r
distance = abs(-4*0 + 4*sqrt(3)*0 - 64) / sqrt((-4)**2 + (4*sqrt(3))**2)
expected_distance = r
assert simplify(distance - expected_distance) == 0, f'Distance check failed: {distance} != {expected_distance}'

print('VERIFY_PASS')