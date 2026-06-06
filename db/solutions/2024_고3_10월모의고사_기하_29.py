import sympy as sp
from sympy import sqrt, symbols

# 문제 조건
Q = (-2, 3)
F = (2, 0)
F_prime = (-2, 0)

# |QF'|, |QF| 계산
QF_prime = sqrt((Q[0] - F_prime[0])**2 + (Q[1] - F_prime[1])**2)
QF = sqrt((Q[0] - F[0])**2 + (Q[1] - F[1])**2)

# 우리가 구한 a 값
a = -2 + 2*sqrt(10)
P = (a, 0)
QP = sqrt((Q[0] - P[0])**2 + (Q[1] - P[1])**2)

# Q가 C_1 위에 있는지 확인
C1_check = Q[0]**2/16 + Q[1]**2/12

# Q가 C_2 위에 있는지 확인
center_x = (2 + a) / 2
c2_half = (a - 2) / 2
b2_sq = 36 - c2_half**2
C2_check = (Q[0] - center_x)**2/36 + Q[1]**2/b2_sq
C2_check_simplified = sp.simplify(C2_check)

# 등차수열 조건 확인
QF_val = 5
QF_prime_val = 3
QP_val = 7
diff1 = QF_val - QF_prime_val
diff2 = QP_val - QF_val

# 검증
print('|QF\' | =', QF_prime, '= 3?', sp.simplify(QF_prime - 3) == 0)
print('|QF| =', QF, '= 5?', sp.simplify(QF - 5) == 0)
print('|QP| =', sp.simplify(QP), '= 7?', sp.simplify(QP - 7) == 0)
print('C_1 위의 점:', C1_check, '= 1?', C1_check == 1)
print('C_2 위의 점:', C2_check_simplified, '= 1?', C2_check_simplified == 1)
print('등차수열 (공차):', diff1, '=', diff2, '?', diff1 == diff2)

# a = p + q√10 확인
p_val = -2
q_val = 2
a_expected = p_val + q_val*sqrt(10)
print('a 값:', sp.simplify(a - a_expected) == 0)
print('p^2 + q^2 =', p_val**2 + q_val**2)

if (sp.simplify(QF_prime - 3) == 0 and 
    sp.simplify(QF - 5) == 0 and 
    sp.simplify(QP - 7) == 0 and
    C1_check == 1 and
    C2_check_simplified == 1 and
    diff1 == diff2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')