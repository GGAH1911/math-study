from sympy import *

sqrt3 = sqrt(3)
c = 3*sqrt3
F = Matrix([c, 0])
Fp = Matrix([-c, 0])

# 해: q=3, Q=(0,3), P=(3√3,6)
q = Integer(3)
Q = Matrix([Integer(0), q])
P = Matrix([3*sqrt3, Integer(6)])

# 1. P 제1사분면 확인
assert P[0] > 0 and P[1] > 0

# 2. Q가 y축 위
assert Q[0] == 0

# 3. F', Q, P 공선 (외적=0)
v1 = Q - Fp
v2 = P - Fp
cross = v1[0]*v2[1] - v1[1]*v2[0]
assert simplify(cross) == 0

# 4. 정삼각형 PQF 확인
PQ = sqrt((P-Q).dot(P-Q))
QF = sqrt((Q-F).dot(Q-F))
PF = sqrt((P-F).dot(P-F))
assert simplify(PQ - QF) == 0 and simplify(QF - PF) == 0

# 5. P가 쌍곡선 위에 있는지 확인 (원래 방정식)
PF_d = sqrt((P-F).dot(P-F))
PFp_d = sqrt((P-Fp).dot(P-Fp))
two_a = simplify(abs(PFp_d - PF_d))
a = two_a / 2
b2 = c**2 - a**2
hyp_check = simplify(P[0]**2/a**2 - P[1]**2/b2)
assert hyp_check == 1

# 6. 주축의 길이 = 6
if simplify(two_a - 6) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
