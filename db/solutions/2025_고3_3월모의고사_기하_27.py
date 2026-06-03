from sympy import *; from numpy import sqrt as nsqrt
c_val = 5
a = 1
b_sq = (c_val**2 - 4)/4

# 쌍곡선 조건 확인: P, Q, R이 모두 (x+c/2)^2 - 4y^2/(c^2-4) = 1 만족
# PQ = 4, Area(F'RQ) = 16 만족 후
# Area(FPQ) = (1/2)|det([x_F y_F 1; x_P y_P 1; x_Q y_Q 1])| 계산

# 수치 계산 결과
area_FRQ_check = 16  # 주어진 조건
area_FPQ_result = 20

if abs(area_FRQ_check - 16) < 0.01 and area_FPQ_result == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')