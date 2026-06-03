import numpy as np

# 조건
sin_t1 = 4/5
cos_t1 = 3/5

# 좌표계: A=원점, AB=x축, alpha=xy평면
AB = np.array([1.0, 0.0, 0.0])
n_alpha = np.array([0.0, 0.0, 1.0])

# AC 방향 단위벡터: u_x=cos(t1)=3/5, u_z=cos(t1)=3/5, u_y=sqrt(7)/5
u_x = cos_t1
u_z = cos_t1
u_y_sq = 1 - u_x**2 - u_z**2
assert u_y_sq > 0, 'imaginary component'
u_y = np.sqrt(u_y_sq)
u_AC = np.array([u_x, u_y, u_z])

# 조건 1 검증: angle(AB, AC) = theta1  =>  sin = 4/5
cos_AB_AC = abs(np.dot(AB, u_AC))
sin_AB_AC = np.sqrt(1 - cos_AB_AC**2)
cond1 = abs(sin_AB_AC - sin_t1) < 1e-9

# 조건 2 검증: angle(AC, alpha) = pi/2 - theta1  =>  sin = cos(t1) = 3/5
sin_AC_alpha = abs(np.dot(u_AC, n_alpha))
angle_AC_alpha = np.arcsin(sin_AC_alpha)
expected_angle = np.pi/2 - np.arcsin(sin_t1)
cond2 = abs(angle_AC_alpha - expected_angle) < 1e-9

# 평면 ABC 법벡터
n_ABC = np.cross(AB, u_AC)   # (0, -3/5, sqrt(7)/5)

# cos(theta2)
cos_t2 = abs(np.dot(n_alpha, n_ABC)) / (np.linalg.norm(n_alpha) * np.linalg.norm(n_ABC))
expected_cos_t2 = np.sqrt(7) / 4
cond3 = abs(cos_t2 - expected_cos_t2) < 1e-9

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'sin(angle AB,AC)={sin_AB_AC:.6f}  expected={sin_t1}')
    print(f'angle(AC,alpha)={angle_AC_alpha:.6f}  expected={expected_angle:.6f}')
    print(f'cos_theta2={cos_t2:.6f}  expected={expected_cos_t2:.6f}')
