from sympy import *

# 파라미터
a2 = Integer(2)          # a^2 = 2
c2 = Integer(1)          # c^2 = 1
d2 = Rational(7, 2)      # d^2 = 7/2

a = sqrt(a2)
c = sqrt(c2)
d = sqrt(d2)

F  = Matrix([c,  Integer(0)])
Fp = Matrix([-c, Integer(0)])
G  = Matrix([Integer(0),  d])
Gp = Matrix([Integer(0), -d])

# P = midpoint of FG
P = Matrix([Rational(1,2), d/2])

# 조건1: P가 C1 위에 있는가
C1_check = P[0]**2 / a2 + P[1]**2 - 1
assert simplify(C1_check) == 0, f'P not on C1: {simplify(C1_check)}'

# 조건2: GP = PF
GP = sqrt((P - G).dot(P - G))
PF = sqrt((P - F).dot(P - F))
assert simplify(GP - PF) == 0, f'GP != PF'

# 조건3: GP + PF' = 2sqrt(2)
PFp = sqrt((P - Fp).dot(P - Fp))
assert simplify(GP + PFp - 2*sqrt(2)) == 0, f'GP+PFp != 2sqrt(2)'

# C2: B^2 = a^2 = 2, A^2 = 2 + 7/2 = 11/2
B2 = a2
A2 = B2 + d2
A  = sqrt(A2)

# C2가 (sqrt(2), 0)을 지나는지
C2_vtx_check = Rational(2,1)/B2 + Integer(0)/A2 - 1
assert simplify(C2_vtx_check) == 0, 'C2 does not pass vertex'

# QG + QG' = 2A (타원 정의)
QG_sum = 2 * A
result = simplify(QG_sum**2 - 22)
if result == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: QG+QG\' squared = {simplify(QG_sum**2)}')
