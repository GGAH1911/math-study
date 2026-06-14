CANDIDATE = 12

from sympy import *

k = symbols('k', positive=True)

# k>1 조건에서 3k = k^2 => k=3
k_val = Rational(3)
assert 3*k_val == k_val**2, 'k 검증 실패'

# m 결정
m_val = Rational(1, 4)

# 좌표
alpha = 3  # x_B
beta = 9   # x_C

# A, B, C, D, E
A = (1, 0)
B = (alpha, m_val*(alpha-1))
C = (beta, m_val*(beta-1))
D = (beta, log(beta, 9))  # log_{9}(9) = 1
E = (beta, 0)

# B가 log_9(x) 위인지 확인
b_curve = log(B[0], 9)
assert simplify(b_curve - B[1]) == 0, 'B not on log_9'

# C가 log_3(x) 위인지 확인
c_curve = log(C[0], 3)
assert simplify(c_curve - C[1]) == 0, 'C not on log_3'

# 넓이 계산
def area(P1, P2, P3):
    return Abs(P1[0]*(P2[1]-P3[1]) + P2[0]*(P3[1]-P1[1]) + P3[0]*(P1[1]-P2[1])) / 2

S_BDC = area(B, D, C)
S_ADB = area(A, D, B)
S_AED = area(A, E, D)

# 조건 (가): S_BDC = 3 * S_ADB
cond_ga = simplify(S_BDC - 3*S_ADB) == 0
# 조건 (나): S_BDC = (3/4) * S_AED
cond_na = simplify(S_BDC - Rational(3,4)*S_AED) == 0

# k/m 값 확인
result = k_val / m_val

if cond_ga and cond_na and result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'S_BDC={S_BDC}, S_ADB={S_ADB}, S_AED={S_AED}')
    print(f'cond_ga={cond_ga}, cond_na={cond_na}, k/m={result}')
