import numpy as np

A = np.array([9.0, 0.0])
B = np.array([8.0, 1.0])
O = np.array([0.0, 0.0])
P_pt = np.array([11.0, 0.0])

# 조건 (가): |AP| = 2
assert abs(np.linalg.norm(P_pt - A) - 2.0) < 1e-9, 'Cond (가) FAIL'

# 조건 (나): 실수 k 존재 여부 (이차방정식 판별식)
BX = P_pt - B  # (3, -1)
a, b = BX
A_c = a**2 + b**2      # 10
B_c = 16*a + 2*b       # 46
C_c = 49.0
disc = B_c**2 - 4*A_c*C_c  # 2116 - 1960 = 156
assert disc >= 0, f'Cond (나) FAIL: disc={disc}'

# 실제 k 대입 검증
k_val = (-B_c + np.sqrt(disc)) / (2*A_c)
vec = B - O + k_val * BX  # OB + k*BX
assert abs(np.linalg.norm(vec) - 4.0) < 1e-9, f'|OB+kBX|={np.linalg.norm(vec)} FAIL'

# cos(theta) 계산
OP = P_pt - O
BP = P_pt - B
cos_theta = np.dot(OP, BP) / (np.linalg.norm(OP) * np.linalg.norm(BP))
expected = 3 * np.sqrt(10) / 10

if abs(cos_theta - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {cos_theta:.10f}, expected {expected:.10f}')
