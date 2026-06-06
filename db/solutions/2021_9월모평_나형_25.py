import math
from sympy import sqrt, symbols, solve, simplify

# 좌표 설정
# A = (0, 0), B = (6, 0)
# C = (95/12, 5√215/12)
# D = (19/4, √215/4)

x_c = 95/12
y_c_sq = 5375/144
y_c = math.sqrt(y_c_sq)

# 검증
AC = math.sqrt(x_c**2 + y_c**2)
AB = 6

D_x = 3 * x_c / 5
D_y = 3 * y_c / 5

AD = math.sqrt(D_x**2 + D_y**2)
BD = math.sqrt((D_x - 6)**2 + D_y**2)

B_x, B_y = 6, 0
BC = math.sqrt((x_c - B_x)**2 + (y_c - B_y)**2)
BC_sq = (x_c - B_x)**2 + y_c**2

# 검증
assert abs(AB - 6) < 1e-10, f'AB 오류: {AB}'
assert abs(AC - 10) < 1e-10, f'AC 오류: {AC}'
assert abs(AD - 6) < 1e-10, f'AD 오류: {AD}'
assert abs(BD - math.sqrt(15)) < 1e-10, f'BD 오류: {BD}'
assert abs(BC_sq - 41) < 1e-10, f'BC² 오류: {BC_sq}'

print('VERIFY_PASS')