from sympy import pi, sin, cos, simplify

CANDIDATE = 3

# 문제 조건 인코딩
# 첫 번째 부채꼴 O_1A_1B_1: 중심각 π/4, 반지름 1
# S_1 = (1/2) * r^2 * θ = (1/2) * 1^2 * (π/4) = π/8
S_1 = pi / 8

# 닮음비 계산
# O_2 = (cos(5π/12), sin(5π/12))
# A_2 = (sin(5π/12), sin(5π/12))  [O_2를 지나고 O_1A_1에 평행한 직선과 O_1B_1의 교점]
# O_2A_2 = sin(5π/12) - cos(5π/12)

theta_total = 5 * pi / 12
k = sin(theta_total) - cos(theta_total)
k = simplify(k)  # sqrt(2)/2

# 넓이비 = k^2
area_ratio = simplify(k ** 2)  # 1/2

# 무한급수 합: Σ S_n = S_1 / (1 - area_ratio)
# = (π/8) / (1 - 1/2) = (π/8) / (1/2) = π/4
infinite_sum = simplify(S_1 / (1 - area_ratio))

# 보기 목록 (표준 기출형식)
# CANDIDATE=3은 보기번호
choices = {
    1: pi/6,
    2: pi/5, 
    3: pi/4,
    4: pi/3,
    5: pi/2
}

# 계산 결과가 보기 CANDIDATE의 값과 일치하는지 검증
if simplify(infinite_sum - choices[CANDIDATE]) == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")