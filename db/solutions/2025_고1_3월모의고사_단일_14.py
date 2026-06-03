import numpy as np
from numpy import cos, sin, pi, sqrt

# α = 36°
alpha = 36 * pi / 180

# 중심각: 호 AB = 108°, 호 CD = 72°
angle_AOB = 3 * alpha  # 108°
angle_COD = 2 * alpha  # 72°

# β + γ = 180°로 설정 (예: β = 100°, γ = 80°)
beta = 100 * pi / 180
gamma = 80 * pi / 180

# 원의 반지름 = 1
A = np.array([1, 0])
B = np.array([cos(angle_AOB), sin(angle_AOB)])
C = np.array([cos(angle_AOB + beta), sin(angle_AOB + beta)])
D = np.array([cos(angle_AOB + beta + angle_COD), sin(angle_AOB + beta + angle_COD)])

# 벡터 AC, BD
AC = C - A
BD = D - B

# AC · BD = 0 확인 (수직 조건)
dot_product = np.dot(AC, BD)

# ∠ACB 계산 (호 AB에 대한 원주각)
CA = A - C
CB = B - C
cos_angle = np.dot(CA, CB) / (np.linalg.norm(CA) * np.linalg.norm(CB))
angle_ACB = np.arccos(cos_angle) * 180 / pi

if abs(angle_ACB - 54) < 0.1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')