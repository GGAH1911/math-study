import sympy as sp
from sympy import symbols, exp, log, solve, N

a_val = sp.Rational(2, 9)
b_val = sp.Rational(20, 9)

# 곡선 위의 점들
P = (a_val, 2**a_val)
Q = (b_val, 2**b_val)

# 직선 PQ의 기울기
m = (2**b_val - 2**a_val) / (b_val - a_val)
m_simplified = sp.simplify(m)

# 점 A, B
A_x = a_val + 2**a_val / m
B_y = m * a_val + 2**a_val

# 거리 계산
PB_dist = (a_val**2 + (m * a_val)**2)**0.5
AB_dist = ((A_x - 0)**2 + (0 - B_y)**2)**0.5

# 첫 번째 조건 검증
ratio1 = sp.simplify(AB_dist / PB_dist)

# 점 C
C_x = b_val + 2**b_val / m

# CQ 거리
CQ_dist = ((C_x - b_val)**2 + (0 - 2**b_val)**2)**0.5

# 두 번째 조건 검증
ratio2 = sp.simplify(CQ_dist / AB_dist)

# 최종 답 검증
answer_check = 90 * (a_val + b_val)

if (abs(float(ratio1) - 4) < 1e-10 and abs(float(ratio2) - 3) < 1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')