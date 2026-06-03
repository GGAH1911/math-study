import math
from numpy import isclose

# 답: a × OB = 2^(5/2)
a_times_OB = 2**(5/2)

# 역산: x_0 = 4, a = 2^(1/2)
x_0 = 4
a = 2**(1/2)

# 검증 1: a^(x_0) = 4
check1 = a**x_0
print(f'a^x_0 = {check1}, expected = 4')
assert isclose(check1, 4), f'Failed: a^x_0 should be 4'

# 검증 2: AB = BC = 2
AB = a**x_0 - 2
BC = 2
print(f'AB = {AB}, BC = {BC}')
assert isclose(AB, BC), f'Failed: AB should equal BC'

# 검증 3: 삼각형 AOC의 넓이 = 8
# A = (4, 2), O = (0, 0), C = (4, -2)
# 넓이 = 2 × 4 = 8
area = 2 * x_0
print(f'Area of AOC = {area}, expected = 8')
assert isclose(area, 8), f'Failed: Area should be 8'

# 검증 4: a × OB
OB = x_0
result = a * OB
expected = 2**(5/2)
print(f'a × OB = {result}, expected = {expected}')
assert isclose(result, expected), f'Failed: a × OB should be 2^(5/2)'

print('VERIFY_PASS')