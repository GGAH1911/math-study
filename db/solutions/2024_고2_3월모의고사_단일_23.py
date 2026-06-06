import math

# 외분점 검증: PA와 PB의 거리비가 2:1인지 확인
A = (3, 3)
B = (7, 11)
P = (11, 19)

# 거리 계산
dist_PA = math.sqrt((P[0] - A[0])**2 + (P[1] - A[1])**2)
dist_PB = math.sqrt((P[0] - B[0])**2 + (P[1] - B[1])**2)

ratio = dist_PA / dist_PB

# 벡터로도 확인: PA = 2 * PB인지
PA = (A[0] - P[0], A[1] - P[1])
PB = (B[0] - P[0], B[1] - P[1])

# PA와 PB가 같은 방향이고 비율이 2:1인지 확인
vector_ratio = PA[0] / PB[0] if PB[0] != 0 else PA[1] / PB[1]

if abs(ratio - 2.0) < 1e-9 and abs(vector_ratio - 2.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')