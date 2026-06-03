import sympy as sp
a_val = -1
x = sp.Symbol('x')
f = -sp.sqrt(x - a_val) + a_val + 2
# 점 (a, -a) 통과 확인
point_x, point_y = a_val, -a_val
val_at_point = f.subs(x, point_x)
assert val_at_point == point_y, f'점 통과 실패: {val_at_point} != {point_y}'
# 치역 확인: x >= -1 에서 최댓값 = 1, 최솟값 없음
max_val = f.subs(x, a_val)  # x = -1 일 때
assert max_val == 1, f'최댓값 확인 실패: {max_val}'
# x=100 대입해 y < 1 확인
import math
test_val = -math.sqrt(100 - a_val) + a_val + 2
assert test_val < 1, 'y <= 1 조건 위반'
print('VERIFY_PASS')