import numpy as np
from scipy.optimize import fsolve

# 포물선: y^2 = 16x
# P = (8, 8√2)
P = np.array([8, 8*np.sqrt(2)])

# 초점 F1, F3
F1 = np.array([4, 0])
F3 = np.array([-8, 0])

# 타원의 중심과 c
center = np.array([-2, 0])
c = 6
a = np.sqrt(54)
b = 3*np.sqrt(2)

# 단축 꼭짓점
vertex = np.array([-2, b])

# 선분 PF3의 직선 방정식: y = (√2/2)(x+8)
# vertex가 이 직선 위에 있는지 확인
y_on_line = (np.sqrt(2)/2) * (vertex[0] + 8)
print(f"Vertex y-coordinate: {vertex[1]}")
print(f"Line y-value at x=-2: {y_on_line}")
print(f"Match: {np.isclose(vertex[1], y_on_line)}")

# 타원 방정식 검증: (x+2)²/a² + y²/b² = 1
ellipse_val = (vertex[0] + 2)**2 / a**2 + vertex[1]**2 / b**2
print(f"Ellipse equation at vertex: {ellipse_val}")
print(f"Should be 1: {np.isclose(ellipse_val, 1)}")

# 초점 거리 검증
focal_distance = np.linalg.norm(F1 - F3)
print(f"Focal distance 2c: {focal_distance}")
print(f"Should be 12: {np.isclose(focal_distance, 12)}")

# a² 값 검증
a_squared = a**2
print(f"\na² = {a_squared}")

if np.isclose(a_squared, 54):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")