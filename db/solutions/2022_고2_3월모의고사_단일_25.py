import sympy as sp
x, y = sp.symbols('x y', real=True)

# 원의 방정식: x^2 + y^2 + ax + by + c = 0
# 원의 중심(-1, 1), 반지름 1에서 a=2, b=-2, c=1
a, b_coef, c = 2, -2, 1

# 검증 1: 중심이 곡선 위에 있는가?
center_x, center_y = -1, 1
curve_y = center_x**2 - center_x - 1
assert curve_y == center_y, f"중심이 곡선 위에 없음: {curve_y} != {center_y}"

# 검증 2: 원의 중심과 반지름
# (x + 1)^2 + (y - 1)^2 = 1 형태인지 확인
original_eq = x**2 + y**2 + a*x + b_coef*y + c
# 표준형으로 변환: (x - h)^2 + (y - k)^2 = r^2
# x^2 + ax + ... = (x + a/2)^2 - (a/2)^2
h = -a/2
k = -b_coef/2
r_squared = h**2 + k**2 - c

assert h == -1 and k == 1 and r_squared == 1, f"중심 또는 반지름 오류: h={h}, k={k}, r^2={r_squared}"

# 검증 3: 반지름이 축까지의 거리와 일치
assert abs(k) == 1, f"y축까지 거리 오류: {abs(k)}"
assert abs(h) == 1, f"x축까지 거리 오류: {abs(h)}"

# 검증 4: 최종 답
answer = a + b_coef + c
assert answer == 1, f"답 계산 오류: {answer}"

print('VERIFY_PASS')