from sympy import *
import math

# 포물선 정의
def parabola(x):
    return 8*x

# 점들의 좌표
P = (16, 8*sqrt(2))
H = (-2, 8*sqrt(2))
F = (2, 0)
A = (1, 2*sqrt(2))

# 검증 1: P와 A가 포물선 위에 있는가
check_P = P[1]**2 - parabola(P[0])
check_A = A[1]**2 - parabola(A[0])

# 검증 2: HA : AF = 3 : 1
HA = sqrt((A[0] - H[0])**2 + (A[1] - H[1])**2)
AF = sqrt((F[0] - A[0])**2 + (F[1] - A[1])**2)
ratio = simplify(HA / AF)

# 검증 3: PH 계산
PH = sqrt((H[0] - P[0])**2 + (H[1] - P[1])**2)
PH_value = simplify(PH)

# 검증 4: 포물선의 성질 (PF = PH)
PF = sqrt((F[0] - P[0])**2 + (F[1] - P[1])**2)
PF_value = simplify(PF)

if abs(check_P) < 1e-10 and abs(check_A) < 1e-10 and ratio == 3 and PH_value == 18 and PF_value == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')