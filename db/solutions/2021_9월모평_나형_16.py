import numpy as np
from sympy import sqrt, symbols, simplify

n = symbols('n', positive=True, integer=True)

# 원래 조건: a_{n+1} - a_n = 3
a = lambda k: 3*k - 2

# 검증: n=8일 때
n_val = 8
a_n = a(n_val)  # a_8 = 22
a_n1 = a(n_val + 1)  # a_9 = 25

# 점들의 좌표
O = np.array([0, 0])
P_n1 = np.array([a_n1, 0])
Q_n = np.array([a_n, np.sqrt(3 * a_n)])

# 삼각형 넓이 (신발끈 공식)
area = 0.5 * abs(O[0]*(P_n1[1] - Q_n[1]) + P_n1[0]*(Q_n[1] - O[1]) + Q_n[0]*(O[1] - P_n1[1]))

# 공식으로 계산한 넓이
f_n = 3*n_val + 1  # f(8) = 25
area_formula = 0.5 * f_n * np.sqrt(9*n_val - 6)

# 검증
if abs(area - area_formula) < 1e-10:
    p = 3
    result = p + f_n
    if result == 28:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')