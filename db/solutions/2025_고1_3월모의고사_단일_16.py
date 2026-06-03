import sympy as sp
from sympy import symbols, Rational

# 각 경우의 a 값
a_values = [8, Rational(1, 2)]

for a_val in a_values:
    # 점 정의
    A = (-8, 0)
    B = (0, 4)
    C = (2, 0)
    D = (0, -2*a_val)
    
    # 벡터 계산
    AD = (D[0] - A[0], D[1] - A[1])  # (8, -2a)
    CB = (B[0] - C[0], B[1] - C[1])  # (-2, 4)
    DC = (C[0] - D[0], C[1] - D[1])  # (2, 2a)
    AB = (B[0] - A[0], B[1] - A[1])  # (8, 4)
    
    # 평행 조건 검사 (외적이 0)
    cross_AD_CB = AD[0] * CB[1] - AD[1] * CB[0]
    cross_DC_AB = DC[0] * AB[1] - DC[1] * AB[0]
    
    # 사다리꼴 확인: 정확히 하나의 대변 쌍이 평행
    is_trapezoid = (cross_AD_CB == 0 and cross_DC_AB != 0) or (cross_AD_CB != 0 and cross_DC_AB == 0)
    assert is_trapezoid, f'a={a_val}은 사다리꼴이 아님'

# 합 계산
total_sum = sum(a_values)
assert total_sum == Rational(17, 2), f'합이 {total_sum}'
print('VERIFY_PASS')