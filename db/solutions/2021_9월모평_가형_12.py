import math
from math import sqrt

# 주어진 조건
AB = 6
AC = 10
AD = 6  # AB = AD
BD = sqrt(15)

# 좌표 설정
A = (0, 0)
C = (10, 0)
D = (6, 0)

# B의 좌표 계산
# AB = 6: x^2 + y^2 = 36
# BD = sqrt(15): (x-6)^2 + y^2 = 15
# 풀이: x = 19/4, y^2 = 215/16

x_B = 19/4
y_B_squared = 215/16
y_B = sqrt(y_B_squared)

B = (x_B, y_B)

# 검증
AB_check = sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
AD_check = sqrt((D[0] - A[0])**2 + (D[1] - A[1])**2)
BD_check = sqrt((B[0] - D[0])**2 + (B[1] - D[1])**2)
BC_computed = sqrt((B[0] - C[0])**2 + (B[1] - C[1])**2)

# 모든 조건 확인
abs_err_AB = abs(AB_check - AB)
abs_err_AD = abs(AD_check - AD)
abs_err_BD = abs(BD_check - BD)

if abs_err_AB < 1e-9 and abs_err_AD < 1e-9 and abs_err_BD < 1e-9:
    # BC = sqrt(41)
    expected_BC = sqrt(41)
    if abs(BC_computed - expected_BC) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')