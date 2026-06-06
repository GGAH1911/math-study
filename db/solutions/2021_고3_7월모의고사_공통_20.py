import math
from math import sqrt

# 삼각형 CAD의 꼭짓점
C = (2, 4*sqrt(2))
A = (0, 0)
D = (10, 0)

# 외접원의 중심과 반지름 (계산 결과)
center = (5, sqrt(2))
R = sqrt(27)

# 세 점이 모두 외접원 위에 있는지 확인
dist_A = math.sqrt((center[0]-A[0])**2 + (center[1]-A[1])**2)
dist_D = math.sqrt((center[0]-D[0])**2 + (center[1]-D[1])**2)
dist_C = math.sqrt((center[0]-C[0])**2 + (center[1]-C[1])**2)

tolerance = 1e-9
if abs(dist_A - R) < tolerance and abs(dist_D - R) < tolerance and abs(dist_C - R) < tolerance:
    S = math.pi * R**2
    answer = S / math.pi
    if abs(answer - 27) < tolerance:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')