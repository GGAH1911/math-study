import sympy as sp
import numpy as np
from sympy import symbols, cos, sin, sqrt, solve, simplify

# 문제 설정
r, k = 3, -18
theta, phi = symbols('theta phi', real=True)

# P'의 좌표 (P를 y=x 대칭)
x1 = r * sin(theta)
y1 = 6 + r * cos(theta)

# Q'의 좌표 (Q를 x방향 k 평행이동)
x2 = 6 + r * cos(phi) + k
y2 = r * sin(phi)

# 기울기
slope = (y2 - y1) / (x2 - x1)

# 최솟값이 0이 되는 경우: theta=pi, phi=pi/2
theta_min = sp.pi
phi_max = sp.pi/2

x1_min = r * sin(theta_min)  # 0
y1_min = 6 + r * cos(theta_min)  # 6 - 3 = 3
x2_max = 6 + r * cos(phi_max) + k  # 6 + 0 - 18 = -12
y2_max = r * sin(phi_max)  # 3

slope_min = (y2_max - y1_min) / (x2_max - x1_min)
print(f"Slope at min case: {slope_min} (should be 0)")
if slope_min == 0:
    print("✓ Minimum slope = 0")

# 공통외접선 기울기 검증
# m^2[(6+k)^2 - 36] + 12m(6+k) = 0
a = 6 + k  # -12
m = symbols('m', real=True)
eq = m**2 * (a**2 - 36) + 12*m*a
solutions = solve(eq, m)
print(f"\nCommon tangent slopes: {solutions}")
print(f"Slopes: {[float(s) if s.is_real else s for s in solutions]}")

# 다른 기울기도 확인 (m = -6/(6+k))
m_case_a = -6 / (6 + k)
print(f"\nCase A slope: m = -6/(6+k) = {m_case_a}")

all_slopes = sorted([float(s) if s.is_real else s for s in solutions] + [m_case_a])
print(f"All critical slopes: {all_slopes}")
print(f"Min: {min(all_slopes)}, Max: {max(all_slopes)}")

if min(all_slopes) == 0 and max(all_slopes) == float(4/3):
    print("✓ Conditions satisfied: min=0, max=4/3")
    print(f"\n|r + k| = |{r} + {k}| = {abs(r + k)}")
    print("\nVERIFY_PASS")
else:
    print("VERIFY_FAIL")