from fractions import Fraction
import sympy as sp

CANDIDATE = 2

# 선택지 (보기 번호 1-5)
choices = [
    Fraction(35, 6),   # 1번
    Fraction(17, 3),   # 2번
    Fraction(11, 2),   # 3번
    Fraction(16, 3),   # 4번
    Fraction(31, 6),   # 5번
]

k_candidate = choices[CANDIDATE - 1]

# 원래 문제의 함수와 조건
# 함수 1: y = (2/3)^(x+3) + 1 (점 P)
# 함수 2: y = (2/3)^(x+1) + 8/3 (점 Q)
# 직선: y = 2x + k
# 조건: |PQ| = sqrt(5)

# 직선의 기울기가 2이고 PQ = sqrt(5)이므로
# sqrt[(x_q - x_p)^2 + (y_q - y_p)^2] = sqrt(5)
# (y_q - y_p) = 2(x_q - x_p) → sqrt[5(x_q - x_p)^2] = sqrt(5)
# |x_q - x_p| = 1, 그래프에서 x_q = x_p + 1

x_p = sp.Symbol('x_p', real=True)

# P(x_p, y_p)는 함수 1 위: y_p = (2/3)^(x_p+3) + 1
# Q(x_p+1, y_q)는 함수 2 위: y_q = (2/3)^(x_p+1+1) + 8/3
y_p_expr = sp.Rational(2, 3) ** (x_p + 3) + 1
y_q_expr = sp.Rational(2, 3) ** (x_p + 2) + sp.Rational(8, 3)

# 직선 조건: y_q - y_p = 2 * 1 = 2
equation = sp.Eq(y_q_expr - y_p_expr, 2)

# 방정식 풀이
solutions = sp.solve(equation, x_p)

if solutions:
    x_p_value = solutions[0]
    
    # P의 y좌표 계산
    y_p_value = sp.Rational(2, 3) ** (x_p_value + 3) + 1
    
    # 직선 y = 2x + k에서 k값 계산
    k_calculated = y_p_value - 2 * x_p_value
    
    # Q의 좌표 (검증용)
    x_q_value = x_p_value + 1
    y_q_value = sp.Rational(2, 3) ** (x_q_value + 1) + sp.Rational(8, 3)
    
    # PQ 거리의 제곱 확인
    distance_squared = (x_q_value - x_p_value) ** 2 + (y_q_value - y_p_value) ** 2
    
    # 모든 조건 확인
    # 1. k값이 CANDIDATE와 일치하는가?
    # 2. PQ = sqrt(5)인가? (distance_squared = 5)
    if k_calculated == k_candidate and distance_squared == 5:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")