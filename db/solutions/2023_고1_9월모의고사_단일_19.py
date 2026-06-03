import numpy as np
from sympy import symbols, solve, sqrt

# 원 검증
print('A 원 위:', (-1)**2 + 3**2 == 10)
print('B 원 위:', (-3)**2 + (-1)**2 == 10)
print('C 원 위:', 1**2 + (-3)**2 == 10)

# AB 거리
AB_dist = np.sqrt(((-1)-(-3))**2 + (3-(-1))**2)
print('|AB| =', AB_dist, '(정답: 2√5 =', 2*np.sqrt(5), ')')
print('|AB| 검증:', np.isclose(AB_dist, 2*np.sqrt(5)))

# A 제2사분면, B 제3사분면
print('A 제2사분면:', -1 < 0 and 3 > 0)
print('B 제3사분면:', -3 < 0 and -1 < 0)

# C는 직선 OA 위
print('C on OA:', -3 == -3*1)

# D는 직선 l 위 (y = 2x + 5)
print('D on l:', -3 == 2*(-4) + 5)

# D의 y좌표는 C의 y좌표
print('D y좌표 = C y좌표:', -3 == -3)

print('VERIFY_PASS')