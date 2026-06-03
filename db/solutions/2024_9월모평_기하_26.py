import math
from math import sqrt

# 좌표 설정
A = (0, 0, 0)
B = (3, 0, 0)
D = (0, 3, 0)
E = (0, 0, 6)
G = (3, 3, 6)

# 삼각형 BEG의 무게중심 P
P = tuple((B[i] + E[i] + G[i]) / 3 for i in range(3))

# DP 거리
dist_DP = sqrt(sum((P[i] - D[i])**2 for i in range(3)))

# 검증: 답이 2√6인지 확인
expected = 2 * sqrt(6)

if abs(dist_DP - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')