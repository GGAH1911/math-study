import numpy as np
from sympy import sqrt, symbols, solve, simplify

# AP = BP 조건을 만족하는 t 구하기
t = symbols('t')
AP_squared = (t - 2)**2 + (-t - 4)**2
BP_squared = (t - 5)**2 + (-t - 1)**2
eq = AP_squared - BP_squared
t_val = solve(eq, t)[0]

# P의 좌표와 OP 길이
P = np.array([float(t_val), float(-t_val)])
OP_length = np.linalg.norm(P)

# 원래 조건 검증
A = np.array([2, 4])
B = np.array([5, 1])
AP = np.linalg.norm(P - A)
BP = np.linalg.norm(P - B)

# P가 y = -x 위에 있는지 확인
on_line = np.isclose(P[1], -P[0])

# 최종 검증
if on_line and np.isclose(AP, BP) and np.isclose(OP_length, float(sqrt(2)/2)):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')