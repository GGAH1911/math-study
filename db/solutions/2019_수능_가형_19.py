import numpy as np
from sympy import *

# 정삼각형 BCD, 변 12
B = Matrix([0, 0, 0])
D = Matrix([12, 0, 0])
C = Matrix([6, 6*sqrt(3), 0])

# 넓이 조건으로 H 무게중심 좌표
# Area(CDH)=3*Area(BCH), Area(DBH)=2*Area(BCH)
# lambda_B=1/2, lambda_C=1/3, lambda_D=1/6
lam_B = Rational(1,2)
lam_C = Rational(1,3)
lam_D = Rational(1,6)
H = lam_B*B + lam_C*C + lam_D*D
print('H =', H.T)

# 넓이 검증
def tri_area(P1, P2, P3):
    v1 = P2 - P1
    v2 = P3 - P1
    cross = v1.cross(v2)
    return Abs(cross.norm()) / 2

S = tri_area(B, C, H)
S_CDH = tri_area(C, D, H)
S_DBH = tri_area(D, B, H)
print('Area BCH =', simplify(S))
print('Area CDH =', simplify(S_CDH), '= 3*S:', simplify(S_CDH - 3*S) == 0)
print('Area DBH =', simplify(S_DBH), '= 2*S:', simplify(S_DBH - 2*S) == 0)

# A = H + (0,0,3)
A = Matrix([H[0], H[1], 3])
print('A =', A.T)
print('AH =', simplify((A-H).norm()))

# M = midpoint of BD
M = (B + D) / 2
print('M =', M.T)

# 직선 CM, t=0 at C, t=1 at M
t = symbols('t')
P = C + t*(M - C)
AP = P - A
CM_dir = M - C

# 수직 조건
eq = AP.dot(CM_dir)
t0 = solve(eq, t)[0]
print('t0 =', t0)

Q = C + t0*(M - C)
print('Q =', Q.T)

# AQ 계산
AQ_vec = Q - A
AQ_len = simplify(AQ_vec.norm())
print('|AQ| =', AQ_len)

# 검증
if simplify(AQ_len**2 - 13) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', 'AQ^2 =', simplify(AQ_len**2))
