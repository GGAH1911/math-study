import math

# 좌표 설정
B = (0, 0)
H = (5, 0)
C = (14, 0)
A = (5, 12)

# 주어진 조건 검증
AB = math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
BC = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
AH = abs(A[1] - H[1])

# H가 BC 위에 있는지 확인 (y좌표 같음, x좌표가 B와 C 사이)
is_H_on_BC = (H[1] == B[1] == C[1]) and (B[0] <= H[0] <= C[0])

# AH가 BC에 수직인지 확인 (AH는 수직선)
is_AH_perpendicular = (A[0] == H[0])

# 구하는 값: AC
AC = math.sqrt((C[0]-A[0])**2 + (C[1]-A[1])**2)

# 모든 조건 확인
if abs(AB - 13) < 1e-9 and abs(BC - 14) < 1e-9 and abs(AH - 12) < 1e-9 and is_H_on_BC and is_AH_perpendicular:
    if abs(AC - 15) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')