import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 검증: Y가 만족하는 원의 방정식 확인
# 경우 1: 중심 (-4, 4), 반지름 2√3
center1 = np.array([-4, 4])
radius1 = 2 * np.sqrt(3)

# 경우 2: 중심 (4, 4), 반지름 2√3  
center2 = np.array([4, 4])
radius2 = 2 * np.sqrt(3)

# 경우 1의 호: θ1 - π/6 ∈ [π/2, 4π/3]
# 샘플점: θ = 3π/4
theta1_sample = 3 * np.pi / 4
Y1_sample = center1 + radius1 * np.array([np.cos(theta1_sample), np.sin(theta1_sample)])
dist1 = np.linalg.norm(Y1_sample - center1)

# 경우 2의 호: φ1 - π/6 ∈ [-π/6, 4π/3]
theta2_sample = np.pi / 3
Y2_sample = center2 + radius2 * np.array([np.cos(theta2_sample), np.sin(theta2_sample)])
dist2 = np.linalg.norm(Y2_sample - center2)

# 호의 길이 계산
arc_length1 = radius1 * (4*np.pi/3 - np.pi/2)  # [π/2, 4π/3]
arc_length2 = radius2 * (4*np.pi/3 - (-np.pi/6))  # [-π/6, 4π/3)
total_arc = arc_length1 + arc_length2

# q/p 계산
q_over_p = total_arc / (np.sqrt(3) * np.pi)

# 검증
if abs(dist1 - radius1) < 1e-10 and abs(dist2 - radius2) < 1e-10:
    if abs(q_over_p - 14/3) < 1e-10:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")