from sympy import symbols, sqrt, solve, Eq, simplify, Rational
import math

CANDIDATE = 6

# ===== 좌표 설정 =====
# BC는 지름, 반지름 R = 2
B = (-2, 0)
C = (2, 0)

# 확인: BC = 4
assert math.sqrt((C[0] - B[0])**2 + (C[1] - B[1])**2) == 4, "BC must be 4"

# ===== 정현법칙으로 CE 구하기 =====
# CE / sin(∠CAE) = 2R = 4
# sin(∠CAE) = 1/4이므로 CE = 4 * (1/4) = 1
CE_target = 1

# ===== E 찾기 =====
# E는 원 위: x_E² + y_E² = 4
# CE = 1: (x_E - 2)² + y_E² = 1
# (x_E - 2)² + y_E² = 1 전개하면
# x_E² - 4*x_E + 4 + y_E² = 1
# 4 - 4*x_E + 4 = 1  (x_E² + y_E² = 4 사용)
# x_E = 7/4

x_E = Rational(7, 4)
y_E_sq = 4 - x_E**2  # = 15/16
y_E = -sqrt(y_E_sq)  # 검증된 풀이에서 음수

E = (x_E, y_E)

# 확인: E가 원 위
assert simplify(x_E**2 + y_E**2 - 4) == 0, "E not on circle"

# 확인: CE = 1
CE_calc = sqrt((x_E - 2)**2 + y_E**2)
assert simplify(CE_calc - 1) == 0, f"CE must be 1, got {CE_calc}"

# ===== D 찾기 =====
# DE = 4 (지름) → D와 E는 정반대
D = (-x_E, -y_E)

# 확인: D가 원 위
assert simplify(D[0]**2 + D[1]**2 - 4) == 0, "D not on circle"

# 확인: DE = 4
DE_calc = sqrt((E[0] - D[0])**2 + (E[1] - D[1])**2)
assert simplify(DE_calc - 4) == 0, "DE must be 4"

# ===== F 찾기 =====
# BF = CE = 1, F는 BC 위
# BC는 y=0 선분에서 B(-2,0)로부터 거리 1
F = (-1, 0)

assert math.sqrt((F[0] - B[0])**2 + (F[1] - B[1])**2) == 1, "BF must be 1"

# ===== A 찾기 =====
# F는 AD의 교점이므로, 직선 AD를 매개변수로
# P(s) = F + s*(D - F) = (-1, 0) + s*(-7/4 + 1, √15/4)
# P(s) = (-1, 0) + s*(-3/4, √15/4)
# A는 이 직선 위 원 위의 점: |P(s)|² = 4

s = symbols('s', real=True)
x_line = -1 - Rational(3, 4) * s
y_line = sqrt(Rational(15, 16)) * s

eq_circle = x_line**2 + y_line**2 - 4
s_solutions = solve(eq_circle, s)
# s = 1 (점 D) 또는 s = -2 (점 A)

s_A = -2
A_x = -1 - Rational(3, 4) * s_A
A_y = sqrt(Rational(15, 16)) * s_A

A = (A_x, A_y)

# 확인: A가 원 위
assert simplify(A_x**2 + A_y**2 - 4) == 0, "A not on circle"

# ===== AF 계산 =====
AF_sq = (A_x - F[0])**2 + (A_y - F[1])**2
AF_sq = simplify(AF_sq)

# k = √(AF²), k² = AF²
k_sq = AF_sq

# ===== sin(∠CAE) 검증 =====
# 벡터 AC, AE
AC_x, AC_y = C[0] - A_x, C[1] - A_y
AE_x, AE_y = E[0] - A_x, E[1] - A_y

# 길이
AC_len = sqrt(AC_x**2 + AC_y**2)
AE_len = sqrt(AE_x**2 + AE_y**2)

# cos(∠CAE)
dot = AC_x * AE_x + AC_y * AE_y
cos_CAE = simplify(dot / (AC_len * AE_len))

# sin(∠CAE)
sin_CAE = simplify(sqrt(1 - cos_CAE**2))

# 조건 검증
assert simplify(sin_CAE - Rational(1, 4)) == 0, f"sin(∠CAE) must be 1/4, got {sin_CAE}"

# ===== 최종 판정 =====
if k_sq == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")