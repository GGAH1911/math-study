import math
from sympy import sqrt, Rational

# P의 좌표
P = (Rational(7,2), sqrt(15)/2)
Q = (Rational(5,2), sqrt(15)/2)
A = (2, 0)
B = (6, 0)
C = (0, 1)
O = (0, 0)

# 조건 (가) 검증: AP · BP = 0
AP = (P[0] - A[0], P[1] - A[1])
BP = (P[0] - B[0], P[1] - B[1])
dot_AP_BP = AP[0] * BP[0] + AP[1] * BP[1]
assert dot_AP_BP == 0, f'AP·BP should be 0, got {dot_AP_BP}'

# 조건 (가) 검증: OP · OC ≥ 0
OP = (P[0] - O[0], P[1] - O[1])
OC = (C[0] - O[0], C[1] - O[1])
dot_OP_OC = OP[0] * OC[0] + OP[1] * OC[1]
assert dot_OP_OC > 0, f'OP·OC should be >= 0, got {dot_OP_OC}'

# 조건 (나) 검증: QB = 4QP + QA
QB = (B[0] - Q[0], B[1] - Q[1])
QP = (P[0] - Q[0], P[1] - Q[1])
QA = (A[0] - Q[0], A[1] - Q[1])
check_QB = (4*QP[0] + QA[0], 4*QP[1] + QA[1])
assert QB[0] == check_QB[0] and QB[1] == check_QB[1], f'QB check failed'

# |QA| = 2 검증
QA_norm = (QA[0]**2 + QA[1]**2)**Rational(1,2)
assert QA_norm == 2, f'|QA| should be 2, got {QA_norm}'

# AP · AQ = k 계산
AQ = (Q[0] - A[0], Q[1] - A[1])
k = AP[0] * AQ[0] + AP[1] * AQ[1]
assert k == Rational(9,2), f'k should be 9/2, got {k}'

# 최종 답: 20 × k
answer = 20 * k
assert answer == 90, f'20*k should be 90, got {answer}'

print('VERIFY_PASS')