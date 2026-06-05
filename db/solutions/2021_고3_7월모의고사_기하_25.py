import numpy as np
from sympy import symbols, sqrt, solve

# 주어진 조건
A = np.array([2, 6])
line_coeff = [2, 1, -5]  # 2x + y - 5 = 0
direction_vec = np.array([1, -2])  # 직선의 방향벡터

# 직선 위의 점 P를 (t, 5-2t)로 매개변수화
t = symbols('t')
P_x = t
P_y = 5 - 2*t

# 벡터 AP
AP_x = P_x - 2
AP_y = P_y - 6

# 수직 조건: AP · direction = 0
dot_product = AP_x * direction_vec[0] + AP_y * direction_vec[1]
t_solution = solve(dot_product, t)

# t값 확인
t_val = t_solution[0]
P_coords = (float(t_val), float(5 - 2*t_val))

# 점 P가 직선 위에 있는지 확인
line_check = 2*P_coords[0] + P_coords[1] - 5

# 벡터 AP와 방향벡터가 수직인지 확인
AP_vec = np.array([P_coords[0] - 2, P_coords[1] - 6])
dot_check = np.dot(AP_vec, direction_vec)

# 답: |OP|
OP_magnitude = np.sqrt(P_coords[0]**2 + P_coords[1]**2)

if abs(line_check) < 1e-9 and abs(dot_check) < 1e-9 and abs(OP_magnitude - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')