import math
from math import log2, sqrt, isclose

CANDIDATE = 9

# 주어진 조건
# 곡선 1: y = 2^(x+1) + k
# 곡선 2: y = log_2(x-k) + 1
# A, B는 곡선 1 위의 점, C는 곡선 2 위의 점
# 조건 (가): AB의 기울기 = 1
# 조건 (나): ABC는 한 변의 길이 2√2인 정삼각형

# 풀이에서 구한 k 값들
log2_3 = log2(3)
k1 = 1/3 - log2_3 + sqrt(3)
k2 = 1/3 - log2_3 - sqrt(3)

# S = k1 + k2 계산
S = k1 + k2
S_theory = 2/3 - 2*log2_3
assert isclose(S, S_theory, rel_tol=1e-9), f"S 계산 오류: {S} vs {S_theory}"

# k=k1일 때 조건 검증
k = k1

# 풀이에서 t=2일 때 2^a = 1/3
a = -log2_3
b = 2 - log2_3
assert isclose(2**a, 1/3, rel_tol=1e-9), "2^a = 1/3 조건 실패"

# 곡선 1: y = 2^(x+1) + k에서 A, B의 좌표
A_x = a
A_y = 2**(a+1) + k
B_x = b
B_y = 2**(b+1) + k

# 조건 (가) 검증: AB의 기울기 = 1
slope_AB = (B_y - A_y) / (B_x - A_x)
assert isclose(slope_AB, 1.0, rel_tol=1e-9), f"기울기 조건 실패: {slope_AB}"

# 조건 (나) 검증: |AB| = 2√2
AB_length = sqrt((B_x - A_x)**2 + (B_y - A_y)**2)
assert isclose(AB_length, 2*sqrt(2), rel_tol=1e-9), f"|AB| 조건 실패: {AB_length}"

# C의 좌표
# 중점 M = (1 - log_2(3), 5/3 + k)
# AB에 수직 방향 ±√3 거리 이동
C_x = 1 - log2_3 + sqrt(3)
C_y = 5/3 + k - sqrt(3)

# C가 곡선 2 위에 있는지 검증: y = log_2(x-k) + 1
y_curve2 = log2(C_x - k) + 1
assert isclose(C_y, y_curve2, rel_tol=1e-9), f"C가 곡선 2 위에 없음: {C_y} vs {y_curve2}"

# 정삼각형 조건: |AC| = |BC| = |AB| = 2√2
AC_length = sqrt((C_x - A_x)**2 + (C_y - A_y)**2)
BC_length = sqrt((C_x - B_x)**2 + (C_y - B_y)**2)

assert isclose(AC_length, 2*sqrt(2), rel_tol=1e-9), f"|AC| 조건 실패: {AC_length}"
assert isclose(BC_length, 2*sqrt(2), rel_tol=1e-9), f"|BC| 조건 실패: {BC_length}"

# 최종 답 계산
# 2^(-S + 2/3) = 2^(2*log_2(3)) = 3^2 = 9
result = 2**(-S + 2/3)

if isclose(result, CANDIDATE, rel_tol=1e-9):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")