from sympy import *
from math import gcd

CANDIDATE = 13

# ============================================================
# 문제: 쌍곡선 x²/10 - y²/a² = 1
# 초점: F(c,0), F'(-c,0), c² = 10 + a²
# 점 P: 쌍곡선 위 (제2사분면)
# 조건: ∠F'PF = π/2, 넓이(F'FP) = 15
# 구하기: 직선 PF'과 평행한 쌍곡선 접선들의 x절편 거리
#         |Q1Q2| = (q/p)√3, p+q = ?
# ============================================================

verify_result = True

try:
    # 문제 조건들로부터 계산된 값
    a_squared = 15
    c = 5
    P = (-4, 3)
    F = (5, 0)
    F_prime = (-5, 0)
    
    # [검증 1] P가 쌍곡선 위의 점인가?
    # x²/10 - y²/a² = 1
    hyperbola_check = P[0]**2 / 10 - P[1]**2 / a_squared
    if hyperbola_check != 1:
        verify_result = False
    
    # [검증 2] c² = 10 + a² 관계식
    if c**2 != 10 + a_squared:
        verify_result = False
    
    # [검증 3] ∠F'PF = π/2 (직각)
    # 벡터 PF와 PF'의 내적이 0
    PF = (F[0] - P[0], F[1] - P[1])
    PF_prime = (F_prime[0] - P[0], F_prime[1] - P[1])
    dot_product = PF[0] * PF_prime[0] + PF[1] * PF_prime[1]
    if dot_product != 0:
        verify_result = False
    
    # [검증 4] 삼각형 F'FP의 넓이 = 15
    # 직각삼각형: 넓이 = (1/2) * |PF| * |PF'|
    dist_PF = sqrt(PF[0]**2 + PF[1]**2)
    dist_PF_prime = sqrt(PF_prime[0]**2 + PF_prime[1]**2)
    area = simplify(dist_PF * dist_PF_prime / 2)
    if area != 15:
        verify_result = False
    
    # [검증 5] 직선 PF'의 기울기
    slope = (P[1] - F_prime[1]) / (P[0] - F_prime[0])
    if slope != 3:
        verify_result = False
    
    # [검증 6] 기울기 m인 직선이 쌍곡선 x²/A - y²/B = 1에 접할 조건
    # y = mx + n 형태에서 n² = A*m² - B
    # 쌍곡선: x²/10 - y²/15 = 1, 기울기 m=3
    A_coef = 10
    B_coef = a_squared  # 15
    n_squared = A_coef * slope**2 - B_coef
    if n_squared != 75:  # 10*9 - 15 = 75
        verify_result = False
    
    # [검증 7] 접선과 x축의 교점
    # 접선 1: y = 3x + √75 → x절편 = -√75/3
    # 접선 2: y = 3x - √75 → x절편 = √75/3
    n_val = sqrt(75)
    Q1_x = -n_val / 3
    Q2_x = n_val / 3
    
    # [검증 8] |Q1Q2| 거리 계산
    Q1Q2_distance = Q2_x - Q1_x
    Q1Q2_simplified = simplify(Q1Q2_distance)
    
    # Q1Q2 = √75/3 + √75/3 = 2√75/3 = 2*5√3/3 = 10√3/3
    expected_distance = Rational(10, 3) * sqrt(3)
    if simplify(Q1Q2_simplified - expected_distance) != 0:
        verify_result = False
    
    # [검증 9] |Q1Q2| = (q/p)√3 형태에서 q, p
    # (10/3)√3 → q=10, p=3
    q = 10
    p = 3
    
    # gcd(q, p) = 1 확인
    if gcd(q, p) != 1:
        verify_result = False
    
    # [검증 10] 최종 답: p + q
    computed_answer = p + q
    
    # CANDIDATE와 비교 (원래 식으로부터 계산한 결과)
    if computed_answer != CANDIDATE:
        verify_result = False

except:
    verify_result = False

if verify_result:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")