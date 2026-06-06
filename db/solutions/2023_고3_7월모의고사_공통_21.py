import numpy as np
from scipy.optimize import fsolve

m, n = 3, 10
x_A, x_B = 4, 6

# 검증: A, B가 두 식의 교점인지 확인
check_A_exp = 2**(x_A - m) + n
check_A_line = 3 * x_A
assert abs(check_A_exp - check_A_line) < 1e-9, f'A 검증 실패: {check_A_exp} != {check_A_line}'

check_B_exp = 2**(x_B - m) + n
check_B_line = 3 * x_B
assert abs(check_B_exp - check_B_line) < 1e-9, f'B 검증 실패: {check_B_exp} != {check_B_line}'

# 삼각형 ABC 넓이 검증
A = np.array([x_A, 3*x_A])
B = np.array([x_B, 3*x_B])
C = np.array([0, 10*x_B/3])

area = 0.5 * abs((B[0]-A[0])*(C[1]-A[1]) - (C[0]-A[0])*(B[1]-A[1]))
assert abs(area - 20) < 1e-9, f'넓이 검증 실패: {area} != 20'

# D가 5:3 외분 조건 검증
D = (5*A - 3*C) / 2
assert abs(D[1]) < 1e-9, f'D y좌표가 0이 아님: {D[1]}'
assert abs(3*x_A - 2*x_B) < 1e-9, f'외분 조건 실패'

print('VERIFY_PASS')