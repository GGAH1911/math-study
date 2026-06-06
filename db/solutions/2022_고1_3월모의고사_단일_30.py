import numpy as np
from sympy import symbols, solve, simplify, Rational

# 변수 설정
h = symbols('h', positive=True)
c = 12  # BC 길이 (EF=3 조건에서 구함)

# 좌표 설정
A = np.array([0.0, 1.0])  # 임의 h=1로 정규화
B = np.array([0.0, 0.0])
D = np.array([4.0, 1.0])
C = np.array([12.0, 0.0])

# 대각선 교점 E
# AC: y = 1 - x/12
# BD: y = x/4
# 교점: 1 - x/12 = x/4 → x = 3
E = np.array([3.0, 0.75])

# F 점 (E를 지나고 AD와 평행한 직선이 CD와 만나는 점)
# CD: y = (x-12)/(-8) = (12-x)/8
# y = 0.75에서: 0.75 = (12-x)/8 → x = 6
F = np.array([6.0, 0.75])

# EF 확인
EF_dist = abs(F[0] - E[0])
print(f"EF distance: {EF_dist} (expected 3)")
assert abs(EF_dist - 3.0) < 1e-9, f"EF check failed"

# G 점 (AC와 BF의 교점)
# AC: y = 1 - x/12
# BF: B(0,0) → F(6, 0.75), 방정식: y = 0.75/6 * x = x/8
# 교점: 1 - x/12 = x/8 → 1 = x/8 + x/12 = 5x/24 → x = 24/5
G = np.array([24.0/5.0, 3.0/5.0])

# 검증: G가 AC 위에 있는가
y_AC = 1.0 - G[0]/12.0
print(f"G y-coord: {G[1]}, AC에서의 y: {y_AC}")
assert abs(G[1] - y_AC) < 1e-9, "G not on AC"

# 검증: G가 BF 위에 있는가
y_BF = G[0] / 8.0
print(f"G y-coord: {G[1]}, BF에서의 y: {y_BF}")
assert abs(G[1] - y_BF) < 1e-9, "G not on BF"

# 삼각형 EGF의 넓이 (h=1일 때)
triangle_area = 0.5 * abs((E[0]-F[0])*(G[1]-E[1]) - (E[0]-G[0])*(F[1]-E[1]))
print(f"Triangle EGF area (h=1): {triangle_area}")
print(f"Expected (9/40): {9/40}")
assert abs(triangle_area - 9/40) < 1e-9, "Triangle area check failed"

# 사다리꼴 ABCD의 넓이 (h=1일 때)
trapezoid_area = 0.5 * (4.0 + 12.0) * 1.0
print(f"Trapezoid ABCD area (h=1): {trapezoid_area}")

# k 계산
k = trapezoid_area / triangle_area
print(f"k = {k}")
print(f"9k = {9*k}")
assert abs(9*k - 320) < 1e-9, f"9k check failed: got {9*k}"

print("\nVERIFY_PASS")