import numpy as np
from numpy.linalg import norm

c = 3 * np.sqrt(17) / 2

a2 = 25 * c**2 / 17
b2 = 8 * c**2 / 17

F  = np.array([c,  0.0])
Fp = np.array([-c, 0.0])

# Q 결정 (원래 조건에서 유도)
Q = np.array([15*c/17, -8*c/17])

# 조건 1: Q가 타원 위
assert abs(Q[0]**2/a2 + Q[1]**2/b2 - 1) < 1e-9

# 조건 2: OQ = OF = c
assert abs(norm(Q) - c) < 1e-9

# 조건 3: FQ:F'Q = 1:4
FQ_len  = norm(Q - F)
FpQ_len = norm(Q - Fp)
assert abs(FpQ_len / FQ_len - 4) < 1e-9

# P: 타원과 y=4(x-c) 교점 (Q 아닌 쪽)
A_coef = 1/a2 + 16/b2
B_coef = -32*c/b2
C_coef = 16*c**2/b2 - 1
disc = B_coef**2 - 4*A_coef*C_coef
roots = [(-B_coef + np.sqrt(disc))/(2*A_coef),
         (-B_coef - np.sqrt(disc))/(2*A_coef)]
cands = [(x, 4*(x-c)) for x in roots if abs(x - Q[0]) > 1e-6]
assert len(cands) == 1
xP, yP = cands[0]
P = np.array([xP, yP])

# P가 타원 위이고 1사분면
assert abs(P[0]**2/a2 + P[1]**2/b2 - 1) < 1e-9
assert P[0] > 0 and P[1] > 0

# 삼각형 PF'Q 내접원 반지름 = 넓이 / 반둘레
PQ_len  = norm(P - Q)
QFp_len = norm(Q - Fp)
PFp_len = norm(P - Fp)
s    = (PQ_len + QFp_len + PFp_len) / 2
area = 0.5 * abs((Q[0]-P[0])*(Fp[1]-P[1]) - (Fp[0]-P[0])*(Q[1]-P[1]))
r    = area / s

if abs(r - 2) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: r={r:.8f}')