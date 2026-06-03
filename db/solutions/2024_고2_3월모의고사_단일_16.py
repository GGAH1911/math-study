import math
from sympy import *

x, y = 2*sqrt(2), sqrt(2)

# 조건 1: BC = √10
BC = sqrt((x - 0)**2 + (0 - y)**2)
assert BC == sqrt(10), f'BC = {BC}'

# 조건 2: 정사각형의 꼭짓점 계산
p = x - 20/(7*y)
s = y - 20/(7*x)
q_x = p + 2*y/7
q_y = 2*x/7
r_x = q_x - 2*x/7
r_y = q_y + 2*y/7

P = (p, 0)
Q = (q_x, q_y)
R = (r_x, r_y)
S = (0, s)

# PQ, QR, RS, SP 벡터
vec_PQ = (Q[0] - P[0], Q[1] - P[1])
vec_QR = (R[0] - Q[0], R[1] - Q[1])
vec_RS = (S[0] - R[0], S[1] - R[1])
vec_SP = (P[0] - S[0], P[1] - S[1])

# 길이 확인 (모두 (2√10)/7이어야 함)
PQ_len = sqrt(vec_PQ[0]**2 + vec_PQ[1]**2)
QR_len = sqrt(vec_QR[0]**2 + vec_QR[1]**2)
RS_len = sqrt(vec_RS[0]**2 + vec_RS[1]**2)
SP_len = sqrt(vec_SP[0]**2 + vec_SP[1]**2)

expected_len = 2*sqrt(10)/7
assert simplify(PQ_len - expected_len) == 0
assert simplify(QR_len - expected_len) == 0
assert simplify(RS_len - expected_len) == 0
assert simplify(SP_len - expected_len) == 0

# 수직 확인
dot_PQ_QR = vec_PQ[0]*vec_QR[0] + vec_PQ[1]*vec_QR[1]
dot_QR_RS = vec_QR[0]*vec_RS[0] + vec_QR[1]*vec_RS[1]
assert simplify(dot_PQ_QR) == 0
assert simplify(dot_QR_RS) == 0

# Q, R이 BC 위에 있는지 확인
assert simplify(x*q_y + y*q_x - x*y) == 0
assert simplify(x*r_y + y*r_x - x*y) == 0

# x > y 확인
assert x > y

# 최종 답 계산
answer = x**3 - y**3
result = simplify(answer)
assert result == 14*sqrt(2), f'x³ - y³ = {result}'

print('VERIFY_PASS')