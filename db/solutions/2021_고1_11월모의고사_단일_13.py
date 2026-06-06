import sympy as sp

a, b = 1, 4

# 원 C의 중심과 반지름
center_x, center_y = a + 3, b - 8
radius = b

# x축과의 거리
dist_x_axis = abs(center_y)
assert dist_x_axis == radius, f'x축 접촉 실패: {dist_x_axis} != {radius}'

# y축과의 거리
dist_y_axis = abs(center_x)
assert dist_y_axis == radius, f'y축 접촉 실패: {dist_y_axis} != {radius}'

# 답 확인
answer = a + b
assert answer == 5, f'답 불일치: {answer} != 5'

print('VERIFY_PASS')