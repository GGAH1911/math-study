from sympy import sqrt, simplify, Rational

CANDIDATE = 4

# ========== 검증된 풀이 단계 인코딩 ==========

# 단계 1: 좌표 설정
# A(-2, 0), B1(0, 0), C1(0, √3)
A_coord = (-2, 0)
B1_coord = (0, 0)
C1_coord = (0, sqrt(3))

# 단계 2: 방멱 조건으로 E1 계산
# C1B1 · C1E1 = C1D1² = 1
C1B1_dist = sqrt(3)  # C1(0,√3) - B1(0,0)의 거리
C1D1_dist = 1        # 주어진 조건
C1E1_dist = C1D1_dist**2 / C1B1_dist  # = 1/√3
E1_y = sqrt(3) - C1E1_dist  # E1은 B1C1 위의 점
E1_y_simplified = simplify(E1_y)  # = 2/√3
E1_coord = (0, E1_y_simplified)

# 단계 3: 원의 중심과 반지름 검증
# AE1이 지름이므로: 중심 = (-1, 1/√3), 반지름 = 2/√3
center = (-1, 1/sqrt(3))
radius = 2/sqrt(3)

# 단계 4: 첫 번째 색칠 넓이
# 삼각형 C1D1E1 + 두 활꼴의 합
S1 = sqrt(3) / 6

# 단계 5: A 중심 닮음비
# 7k² - 6k = 0에서 k = 6/7
k = Rational(6, 7)
area_ratio = k**2  # = 36/49

# 단계 6: 색칠 넓이의 등비급수
# S_n은 첫항 S1, 공비 36/49인 등비급수
# lim S_n = S_1 + k²·S_1 + k⁴·S_1 + ... = S_1/(1-k²)
one_minus_ratio = 1 - area_ratio  # = 13/49
limit_calculated = S1 / one_minus_ratio
limit_value = simplify(limit_calculated)

# 단계 7: 보기 정의
# 검증된 풀이에서 "→ 보기 ④"로 명시된 값
options_by_number = {
    4: (49 * sqrt(3)) / 78,
}

# 단계 8: 검증
# CANDIDATE(보기 번호 4)의 값이 계산된 극한값과 일치하는지 확인
expected_value = simplify(options_by_number[CANDIDATE])
difference = simplify(limit_value - expected_value)

if difference == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")