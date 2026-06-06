from sympy import symbols, expand

CANDIDATE = 16

# 원래 문제 조건 인코딩:
# - 4종류 인형(A, B, C, D), 각 2개씩 (총 8개)
# - 5개 선택
# - 각 종류에서 0개~2개 선택 가능
# - 같은 종류끼리는 구별하지 않음

# 수식: a_1 + a_2 + a_3 + a_4 = 5
#       0 <= a_i <= 2 (i=1,2,3,4)
# 위를 만족하는 (a_1, a_2, a_3, a_4)의 개수 = ?

# 방법 1: 직접 조건을 만족하는 경우의 수 계산
count_direct = 0
for a1 in range(3):  # 0, 1, 2
    for a2 in range(3):
        for a3 in range(3):
            for a4 in range(3):
                if a1 + a2 + a3 + a4 == 5:  # 정확히 5개 선택
                    count_direct += 1

# 방법 2: 생성함수로 검증
# 각 종류: (1 + x + x^2) - 0개, 1개, 또는 2개 선택
# 4종류: (1 + x + x^2)^4
# x^5의 계수 = 5개 선택하는 경우의 수
x = symbols('x')
generating_function = (1 + x + x**2)**4
expanded = expand(generating_function)
coeff_gf = expanded.coeff(x, 5)

# CANDIDATE가 원래 문제 조건을 만족하는지 검증
if count_direct == CANDIDATE and int(coeff_gf) == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")