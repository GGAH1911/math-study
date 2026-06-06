from sympy import symbols, cos, sin, Rational as Rat

CANDIDATE = 64

# 문제의 미지수와 변수
c, a, B = symbols('c a B', real=True, positive=True)

# ===== 문제의 주어진 조건 =====
# 조건: DB = DF = EG (= a라 놓음)
# 조건: AG = 3 × GC
# 조건: 삼각형 EGC의 넓이 = 8

# ===== 기하학적 분석으로부터 유도된 관계식 =====

# GC = c로 정규화하면: AG = 3c, BC = 4c
# 좌표 설정: B(0, 0), G(3c, 0), C(4c, 0)
#
# 원 위의 점들과 기하학적 조건으로부터:
# - A의 좌표: (6c cos²B, 6c sin B cos B)
# - D의 좌표: (a cos B, a sin B)
# - E의 좌표: (a cos B + 4c - 2a/(3cos B), a sin B)
#   (E는 AC 위의 점이고 ED ∥ BC)

# 조건 1: EG = a로부터
# (E_x - 3c)² + (E_y)² = a²를 풀면:
# c - 2a/(3cos B) = 0
# ∴ a = (3c cos B) / 2

a_relation = Rat(3, 2) * c * cos(B)

# 조건 2: 삼각형 EGC의 넓이 = 8
# G = (3c, 0), C = (4c, 0)은 x축 위
# E의 y좌표 = a sin B
# 넓이 = (1/2) × 밑변GC × 높이 = (1/2) × c × a sin B = 8
# ∴ ca sin B = 16
#
# a = (3c cos B)/2를 대입:
# c × (3c cos B / 2) × sin B = 16
# (3/2) c² cos B sin B = 16
# c² sin B cos B = 32/3

c_squared_sin_cos_B = Rat(32, 3)

# ===== S와 T 계산 =====
#
# S = 삼각형 ABG의 넓이
#   좌표: A(6c cos²B, 6c sin B cos B), B(0, 0), G(3c, 0)
#   기저 BG = 3c, 높이 = A의 y좌표 = 6c sin B cos B
#   S = (1/2) × 3c × 6c sin B cos B = 9c² sin B cos B
#
# T = 삼각형 AGC의 넓이
#   좌표: A(6c cos²B, 6c sin B cos B), G(3c, 0), C(4c, 0)
#   기저 GC = c, 높이 = A의 y좌표 = 6c sin B cos B
#   T = (1/2) × c × 6c sin B cos B = 3c² sin B cos B
#
# S - T = 9c² sin B cos B - 3c² sin B cos B
#       = 6c² sin B cos B
#       = 6 × (32/3)
#       = 64

S_minus_T = 6 * c_squared_sin_cos_B

# ===== 최종 검증 =====

if S_minus_T == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')