from sympy import symbols, sqrt, solve, simplify, nsimplify, Rational
from sympy.geometry import Point, Ellipse
import math

CANDIDATE = 396

# ============= 문제 조건 인코딩 =============
# C_1의 초점: F(0, 6), F'(0, -6)
F = Point(0, 6)
F_prime = Point(0, -6)
c_1 = 6  # 초점까지의 거리

# C_1의 타원: 초점이 y축 위이므로 a_1 > b_1
# c_1 = 6이므로 a_1^2 - b_1^2 = 36

a_1 = symbols('a_1', positive=True, real=True)
b_1_sq = a_1**2 - 36  # b_1^2 = a_1^2 - 36

# y=6인 직선과 C_1의 교점
# 타원 방정식: x^2/b_1^2 + y^2/a_1^2 = 1
# y=6일 때: x^2/b_1^2 + 36/a_1^2 = 1
# x^2 = b_1^2 * (1 - 36/a_1^2) = b_1^2 * (a_1^2 - 36) / a_1^2 = b_1^4 / a_1^2
# 제1사분면: P = (b_1^2/a_1, 6)

P_x = b_1_sq / a_1
P = Point(P_x, 6)

# Q: 선분 PF'과 x축의 교점
# P = (b_1^2/a_1, 6), F' = (0, -6)
# 직선 PF': (y - (-6)) = (6 - (-6))/(b_1^2/a_1 - 0) * (x - 0)
# (y + 6) = 12*a_1/b_1^2 * x
# y=0: 6 = 12*a_1/b_1^2 * x_Q
# x_Q = 6*b_1^2 / (12*a_1) = b_1^2 / (2*a_1)

Q_x = b_1_sq / (2*a_1)
Q = Point(Q_x, 0)

# C_2의 초점: P, F
# Q는 C_2의 "꼭짓점" (단축 끝점 또는 장축 끝점)
# P = (b_1^2/a_1, 6), F = (0, 6)
# P, F의 중점 = (b_1^2/(2*a_1), 6) = (Q_x, 6)
# 초점들이 y=6 위에 있고 중점의 x좌표 = Q_x이므로
# C_2의 중심 = (b_1^2/(2*a_1), 6)
# 초점 사이 거리 = |P_x - 0| = b_1^2/a_1
# 따라서 c_2 = b_1^2/(2*a_1)

c_2 = b_1_sq / (2*a_1)

# Q = (b_1^2/(2*a_1), 0)이 C_2의 꼭짓점이고
# C_2의 중심 = (b_1^2/(2*a_1), 6)이므로
# Q에서 중심까지의 거리 = 6
# 이는 단축 끝점 → b_2 = 6

b_2 = 6

# C_2: a_2^2 = b_2^2 + c_2^2 = 36 + (b_1^2/(2*a_1))^2
a_2_sq = 36 + c_2**2
a_2_sq = simplify(a_2_sq)

# a_2_sq = 36 + b_1^4/(4*a_1^2)
#        = 36 + (a_1^2-36)^2/(4*a_1^2)
#        = (144*a_1^2 + (a_1^2-36)^2) / (4*a_1^2)
#        = (144*a_1^2 + a_1^4 - 72*a_1^2 + 1296) / (4*a_1^2)
#        = (a_1^4 + 72*a_1^2 + 1296) / (4*a_1^2)
#        = ((a_1^2 + 36)^2) / (4*a_1^2)

a_2_sq_expanded = ((a_1**2 + 36)**2) / (4*a_1**2)
a_2 = (a_1**2 + 36) / (2*a_1)

# ============= 핵심 조건: \overline{F'R} - \overline{PR} = 7*sqrt(2) =============
# R은 C_1, C_2의 교점
# C_1 위의 점: F'R + FR = 2*a_1
# C_2 위의 점: PR + FR = 2*a_2
# 따라서: F'R = 2*a_1 - FR, PR = 2*a_2 - FR
# F'R - PR = (2*a_1 - FR) - (2*a_2 - FR) = 2*a_1 - 2*a_2 = 2*(a_1 - a_2)

# 조건: 2*(a_1 - a_2) = 7*sqrt(2)
# a_1 - a_2 = 7*sqrt(2)/2

condition = 2*(a_1 - a_2) - 7*sqrt(2)
condition = simplify(condition)

# a_1 - a_2 = a_1 - (a_1^2 + 36)/(2*a_1)
#           = (2*a_1^2 - a_1^2 - 36) / (2*a_1)
#           = (a_1^2 - 36) / (2*a_1)
#           = b_1^2 / (2*a_1)

a_1_minus_a_2 = (a_1**2 - 36) / (2*a_1)

# 조건: (a_1^2 - 36) / (2*a_1) = 7*sqrt(2) / 2
# a_1^2 - 36 = 7*sqrt(2)*a_1
# a_1^2 - 7*sqrt(2)*a_1 - 36 = 0

quadratic_eq = a_1**2 - 7*sqrt(2)*a_1 - 36
a_1_solutions = solve(quadratic_eq, a_1)

# a_1은 양수
a_1_value = [sol for sol in a_1_solutions if sol > 0][0]
a_1_value = simplify(a_1_value)

# a_1 = 9*sqrt(2) 확인
assert simplify(a_1_value - 9*sqrt(2)) == 0, f"a_1 값 오류: {a_1_value}"

# b_1^2 = a_1^2 - 36
b_1_sq_value = a_1_value**2 - 36
b_1_sq_value = simplify(b_1_sq_value)
# b_1^2 = 162 - 36 = 126
assert b_1_sq_value == 126, f"b_1^2 값 오류: {b_1_sq_value}"

# a_2 = (a_1^2 + 36) / (2*a_1)
a_2_value = (a_1_value**2 + 36) / (2*a_1_value)
a_2_value = simplify(a_2_value)
# a_2 = (162 + 36) / (18*sqrt(2)) = 198 / (18*sqrt(2)) = 11 / sqrt(2) = 11*sqrt(2)/2
assert simplify(a_2_value - 11*sqrt(2)/2) == 0, f"a_2 값 오류: {a_2_value}"

# ============= 최종 답: 장축 길이의 곱 =============
# C_1의 장축 길이 = 2*a_1
# C_2의 장축 길이 = 2*a_2
# 곱 = 2*a_1 * 2*a_2 = 4*a_1*a_2

major_axis_product = 4 * a_1_value * a_2_value
major_axis_product = simplify(major_axis_product)

# 계산: 4 * 9*sqrt(2) * 11*sqrt(2)/2 = 4 * 9 * 11 * 2 / 2 = 4 * 9 * 11 = 396
expected_product = 4 * 9 * sqrt(2) * 11*sqrt(2) / 2
expected_product = simplify(expected_product)

# 검증
if major_axis_product == CANDIDATE == expected_product == 396:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: major_axis_product={major_axis_product}, CANDIDATE={CANDIDATE}, expected={expected_product}")