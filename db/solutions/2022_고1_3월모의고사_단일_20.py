import sympy as sp
a = sp.Rational(-4, 9)
b = sp.Rational(8, 3)
x_A, y_A = 3, 4
x_B, y_B = 0, sp.Rational(10, 3)

# 포물선: y = ax^2 + bx
# 극값점이 (3, 4)인지 확인
y_check = a * x_A**2 + b * x_A
assert y_check == y_A, f"극값값 검증 실패: {y_check} ≠ {y_A}"

# 극값점의 x좌표가 3인지 확인
x_extremum = -b / (2*a)
assert x_extremum == 3, f"극값점 x좌표 검증 실패: {x_extremum} ≠ 3"

# BH = 2 검증
t_0 = (sp.Rational(10,3) * y_A) / (9 + y_A**2)
H_x = 3 * t_0
H_y = y_A * t_0
BH_squared = H_x**2 + (H_y - y_B)**2
BH = sp.sqrt(BH_squared)
assert BH == 2, f"BH 검증 실패: {BH} ≠ 2"

# OA에 수직 확인
vec_BH = (H_x, H_y - y_B)
vec_OA = (x_A, y_A)
dot_product = vec_BH[0] * vec_OA[0] + vec_BH[1] * vec_OA[1]
assert dot_product == 0, f"수직성 검증 실패: {dot_product} ≠ 0"

print('VERIFY_PASS')