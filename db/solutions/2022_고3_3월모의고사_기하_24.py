import math
from sympy import sqrt, simplify

a_sq = 49
b_sq = 40

# 초점 확인
c_sq = a_sq - b_sq
assert c_sq == 9, f"초점 거리 제곱: {c_sq} != 9"

# 점 (0, 7) 타원 방정식에 대입
point_check = 0/b_sq + 49/a_sq
assert point_check == 1, f"점 (0,7) 확인: {point_check} != 1"

# 단축의 길이
b = math.sqrt(b_sq)
minor_axis = 2 * b
expected = 4 * math.sqrt(10)

assert abs(minor_axis - expected) < 1e-10, f"단축: {minor_axis} != {expected}"
print('VERIFY_PASS')