import math
from math import sqrt, cos, sin, pi

# 주어진 조건
AB = 3
AC = 1
angle_BAC = pi / 3

# BC의 길이 (코사인 법칙)
BC_squared = AB**2 + AC**2 - 2*AB*AC*cos(angle_BAC)
BC = sqrt(BC_squared)
assert abs(BC - sqrt(7)) < 1e-10, f"BC = {BC}, expected {sqrt(7)}"

# 각의 이등분선 정리: BP:PC = AB:AC = 3:1
# PC = BC/4
PC = BC / 4
assert abs(PC - sqrt(7)/4) < 1e-10, f"PC = {PC}, expected {sqrt(7)/4}"

# 각의 이등분선이므로 angle_PAC = angle_BAC / 2
angle_PAC = angle_BAC / 2
assert abs(angle_PAC - pi/6) < 1e-10, f"angle_PAC = {angle_PAC}, expected {pi/6}"

# 정현법칙: 2R = PC / sin(angle_PAC)
two_R = PC / sin(angle_PAC)
R = two_R / 2
assert abs(R - sqrt(7)/4) < 1e-10, f"R = {R}, expected {sqrt(7)/4}"

# 외접원의 넓이
area = pi * R**2
expected_area = 7 * pi / 16
assert abs(area - expected_area) < 1e-10, f"Area = {area}, expected {expected_area}"

print('VERIFY_PASS')