import sympy as sp
from sympy import sqrt

A = (0, 1)
B = (0, 4)
p_val, q_val = 5, 4
C = (sqrt(2), p_val)
D = (3*sqrt(2), q_val)

# 조건 (가): CD 기울기 음수
slope_CD = (q_val - p_val) / (D[0] - C[0])
assert slope_CD < 0, f'CD 기울기 음수 실패: {slope_CD}'

# 조건 (나): AB = CD
AB = abs(B[1] - A[1])
CD = sqrt((D[0] - C[0])**2 + (D[1] - C[1])**2)
assert AB == CD, f'AB=CD 실패: {AB} vs {CD}'

# 조건 (나): AD // BC
slope_AD = (D[1] - A[1]) / (D[0] - A[0])
slope_BC = (C[1] - B[1]) / (C[0] - B[0])
assert slope_AD == slope_BC, f'AD//BC 실패: {slope_AD} vs {slope_BC}'

print('VERIFY_PASS')