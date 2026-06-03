import numpy as np
from sympy import symbols, solve, simplify

# 주어진 값
a, b = 2, 2

# 점들
A = np.array([3, -1, a])
B = np.array([3, -1, -a])  # xy평면 대칭
C = np.array([-3, b, 4])

# BC를 1:2로 내분하는 점
P = (2*B + C) / 3

# x축 위의 점 조건: y=0, z=0
if abs(P[1]) < 1e-10 and abs(P[2]) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')