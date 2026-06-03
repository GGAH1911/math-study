import sympy as sp
from sympy import symbols, sqrt, solve, simplify

# 검증: a^2 = 12일 때, 조건을 만족하는지 확인
a_sq = 12

# k를 임의로 설정 (k > 0이면 모두 만족)
k_val = 2
b_sq = 3 * k_val**2  # = 12

# 1. 점 P(4, k)가 쌍곡선 위에 있는지 확인
hyperbola_check = 16 / a_sq - k_val**2 / b_sq
assert abs(hyperbola_check - 1) < 1e-10, f'P not on hyperbola: {hyperbola_check}'

# 2. 접선이 x축, y축과 만나는 점
Q_x = a_sq / 4  # = 3
R_y = -b_sq / k_val  # = -6

# 3. 삼각형 QOR의 넓이
A1 = 0.5 * Q_x * abs(R_y)  # = 0.5 * 3 * 6 = 9

# 4. 삼각형 PRS의 넓이
A2 = 2 * k_val  # = 4

# 5. 넓이 비 확인
area_ratio = A1 / A2  # = 9/4 = 2.25
assert abs(area_ratio - 9/4) < 1e-10, f'Area ratio incorrect: {area_ratio}'

# 6. 주축의 길이
a = sqrt(a_sq)
major_axis = 2 * a
assert simplify(major_axis - 4*sqrt(3)) == 0, f'Major axis incorrect: {major_axis}'

print('VERIFY_PASS')