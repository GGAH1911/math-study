from sympy import sqrt, simplify

CANDIDATE = 243

# ========== 문제 조건 단계별 인코딩 ==========

# 좌표계 설정
# B=(0,0), C=(8√3, 0), A=(0, h), D=(8√3, h)
# AD = 8√3 (주어진 조건)

# 조건 1: E는 AD 위, F는 BC 위
# 조건 2: ∠CFE = 60°
#   C=(8√3, 0), F=(f, 0), E=(e, h)
#   FC⃗·FE⃗ / (|FC⃗||FE⃗|) = cos(60°) = 1/2
#   계산 결과: e - f = h/√3

# 조건 3: G는 EF를 1:2로 내분
#   G = (2E + F)/3 = (f + 2h/(3√3), 2h/3)

# 조건 4: |GA⃗ + GC⃗|² 계산
#   GA⃗ = (-G_x, h/3), GC⃗ = (8√3 - G_x, -2h/3)
#   GA⃗ + GC⃗ = (8√3 - 2G_x, -h/3)
#   |GA⃗ + GC⃗|² = (8√3 - 2G_x)² + h²/9

# G_x 범위: [2h/(3√3), 8√3 - h/(3√3)]
# 최솟값: G_x = 4√3일 때, m² = h²/9, m = h/3
# 최댓값: G_x = 8√3 - h/(3√3)일 때, M² = (2h/(3√3))² + h²/9 = 7h²/27

# 조건 5: M:m = √13:1
# M²/m² = 13
# 더 정확한 분석: h=9일 때
#   G_x_min = 2√3: |GA⃗ + GC⃗|² = (4√3)² + 9 = 57
#   G_x_max = 7√3: |GA⃗ + GC⃗|² = (-6√3)² + 9 = 117
#   최댓값 M = √117 = 3√13, 최솟값 m = 3
#   M/m = √13 ✓

h_value = 9

# ========== h=9일 때 G_1, G_2 결정 ==========
# G_1: |GA⃗ + GC⃗|² = 117 (최댓값)일 때
#   G_x = 7√3, G_y = 2h/3 = 6
G_1_x = 7*sqrt(3)
G_1_y = 6

# G_2: |GA⃗ + GC⃗|² = 9 (최솟값)일 때
#   G_x = 4√3, G_y = 2h/3 = 6
G_2_x = 4*sqrt(3)
G_2_y = 6

# B = (0, 0)
B_x = 0
B_y = 0

# ========== 삼각형 BG_1G_2의 넓이 ==========
# G_1과 G_2의 y좌표가 같음 (모두 6)
# 밑변 = |G_1_x - G_2_x| = |7√3 - 4√3| = 3√3
# 높이 = |G_1_y - B_y| = |6 - 0| = 6
# 넓이 S = (1/2) × 밑변 × 높이

base = G_1_x - G_2_x
height = G_1_y - B_y
S = base * height / 2
S = simplify(S)

# ========== S² 계산 ==========
S_squared = simplify(S**2)

# ========== 검증: CANDIDATE = 243 확인 ==========
if S_squared == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
    print(f"Calculated: S² = {S_squared}")
    print(f"Expected: {CANDIDATE}")